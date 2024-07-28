#pip install selenium pandas openpyxl
#pip install pandas
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
from selenium.common.exceptions import NoSuchElementException



driver = webdriver.Chrome()
driver.get("https://www.amazon.com")
driver.maximize_window() # it will maximize the window 
assert "Amazon" in driver.title # assert statement will check weather the condition is true or false.

#send the input to the elements 
search_box = driver.find_element(By.NAME, "field-keywords")# aa walu pehla website na inspect kar va nu pachi eema find kar va nu input tag search mate nu pachi eema name="" kai pan lakhyu hoi te aapre lakh va nu 
# u can get this web search bar element by clicking on that search bar and the just do right click and inspect.
#get the input to the web page
search_box.send_keys("mobile phones") 
search_box.send_keys(Keys.RETURN)
sleep(2)

#SCRAP PRODUCTS FROM THE AMAZON WEB PAGE 
products = []
for i in range(5):
    print('scrapping page',i+1)
    
    #locate product element by class name 
    product_elements = driver.find_elements(By.CSS_SELECTOR,'.s-result-item.s-asin')
    
    for product_element in product_elements:
        try:
            #retruve the title of that product
            title_element = product_element.find_element(By.CSS_SELECTOR,'.a-size-medium.a-color-base.a-text-normal')
            title = title_element.text
            #retrive the price from that product 
            price_element = product_element.find_element(By.CSS_SELECTOR,'.a-price-whole')
            price = price_element.text
            
            products.append({'title':title,'price':price}) # this will append price and title
        except NoSuchElementException:
            continue
    

    # for the next page button 
    try:
        next_button = driver.find_element(By.CSS_SELECTOR,".s-pagination-next")
        next_button.click()
        sleep(2)
    except NoSuchElementException:
        print("No more pages found")
        break
    
# Print the scraped products from the website
for product in products:
    print(product)
    
#save this printed data to an excel sheet 
df = pd.DataFrame(products)
df.to_excel("AMAZON_SCRAPPED_DATA_SELENIUM.xlsx",index=False)

driver.quit()
