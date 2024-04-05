from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import requests

# URL of the webpage
url = "https://www.amazon.in/s?k=mobile+phones&crid=3GR8LKA7J2JL&sprefix=mobile+phone%2Caps%2C356&ref=nb_sb_noss_1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.37'
}

# Send a GET request to the webpage and get the HTML content
response = requests.get(url, headers=headers)

if response.status_code != 200:
    with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            html_content = page.content()
            soup=BeautifulSoup(html_content,"html.parser") 
else:
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

# Find all div elements with the specified class
div_elements = soup.find_all("div", class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v1vrzjn78dyt752h9j3p7fl64h2 s-latency-cf-section puis-card-border")
print(div_elements)
# Iterate through each div element
for div in div_elements:
    try:
        # Try to find span element with the specified class for product name
        product_name_span = div.find("span", class_="a-size-medium a-color-base a-text-normal")
        if product_name_span:
            product_name = product_name_span.get_text(strip=True)
            print("Product Name:", product_name)
        else:
            product_name = ""
    except ZeroDivisionError:
        # Handle ZeroDivisionError if it occurs
        print("ZeroDivisionError occurred")

