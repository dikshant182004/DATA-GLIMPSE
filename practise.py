from autoscraper import AutoScraper
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import requests
import streamlit as st
import validators
import logging
    
# Configure logging
logging.basicConfig(filename='scraping.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class MyException(Exception):
    def __init__(self, message):
        self.message = message
        st.error(self.message)
        logging.error(message)

class TagDetails:
    def __init__(self, tag_name, id_or_class, class_name, find_method):
        self.tag_name = tag_name
        self.id_or_class = id_or_class
        self.class_name = class_name
        self.find_method = find_method

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

        tag_details_list = []

        tag_index = 0
        while st.checkbox(f"Add Tag {tag_index + 1}", key=f"add_tag_{tag_index}"):
            with st.expander(f"Tag {tag_index + 1} Details"):
                tag_name = st.selectbox("Select Tag Name", ['div', 'span', 'a', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li', 'table', 'tr', 'td', 'th', 'img', 'form', 'input', 'button', 'textarea'], key=f"tag_name_{tag_index}")
                id_or_class = st.radio("Select Id or Class", ["id", "class"], key=f"id_or_class_{tag_index}")
                class_name = st.text_input("Enter Id or Class Name", key=f"class_name_{tag_index}")
                find_method = st.radio("Select Find Method", ["find", "find_all"], key=f"find_method_{tag_index}")

                tag_details = TagDetails(tag_name, id_or_class, class_name, find_method)
                tag_details_list.append(tag_details)

            tag_index += 1

        st.markdown('<p style="font-size: 25px; font-weight: bold;">IN WHAT WAY WOULD YOU LIKE TO REPRESENT YOUR '
                    'DATA :</p>', unsafe_allow_html=True)
        
        self.genre = st.radio(
            "ENTER THE DATA FORMAT",
            ["**SCATTERED**", "**GROUPED**"],
            index=None,
            key="radio_genre"
        )

        if st.button("Let's Scrape !!!"):
            self.scrape_data()

        if st.button('Show Tag Details'):
            self.display_selected_tags(tag_details_list)

    def display_selected_tags(tag_details_list):
        if not tag_details_list:
            st.write("No tags selected.")
        else:
            for index, tag_details in enumerate(tag_details_list, start=1):
                st.write(f"Tag {index} details:",tag_details_list)
                st.write("")

    def complex_data_scraping(self,url,response):
        try:
            # using this to get flexibility with the browser and get the html content if the user-agent fails
            with sync_playwright() as p:
                browser = p.chromium.launch()
                page = browser.new_page()
                page.goto(url)
                html_content = page.content().decode("utf-8")  # Decode bytes to string
                print(html_content)
                browser.close()
            # build the scraper
            result=self.scraper.build(html=html_content,wanted_list=self.wanted_list)
            if self.genre == "**SCATTERED**":
                st.write(result)
            elif self.genre == "**GROUPED**":   
                # st.write(grouped_info)
                pass
            else:
                raise MyException("Failed to fetch the webpage. Status code: {}".format(response.status_code))
        except Exception as e:
            self.handle_exception("An error occured during Scraping",e)

    
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
            # grouped_info = self.scraper.get_result_similar(self.link, grouped=True)

            if self.genre == "**SCATTERED**":
                st.write(result)
            elif self.genre == "**GROUPED**":   
                # st.write(grouped_info)
                pass
            else:
                raise MyException("Not able to scrape data .Plz check your provided details again !!!")
        except Exception as e:
            self.handle_exception("An error occured during Scraping",e)

    def handle_exception(self, message, exception):
        st.error(f"{message}: {str(exception)}")
        logging.error(f"{message}: {str(exception)}",exc_info=True)

if __name__ == "__main__":
    WebScraper()
