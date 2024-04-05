from autoscraper import AutoScraper
from playwright.sync_api import sync_playwright
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import openpyxl
import requests
import streamlit as st
import validators
import logging
import json
    
# Configure logging
logging.basicConfig(filename='scraping.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MyException(Exception):
    def __init__(self, message):
        self.message = message
        st.error(self.message)
        logging.error(message)

class TagDetails:
    def __init__(self, tag_name, id_or_class, class_name):
        self.tag_name = tag_name
        self.id_or_class = id_or_class
        self.class_name = class_name

class WebScraper:
    def __init__(self):
        self.link = ""
        self.wanted_list = []
        self.genre = ""
        self.scraper = AutoScraper()
        self.get_user_input()
        self.options=[]

    def get_user_input(self):
        st.markdown("""
            <div style="padding: 10px; background-color: #f44336; color: white; font-size: 18px; border-radius: 5px;">
                <p>
                    ⚠️ Disclaimer: Please note that web scraping can sometimes be against the terms of service of certain websites. 
                    It's important to respect the terms of service of each website you scrape. 
                    If you're scraping a complex site like Amazon, make sure to mention the required tags and adhere to their guidelines.
                </p>
            </div>
            """, unsafe_allow_html=True)
        st.title("Let's create the data")
        st.markdown("---")
        
        st.markdown('<h3 style="text-align:center; font-size: 30px; font-weight: bold;"> DATA RESEMBLANCE</h3>',
                    unsafe_allow_html=True)
        st.markdown('<p style="font-size: 25px; font-weight: bold;">ENTER THE URL OF THE WEBSITE YOU WANT TO '
                    'SCRAPE:</p>', unsafe_allow_html=True)
        self.link = st.text_input("LINK", key="website_url")
        st.markdown("---")
        st.markdown('<p style="font-size: 25px; font-weight: bold;">ENTER THE EXAMPLE OF DATA YOU WANT TO SCRAPE '
                    ':</p>', unsafe_allow_html=True)
        text = st.text_area("ENTER THE SAME AND UNIQUE VALUES FOR PROPER SCRAPING OF DATA (SEPARATE IT WITH A COMMA)", height=200)
        self.wanted_list = text.split(',')
        st.header("Tag Details")
        st.write("Specify the details for each tag you want to scrape.")


        tag_index = 0
        tag_details_list = []
        while st.checkbox(f"Add Tag {tag_index + 1}", key=f"add_tag_{tag_index}"):
            with st.expander(f"Tag {tag_index + 1} Details"):
                tag_name = st.selectbox("Select Tag Name", ['div', 'span', 'a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'img', 'form', 'input', 'button', 'textarea'], key=f"tag_name_{tag_index}")
                id_or_class = st.radio("Select Id or Class", ["id", "class"], key=f"id_or_class_{tag_index}")
                class_name = st.text_input("Enter Id or Class Name", key=f"class_name_{tag_index}")
                tag_details = TagDetails(tag_name, id_or_class, class_name)

                tag_details_list.append(tag_details)

            tag_index += 1

        if st.button("Save Tag Details"):
            self.save_tag_details(tag_details_list)
            st.success("Tag details saved successfully!")
        

        if st.button("Let's Scrape !!!"):
            self.scrape_data()

    import json

    def save_tag_details(self, tag_details):
        tag_details_dicts = []
        for tag_detail_obj in tag_details:
            tag_details_dicts.append({
                "tag_name": tag_detail_obj.tag_name,
                "id_or_class": tag_detail_obj.id_or_class,
                "class_name": tag_detail_obj.class_name,
            })
        with open("tag_details.json", "w") as file:
            json.dump({"tags": tag_details_dicts}, file, indent=4)

    def read_tag_details(self):
        try:
            with open("tag_details.json") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        
    def complex_data_scraping(self,url,response):
        options = Options()
        options.headless = True
        try:
            # using this to get flexibility with the browser and get the html content if the selenium fails
            # with sync_playwright() as p:
            #     browser = p.chromium.launch()
            #     page = browser.new_page()
            #     page.goto(url)
            #     html_content = page.content().decode("utf-8")  # Decode bytes to string
                driver = webdriver.Chrome(options=options)
                driver.get(url)
                # to give page loading time
                wait = WebDriverWait(driver, 10)  # Adjust the timeout as needed

                html_content = driver.page_source
                soup=BeautifulSoup(html_content,"html.parser") 
                driver.quit()
                self.using_soup(soup)
            
        except Exception as e:
            self.handle_exception("An error occured during Scraping",e)

    def using_soup(self, soup):
        data = self.read_tag_details()
        try:
            index=0
            div_elements = soup.find_all(data['tags'][index]['tag_name'], class_=data['tags'][index]['class_name'])
            self.iterate_over_span_tag(div_elements,index+1,data)
            # Iterate through each div element
        except Exception as e:
            self.handle_exception("An error occured during Scraping",e)


    def iterate_over_span_tag(self,div_elements,index,data):
        if index >= len(data['tags']):
        # No more tag details to process
            return
        for div in div_elements:
            try:
                # Try to find span element with the specified class for product name
                product_name_span = div.find(data['tags'][index]['tag_name'], data['tags'][index]['class_name'])
                if product_name_span:
                    product_name = product_name_span.get_text(strip=True)
                    st.write( product_name)
                    if (index+1) < len(data['tags']):
                        # using recursion
                        self.iterate_over_span_tag(div_elements,index+1,data)

                else:
                    product_name = ""
            except IndexError:
#             # Handle the case when there's no more tag details to process
                print("No more tag details to process.")
                break
            except ZeroDivisionError:
                print("ZeroDivisionError occurred")

    #        
    def scrape_data(self): 
        if not validators.url(self.link):
            st.error("Please provide a valid URL.")
            return

        if not self.wanted_list:
            st.error("Please provide examples of data to scrape.")
            return

        try:
            ## u can make use of proxies server to rotate your ip's and to get prevented from blocking
            # proxies = {
            #     "http": 'http://127.0.0.1:8001', 
            #     "https": 'https://127.0.0.1:8001',
            # }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.37'}
            response=requests.get(self.link,headers=headers)
            if response.status_code != 200:
                # set up selenium driver 
                return self.complex_data_scraping(self.link,response)

            html_content = response.content.decode('utf-8')
            result=self.scraper.build(html=html_content,wanted_list=self.wanted_list)
            if not result:
                soup = BeautifulSoup(html_content, "html.parser")
                self.using_soup(soup)
            else:
                st.write(result)
        except Exception as e:
            self.handle_exception("An error occured during Scraping",e)

    def handle_exception(self, message, exception):
        st.error(f"{message}: {str(exception)}")
        logging.error(f"{message}: {str(exception)}",exc_info=True)

if __name__ == "__main__":
    WebScraper()
