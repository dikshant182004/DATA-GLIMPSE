# Data Glimpse

Data Glimpse is a Streamlit application designed to automate the web scraping process, utilizing the power of AutoScraper and BeautifulSoup. This application simplifies the extraction of data from various websites, including e-commerce platforms like Amazon and Flipkart.

## Features

- Automates web scraping process.
- Supports scraping data from normal websites and e-commerce platforms.
- Uses AutoScraper for general web scraping and BeautifulSoup for scraping product pages.
- Enables users to input website links and specify tag details for scraping.

## Installation

To run Data Glimpse, ensure you have Python 3.x installed on your system. Then, follow these steps:

1. Clone this repository:

    ```bash
    git clone https://github.com/dikshant182004/Data-Glimpse.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Data-Glimpse
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the Streamlit application:

    ```bash
    streamlit run main.py
    ```

2. Input the website link you want to scrape data from.
3. If using for general web scraping:
   - Provide an example of the data you want to scrape.
4. If scraping e-commerce websites like Amazon:
   - Specify tag details required for BeautifulSoup.
   - Ensure the first tag is a `<div>` tag with a class or ID attributes
   - Other tags can be `<span>` and `<a>` with class and ID attributes.
5. After specifying the required details, click on the "Scrape Data" button.
6. View the scraped data in the form of a DataFrame.
7. Optionally, save the scraped data to your local computer.

## Example

Suppose you want to scrape product information from Amazon. Here's how you can use Data Glimpse:

1. Input the Amazon product page link.
2. Provide tag details for BeautifulSoup:
   - Container class (should be a `<div>` tag with the class or id information).

    - - Example: `<div class="puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-vbok7i09ua2q62ek5q2l21tt78 s-latency-cf-section puis-card-border">`
     
      - ## Application Screenshot

        ![Data Glimpse Screenshot](https://github.com/dikshant182004/DATA-GLIMPSE/blob/main/Images/Screenshot%20(876).png)


   - Other relevant tags like `<span>` and `<a>` with class and ID attributes.
  
   - - Example: `<span class ="a-size-medium a-color-base a-text-normal">`
       
3. Click on "Scrape Data" to fetch and display the product information.
4. Optionally, save the scraped data as a CSV file on your local machine.

## Support

For any queries or assistance, feel free to contact [dikshant182004@gmail.com](mailto:dikshant182004@gmail.com).


