import csv
import requests
import time
from bs4 import BeautifulSoup
import random

def scrape_book_data(base_url):
    response = requests.get(base_url)

    if response.ok:
        soup = BeautifulSoup(response.content, 'html.parser')
        all_books_title = soup.find_all('acronym')
        book_names = [book.text for book in all_books_title]
        all_books_price = soup.find_all("div", class_="text-primary font-weight-700")
        book_prices = [price.text.strip().split('\n')[0] for price in all_books_price]
        urls = []
        images = soup.find_all('div', class_="b-aspect")
        for image in images:
            style_attr = image['style']
            start_index = style_attr.find("url('") + 5
            end_index = style_attr.find("')")
            image_url = style_attr[start_index:end_index]
            urls.append(image_url)

        return book_names, book_prices, urls

def scrape_multiple_pages(base_url, num_pages, request_interval):
    all_book_names = []
    all_book_prices = []
    all_urls = []

    for page in range(1, num_pages + 1):
        page_url = base_url + f"&page={page}"
        book_names, book_prices, urls = scrape_book_data(page_url)
        all_book_names.extend(book_names)
        all_book_prices.extend(book_prices)
        all_urls.extend(urls)

        time.sleep(request_interval)

    return all_book_names, all_book_prices, all_urls


base_url = "https://biblusi.ge/products?category=291&category_id=317"
num_pages = 5

request_interval = random.randint(15, 20)

book_names, book_prices, urls = scrape_multiple_pages(base_url, num_pages, request_interval)
filename = "book_inventory.csv"
with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Book Name", "Price", "URL"])
    for i in range(len(book_names)):
        writer.writerow([book_names[i], book_prices[i], urls[i]])
print("Data saved to", filename)





