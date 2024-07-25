import requests
from bs4 import BeautifulSoup

URL = "https://www.trendhunter.com/report?ak=cr_3764e3c6095a42fb08e3a9c6d0ca1#idea=485683"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
print(soup)