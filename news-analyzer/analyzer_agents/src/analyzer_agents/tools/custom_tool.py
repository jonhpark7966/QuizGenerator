import requests
import datetime
import os
from bs4 import BeautifulSoup
import json

from crewai_tools import BaseTool

class NaverHeadlineTool(BaseTool):
    name: str = "Naver News Headlines Tool"
    description: str = "Crawl Naver news tab to get the headlines"

    def _run(self, argument: str) -> str:
        # Assuming 'argument' is the category candidate is one of the following:
        # 정치, 경제, 사회, 생활/문화, 세계, IT/과학

        # convert argument (category) to naver news category code
        category_code = {
          "정치":100, "경제":101, "사회":102, "생활/문화":103, "세계":104, "IT/과학":105
        }
        argument = str(category_code.get(argument, 100))

        url = f"https://news.naver.com/section/{argument}"
        # Send a request to fetch the HTML content of the page
        response = requests.get(url)
        if response.status_code == 200:
            html_content = response.text

            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find the specific <strong> tag with the class "sa_text_strong"
            strong_tags = soup.find_all('strong', class_='sa_text_strong')

            # Extract and return the text content as a json string
            news_headlines = []
            for index, strong in enumerate(strong_tags, 1):
                news_headlines.append(strong.get_text().strip())

            # return news_headlines in json format
            return json.dumps(news_headlines)

        else:
            return f"Failed to retrieve news. Status code: {response.status_code}"


class NaverNewsAPITool(BaseTool):
    name: str = "Naver News API Tool"
    description: str = "Call Naver News API to get the last 24 hour news articles."

    def _run(self, argument: str) -> str:
        # Assuming 'argument' could be the search query or topic
        client_secret = os.getenv("NAVER_CLIENT_SECRET")
        client_id = os.getenv("NAVER_CLIENT_ID")

        # Define the base URL for the Naver News API
        url = "https://openapi.naver.com/v1/search/news.json"

        # Set up the headers with your API credentials
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }

        # Define the search parameters
        params = {
            "query": argument,  # Replace with your search keyword
            "display": 10,                 # Number of results to display
            "start": 1,                    # Starting index of the results
            "sort": "date"                 # Sort by date
        }

        # Make the API request
        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            news_data = response.json()

            # get date string (24 hours ago from now) in format like "2024-08-28T09:44:19"
            date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)

            ret = []
            for item in news_data['items']:
                # break if the news is older than 24 hours
                # item['pubDate'] is string, convert it to datetime object
                # format: "Thu, 29 Aug 2024 17:42:00 +0900"
                pubDate = datetime.datetime.strptime(item['pubDate'], "%a, %d %b %Y %H:%M:%S %z")
                if pubDate < date:
                    break
                ret.append(item)

            return json.dumps(ret)

        else:
            print(f"Error {response.status_code}: {response.text}")


class NewsAPITool(BaseTool):
    name: str = "News API Tool"
    description: str = "Call News API to get the last 24 hour news articles."

    def _run(self, argument: str) -> str:
        # Assuming 'argument' could be the search query or topic
        api_key = os.getenv("NEWSAPI_KEY")

        # get date string (24 hours ago from now) in format like "2024-08-28T09:44:19"
        date = datetime.datetime.now() - datetime.timedelta(days=1)
        date_str = date.strftime("%Y-%m-%d")

        url = f"https://newsapi.org/v2/everything?q={argument}&from={date_str}&sortBy=popularity&apiKey={api_key}"
        print(url)

        response = requests.get(url)
        print(response.status_code)
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])

            if not articles:
                return "No news articles found for this query."

            # Extract and format the first few articles for brevity
            return articles
        else:
            return f"Failed to retrieve news. Status code: {response.status_code}"


class NewsAPIHeadlineTool(BaseTool):
    name: str = "News API Headlines Tool"
    description: str = "Call News API to get the headlines"

    def _run(self, argument: str) -> str:
        # Assuming 'argument' is the category candidate is one of the following:
        # business, entertainment, general, health, science, sports, technology
        # TODO, change countries.
        api_key = os.getenv("NEWSAPI_KEY")

        headline_url = f"https://newsapi.org/v2/top-headlines?country=kr&category={argument}&apiKey={api_key}"

        response = requests.get(headline_url)
        print(response.status_code)
        if response.status_code == 200:
            news_data = response.json()
            articles = news_data.get("articles", [])

            if not articles:
                return "No news articles found for this query."

            # Extract and format the first few articles for brevity
            return articles
        else:
            return f"Failed to retrieve news. Status code: {response.status_code}"


if __name__ == "__main__":
    #ret = NewsAPIHeadlineTool()._run("business")
    #ret = NewsAPITool()._run("웨스팅하우스")
    ret = NaverNewsAPITool()._run("이재명")
    print(ret)
