from bs4 import BeautifulSoup
import requests
import pandas as pd

URL = "https://www.amazon.com/s?k=nintendo+games"

# Headers for request
HEADERS = ({'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36', 'Accept-Language': 'en-US, en;q=0.5'})

# HTTP Request
webpage = requests.get(URL, headers=HEADERS)

type(webpage.content)

# all data
soup = BeautifulSoup(webpage.content, "html.parser")
#print(f"soup \n{soup}")

# Fetch links as List
links = soup.find_all("a", attrs={'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
#print(f"links : \n{links}")

link = links[0].get('href')
#print(f"link : \n{link}")

product_list = "https://amazon.com" + link
#print(f"product_list : \n{product_list}")

new_webpage = requests.get(product_list, headers=HEADERS)
#print(f"new_webpage : \n{new_webpage}") #<Response [200]>


# new Soup all data
new_soup = BeautifulSoup(new_webpage.content, "html.parser")
#print(f"new_soup : \n{new_soup}") all html

title = new_soup.find("span", attrs={"id":'productTitle'}).text.strip()
print(f"title : {title}")

price =  new_soup.find("span", attrs={"class":'a-price'}).find("span", attrs={"class": "a-offscreen"}).text.strip()
print(f"price : {price}")

price2 =  new_soup.find("span", attrs={"class":'a-offscreen'}).text.strip()
print(f"price2 : {price2}")

reviews = new_soup.find("span", attrs={"class":'a-icon-alt'}).text
print(f"reviews : {reviews}")

ratings = new_soup.find("span", attrs={"id":'acrCustomerReviewText'}).text
print(f"ratings : {ratings}")
