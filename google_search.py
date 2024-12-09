# google_search.py
import subprocess
from bs4 import BeautifulSoup
import logging

# Set up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

def google_search_with_curl(query: str) -> str:
    """Perform a Google search using curl and return the top result."""
    try:
        # Construct the Google search URL
        query = query.replace(" ", "+")
        url = f"https://www.google.com/search?q={query}"

        # Run curl command to fetch the HTML
        logger.info(f"Fetching search results for query: {query}")
        process = subprocess.run(
            ["curl", "-s", url, "-A", "Mozilla/5.0"],  # Spoof a browser User-Agent
            capture_output=True,
            text=True,
            check=True
        )
        html_content = process.stdout

        # Parse HTML using BeautifulSoup
        soup = BeautifulSoup(html_content, "html.parser")
        search_results = soup.find_all("div", class_="BNeawe vvjwJb AP7Wnd")

        # Extract the first result
        if search_results:
            top_result = search_results[0].get_text()
            return f"Top result: {top_result}"
        else:
            return "No results found."
    except Exception as e:
        logger.error(f"Error performing Google search: {e}")
        return "Error fetching search results. Please try again later."
