from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

def scrape_dividend_history(quotes):
    # Setup Chrome options
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--ignore-ssl-errors=yes')
    chrome_options.add_argument('--ignore-certificate-errors')

    # Initialize the driver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
    #                         options=chrome_options)
    driver = webdriver.Remote(
            command_executor='http://172.17.0.2:4444/wd/hub', # Change with the selenium' container IP adress
            options=chrome_options
            )

    try:
        # Navigate to the page
        url = f"https://finance.yahoo.com/quote/{quotes}/history/?filter=div&period1=907657200&period2=1718220885"
        driver.get(url)
        # Wait for cookie consent and click if present
        try:
            cookie_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "agree"))
            )
            cookie_button.click()
        except:
            pass

        # Wait for the table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )

        # Extract dividend's quote name
        div_name = driver.find_elements(By.CLASS_NAME, "yf-xxbei9") # Faire attention régulièrement à d'éventuels changement de nom de classe
        quote_name = div_name[0].text
        print(f"Extracting {quote_name}'s data...")


        # Extract table data
        dividend_data = []
        table = driver.find_elements(By.TAG_NAME, "table")
        # print("table: ",table)
        
        for row in table:
            r = row.find_elements(By.TAG_NAME, "tbody")
            # print("row_data:", r)

            for row in r:
                tr = row.find_elements(By.TAG_NAME, "tr")
                # print("tr_data:", tr)

                for tr_ in tr:
                    td = tr_.find_elements(By.TAG_NAME, "td")

                    if td:
                        dividend_data.append({
                            "Date":td[0].text,
                            "Dividend":td[1].find_elements(By.TAG_NAME, "span")[0].text,
                            "Quote": quote_name
                        })

        # Convert to DataFrame
        df = pd.DataFrame(dividend_data)
        return df
        # return dividend_data

    finally:
        driver.quit()

if __name__ == "__main__":
    quotes = ["ZURN.SW","SCMN.SW","RMS.PA","V","BLK","SLHN.SW"]
    dataframes = []
    for quote in quotes:
        df_ = scrape_dividend_history(quote)
        dataframes.append(df_)
    
    df = pd.concat(dataframes, ignore_index=True)
    # Optionally save to CSV
    df.to_csv('actions_dividends.csv', index=False)
