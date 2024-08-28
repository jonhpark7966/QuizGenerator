import requests
import datetime
import os

from crewai_tools import BaseTool

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
    ret = NewsAPITool()._run("웨스팅하우스")
    print(ret)
