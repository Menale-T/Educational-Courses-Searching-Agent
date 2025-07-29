from dotenv import load_dotenv
import os
import sys
sys.path.append('../')
from .agent_flow import AgentFlow

load_dotenv()

def run(query):

  agentFlow = AgentFlow()
  print("Courses Research Agent")

  while True:
    ##query = input("\n Courses Query: ").strip()
    if query.lower() in {"quit", "exit"}:
        break

    if query:
        result = agentFlow.run(query)
        print(f"\n Results for: {query}")
        print("="*60)

        for i, institution in enumerate(result.institutions, 1):
            print(f"\n{i}. 🏢 {institution.name}")
            print(f"   🌐 Website: {institution.website}")
            print(f"   💰 Pricing: {institution.pricing}")
            print(f"   📖 Online: {institution.is_online}")
            
            if institution.description and institution.description != "Analysis failed":
               print(f" Description: {institution.description}")
               return institution.description
            
            if institution.is_online:
               print(f" Is Online: {institution.is_online}")
               return institution.is_online

            '''if institution.certificate_available:
               print(f"Certificate available after completion: {institution.certificate_available}")
            '''
            if institution.duration:
               print(f"Course duration: {institution.duration}")
               return institution.duration
        if result.analysis:
                print("Developer Recommendations: ")
                print("-" * 40)
                print(result.analysis)  
                return result.analysis  
