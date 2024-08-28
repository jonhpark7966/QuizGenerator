import requests
from crewai_tools import BaseTool

class NewsAPITool(BaseTool):
    name: str = "News API Tool"
    description: str = "Call News API to get the latest news."

    def _run(self, argument: str) -> str:
        # Assuming 'argument' could be the search query or topic
        # FIXME: move the API key to a secure location
        api_key = ""

        #FIXME: change the source to a more generic one
        url = f"https://newsapi.org/v2/everything?q=tesla&from=2024-07-28&sortBy=publishedAt&apiKey={api_key}"

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


if __name__ == "__main__":
    ret = NewsAPITool()._run("")
    print(ret)
