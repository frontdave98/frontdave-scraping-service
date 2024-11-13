import requests
from bs4 import BeautifulSoup
from app.config import Config

class MangaScraper:
    @staticmethod
    def scrape_manga(url):
        headers = Config.REQUEST_HEADERS
        try:
            response = requests.get(url)
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("h1").text
            chapters = [
                {
                    "chapter_number": chap.text.strip(),
                    "link": chap["href"]
                }
                for chap in soup.select("#Chapters_List .ceo_latest_comics_widget a")  # Adjust selector based on site structure
            ]

            return {
                "title": title,
                "chapters": chapters
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
