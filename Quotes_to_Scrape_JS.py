from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')
servico= Service(ChromeDriverManager().install())
driver= webdriver.Chrome(service=servico)

url="http://quotes.toscrape.com"
url_page="/js/"
quotes_extraidas=[]

try:

    driver.get(url+url_page)
        
    
    while True:

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "quote"))
            )

        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        quotes= soup.find_all("div",class_="quote")

        for quote in quotes:
            message=quote.find("span",class_="text").text
            author=quote.find("small",class_="author").text
            
            quotes_extraidas.append([message, author])

        
        button=soup.find("li",class_="next")
        if button:
            button=button.find("a")["href"]
            driver.get(url+button)

            soup = BeautifulSoup(driver.page_source,"html.parser")
        else:
            print("No more pages to scrape")
            break
    
except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    driver.quit()


df=pd.DataFrame(quotes_extraidas,columns=["message","author"])

df.to_csv("quotes.csv",index=False,encoding="utf-8")

print(df["author"].value_counts().head(10))
