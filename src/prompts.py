class CoursesPrompts:

    COURSE_EXTRACTION_SYSTEM =  """You are a educational courses researcher. Extract specific course, education tool, platform, or service names from articles covering all Natural Science, Social Science fields and from whole field of studies from all over the world.
                            Focus on actual courses/tools that online students can use to learn, not general concepts or services."""
    
    @staticmethod
    def course_extraction_user(query: str, content: str) -> str:
        return f"""Query: {query}
                Article Content: {content}
                Extract a list of specific course/learning material(tool) names mentioned in this content that are relevant to "{query}".

                Rules:
                - Only include actual courses names, not generic terms
                - Focus on courses learners can directly enroll/start learning
                - Include both free and paid options
                - Limit to the 15 most relevant tools
                - Return just the course/learning tool names, one per line, no descriptions

                Example format:
                ML 
                Data Science
                Accounting
                Business
                Law
                Videography,
                Theology
                Arts,
                Sports
                """
    COURSE_ANALYSIS_SYSTEM = """You are analyzing courses learning materials(tools) and Educational platforms. 
                            Focus on extracting information relevant to online learners/students and courses offering institutions. 
                            Pay special attention to courses, learning books/publications, Digital Platforms, Course Durations, and learning path/environment."""
    
    @staticmethod
    def course_analysis_user(institution_name: str, content: str) -> str:
        return f"""Institution: {institution_name}
                website Content: {content[:2500]}

                Analyze this content from an educational expert and from student perspective and provide:
                - pricing: One of "Free", "Freemium", "Paid", "Enterprise", or "Unknown"
                - is_online: true if open online, false if it requires physical presence, null if unclear
                - learning tools: List of platforms, frameworks, publications, or technologies supported/used
                - description: Brief 1-sentence description focusing on what this course/ learning tool is all about
                - certificate_available: true if certification after taking the course
                - career_capabilities: List of fields/careers it integrates with (e.g., Engineering, Devlopment, Attorny, Sales, Data Enconing, Personal Trainer etc.)

                Focus on student/learner-relevant features like courses, learning books/publications, Digital Platforms, Course Durations, and learning path/environment
                """
                
    RECOMMENDATIONS_SYSTEM = """You are an experienced educational consultant providing quick, concise course and learning platform/tool recommendations. 
                            Keep responses brief and actionable - maximum 3-4 sentences total."""
    
    
    @staticmethod
    def recommendation_user(query: str, institution_data: str) -> str:
        return f"""Student Query: {query}
                Courses/Learning tools/platforms Analyzed: {institution_data}

                Provide a brief recommendation (3-4 sentences max) covering:
                - Which course/learning tool/platform is best and why
                - Key cost/pricing consideration
                - Main technical advantage

                Be concise and direct - no long explanations needed.
                """