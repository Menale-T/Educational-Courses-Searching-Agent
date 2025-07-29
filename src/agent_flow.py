from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from .models import ResearchState, InstitutionInfo, InstitutionAnalysis
from .crawl import FirecrawlService
from .prompts import CoursesPrompts
import os
import sys
sys.path.append('../')

class AgentFlow:
    def __init__(self):
        self.crawl = FirecrawlService()
        self.llm = ChatGoogleGenerativeAI(model = "gemini-2.0-flash", temperature=0)
        self.prompts = CoursesPrompts()
        self.flow = self._agent_flow()

    def _agent_flow(self):
        
        graph = StateGraph(ResearchState)
        graph.add_node("extract_courses", self._extract_courses_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)
        graph.set_entry_point("extract_courses")
        graph.add_edge(start_key="extract_courses", end_key="research")
        graph.add_edge(start_key="research", end_key="analyze")
        graph.add_edge(start_key="analyze", end_key=END)
        return graph.compile()

    def _extract_courses_step(self, state: ResearchState) -> Dict[str, Any]:
        print(f"Finding Articles about: {state.query}")

        article_query = f"{state.query} courses best alternatives"
        search_results = self.crawl.search_institutions(article_query, num_results=3)
        all_content = ""
        for result in search_results.data:
            url = result.get("url", "")
            scraped = self.crawl.scrape_institution_page(url)
            if scraped:
                all_content + scraped.markdown[:1500] + "\n\n"
        
        messages = [
            SystemMessage(content=self.prompts.COURSE_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.course_extraction_user(state.query, all_content))
        ]

        try:
            response = self.llm.invoke(messages)
            course_names = [
                name.strip()
                for name in response.content.strip().split("\n")
                if name.strip()
            ]
            print(f"Extracted Courses: {', '.join(course_names[:5])}")
            return {"extracted courses:", course_names}
        except Exception as e:
            print(e)
            return {"extracted_courses": []}
    def _analyze_institution_contet(self, institution_name: str, content: str) -> InstitutionAnalysis:
        structured_llm = self.llm.with_structured_output(InstitutionAnalysis)
        messages = [
            SystemMessage(content=self.prompts.COURSE_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.course_analysis_user(institution_name, content))
        ]
        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(e)
            return InstitutionAnalysis(
                pricing = "Unknown",
                is_online = None,
                duration = "Failed",
                certificate_available = None,
            )
    def _research_step(self, state: ResearchState) -> Dict[str, Any]:
        extracted_courses = getattr(state, "extracted_courses", [])

        if not extracted_courses:
            print("No extracted courses found, falling back to direct search")
            search_results = self.crawl.search_institutions(state.query, num_results=3)
            course_names = [
                result.get("metadata", {}).get("title", "unknown")
                for result in search_results.data
            ]
        else:
            course_names = extracted_courses[:4]

        print(f"Researching specific courses: {', '.join(course_names)}")
        institutions = []
        for course_name in course_names:
            course_search_results = self.crawl.search_institutions(course_name + "official site", num_results=3)

            if course_search_results:
                result = course_search_results.data[0]
                url = result.get("url", "")

                institution = InstitutionInfo(
                    name=course_name,
                    description=result.get("markdown", ""),
                    website=url,
                )

                scraped = self.crawl.scrape_institution_page(url)
                if scraped:
                    content = scraped.markdown
                    analysis = self._analyze_institution_contet(institution.name, content)

                    institution.pricing = analysis.pricing
                    institution.is_online = analysis.is_online
                    institution.duration = analysis.duration
                    ##institution.certificate_available = analysis.certificate_available
                institutions.append(institution)
        return {"institutions": institutions}
    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        print("Generating recommendations")

        institution_data = ", ".join([
            institution.json() for institution in state.institutions
        ])
                  
        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendation_user(state.query, institution_data))
        ]

        response = self.llm.invoke(messages)
        return {"analysis": response.content}
    def run(self, query:str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.flow.invoke(initial_state)
        return ResearchState(**final_state)