from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

options = webdriver.ChromeOptions()
options.add_argument("--headless")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

cookies = ['fd0c22996ec4ab6ef76b99592b08e00e0e33fd30']

for cookie in cookies:
    driver.add_cookie(cookie)

url = f"https://x.com/G_Akky304250"
driver.get(url)

html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

tweets = soup.find("div", {'data-testid': 'cellInnerDiv'})

for tweet in tweets:
    content = tweet.find('div', {'data-testid': 'tweetText'}).text
    print(content)