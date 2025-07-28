import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv
import sys

load_dotenv()

class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("Missing FIRECRAWL_API_KEY environment variable")
        self.app = FirecrawlApp(api_key=api_key)

    def search_institutions(self, query: str, num_results: int = 10):
        try:
            result = self.app.search(
                query=f"{query} instution",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        except Exception as e:
            print(e)
            return []
    def scrape_institution_page(self, url: str):
        try:
           
           result = self.app.scrape_url(
            url,
            formats=["markdown"]
           )
           return result
        except Exception as e:
            print(e)
            return None
