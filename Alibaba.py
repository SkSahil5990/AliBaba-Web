from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

options = Options()


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_url = "https://sourcing.alibaba.com/rfq/rfq_search_list.htm?country=AE&recently=Y"
driver.get(base_url)

rfq_data = []

max_pages = 5
page_num = 1


def scrape_page():
    WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rfq-item-info'))
    )
    rfqs = driver.find_elements(By.CSS_SELECTOR, '.rfq-item-info')

    for rfq in rfqs:
        try:
            title = rfq.find_element(By.CSS_SELECTOR, '.title').text.strip()
        except:
            title = ""

        try:
            category = rfq.find_element(By.CSS_SELECTOR, '.cat').text.strip()
        except:
            category = ""

        try:
            quantity = rfq.find_element(By.CSS_SELECTOR, '.amount').text.strip()
        except:
            quantity = ""

        try:
            location = rfq.find_element(By.CSS_SELECTOR, '.place').text.strip()
        except:
            location = ""

        try:
            date = rfq.find_element(By.CSS_SELECTOR, '.time').text.strip()
        except:
            date = ""

        try:
            link = rfq.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        except:
            link = ""

        rfq_data.append({
            "Title": title,
            "Category": category,
            "Quantity": quantity,
            "Location": location,
            "Date": date,
            "Link": link
        })
try:
    while page_num <= max_pages:
        print(f"Scraping Page {page_num}")
        scrape_page()
        time.sleep(2)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.ui-pagination-next'))
            )
            if 'disabled' in next_button.get_attribute('class'):
                break
            next_button.click()
            page_num += 1
        except Exception as e:
            print("Pagination error:", e)
            break

except Exception as e:
    print("Scraping error:", e)
finally:
    driver.quit()

df = pd.DataFrame(rfq_data)
df.to_csv("alibaba_rfq_scraped.csv", index=False, encoding='utf-8-sig')
print("✅ Data saved to alibaba_rfq_scraped.csv")
