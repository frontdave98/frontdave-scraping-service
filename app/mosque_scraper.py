import requests
from bs4 import BeautifulSoup
from app.config import Config
import re

class MosqueScraper:
    @staticmethod
    def scrape_mosque(data):
        headers = Config.REQUEST_HEADERS
        try:
            url = "https://simas.kemenag.go.id/page/profilmasjid/index/0/0/0/0/0/none/%s" % (data['offset'])
            response = requests.get(url)
            response = requests.get(url, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")
            title = soup.find("h2").text
            lists = [
                {
                    "chapter": chap.find('h4').text.strip(),
                    "address": chap.find_all('p')[0].text.strip(),
                    "link": chap.find_all('a')[0].get('href'),
                    "map":  chap.find_all('a')[1].get('href'),
                    "img":  chap.find('img').get('src'),
                }
                for chap in soup.select('.search-result-item')  # Adjust selector based on site structure
            ]

            return {
                "title": title,
                "lists": lists
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
        
    @staticmethod
    def scrape_mosque_detail(data):
        headers = Config.REQUEST_HEADERS
        try:
            response = requests.get(data['url'])
            response = requests.get(data['url'], headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            # Images
            images = [image["href"] for image in soup.select('.profil-masjid-photos a') ]
            # Documents
            documents = [document["href"] for document in soup.select('.a-pdf') ]

            # History
            history_soup = soup.select('#content-sejarah')
            history = [element.prettify() for element in history_soup]

            #profile
            date_founding_text = soup.select('.masjid-alamat-calendar')[0].text.strip()
            date_founding_numbers = re.findall(r'\d+', date_founding_text)
            date_founding = ''.join(date_founding_numbers)

            profile = {
                "name": soup.select('.masjid-title')[0].text.strip(),
                "date_founding": date_founding,
                "email": soup.select('.masjid-alamat-phone p')[0].text.strip(),
                "website": soup.select('.masjid-alamat-phone p')[1].text.strip(),
                "address": soup.select('.masjid-alamat-location p')[0].text.strip(),
                "map": soup.select('.masjid-alamat-nav a')[0].get('href'),
                "nav": soup.select('.masjid-alamat-nav a')[1].get('href'),
            }

            summary = [{
                'item' : summary.find('h4').text.strip(),
                'total' : summary.select('p span')[0].text.strip(),
            } for summary in soup.select('.masjid-summary .col') ]

            # facilities =  [{
            #     'section' : detail.find('h4').text.strip(),
            #     'detail_items' : [{
            #         'spec' : "item.select('.label')[0].text.strip()",
            #     } for item in detail.select('.row .row')],
            # } for detail in soup.select('.section-content-info-wrapper')[1:3] ]

            return {
                "profile" : profile,
                "summary" : summary,
                "images": images,
                "history": history,
                "documents": documents,
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
