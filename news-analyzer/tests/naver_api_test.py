import requests

# Define your Naver API credentials
client_id = "edAznuYAvh6Sc1Coc4SX"
client_secret = "vlOoXvRoxW"

# Define the base URL for the Naver News API
url = "https://openapi.naver.com/v1/search/news.json"

# Set up the headers with your API credentials
headers = {
    "X-Naver-Client-Id": client_id,
    "X-Naver-Client-Secret": client_secret
}

# Define the search parameters
params = {
    "query": "테슬라",  # Replace with your search keyword
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
    for item in news_data['items']:
        print("Title:", item['title'])
        print("Description:", item['description'])
        print("Link:", item['link'])
        print("Published Date:", item['pubDate'])
        print("-" * 80)
else:
    print(f"Error {response.status_code}: {response.text}")
