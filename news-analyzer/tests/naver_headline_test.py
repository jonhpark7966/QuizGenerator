import requests
from bs4 import BeautifulSoup

# URL of the news section
url = 'https://news.naver.com/section/100'

# Send a request to fetch the HTML content of the page
response = requests.get(url)
html_content = response.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the specific <strong> tag with the class "sa_text_strong"
strong_tags = soup.find_all('strong', class_='sa_text_strong')

# Extract and print the text content
for index, strong in enumerate(strong_tags, 1):
    print(f"{index}. {strong.get_text().strip()}")
