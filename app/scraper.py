import requests
from bs4 import BeautifulSoup
from app.config import Config

class MangaScraper:
    @staticmethod
    def scrape_manga(data):
        headers = Config.REQUEST_HEADERS
        try:
            response = requests.get(data['url'])
            response = requests.get(data['url'], headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("h1").text
            chapters = [
                {
                    "chapter": chap.text.strip(),
                    "link": chap["href"]
                }
                for chap in soup.select(data['all_chapter_selector'])  # Adjust selector based on site structure
            ]

            return {
                "title": title,
                "chapters": chapters
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    @staticmethod
    def scrape_manga_detail(data):
        headers = Config.REQUEST_HEADERS
        try:
            response = requests.get(data['url'])
            response = requests.get(data['url'], headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            images = [
                {
                    "image_url": image["src"]
                }
                for image in soup.select(data['image_selector'])  # Adjust selector based on site structure
            ]

            return {
                "images": images
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
