from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from urllib.parse import urljoin  # นำเข้า urljoin

# Define the base URL and parameters
base_url = "https://www.amazon.com/s?k=nintendo+games&i=videogames&rh=n%3A468642%2Cp_72%3A1248885011%2Cp_123%3A218247&dc&qid=1727078583&rnid=85457740011&ref=sr_pg_{}"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}

# Function product details
def fetch_product_details(link):
    new_webpage = requests.get(link, headers=HEADERS)
    if new_webpage.status_code == 200:
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")
        try:
            title = new_soup.find("span", attrs={"id": 'productTitle'}).text.strip()
            price = new_soup.find("span", attrs={"class": 'a-price'}).find("span", attrs={"class": "a-offscreen"}).text.strip()
            reviews = new_soup.find("span", attrs={"class": 'a-icon-alt'}).text
            ratings = new_soup.find("span", attrs={"id": 'acrCustomerReviewText'}).text
            return {
                "title": title,
                "price": price,
                "reviews": reviews,
                "ratings": ratings
            }
        except AttributeError:
            return None
    return None

# List to hold product data
product_data = []

# Loop multiple pages
for page in range(1, 12):  # Change the range to the number of pages you want to scrape
    url = base_url.format(page)
    webpage = requests.get(url, headers=HEADERS)
    
    if webpage.status_code == 200:
        soup = BeautifulSoup(webpage.content, "html.parser")
        links = soup.find_all("a", attrs={'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        for link in links:
            product_relative_link = link.get('href')
            product_link = urljoin("https://www.amazon.com", product_relative_link)  # ใช้ urljoin เพื่อสร้าง URL ที่ถูกต้อง
            product_details = fetch_product_details(product_link)
            if product_details:
                product_data.append(product_details)  # Add product details to the list
                
            time.sleep(1)  # หนึ่งวินาทีก่อนการร้องขอต่อไป
    else:
        print(f"Failed to retrieve page {page}")
    
    time.sleep(2)  # หน่วงเวลาเพิ่มเติมหลังจากแต่ละหน้า


df = pd.DataFrame(product_data)

df.to_csv("amazon_data_Full.csv", header=True, index=False)
