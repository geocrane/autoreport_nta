import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def document_initialised(driver):
    return driver.execute_script("return initialised")

options = Options()
options.add_argument("--headless")
driver = webdriver.Chrome(options=options)

driver.get("https://vc.ru/newtechaudit/entries/new")
wait = WebDriverWait(driver, 10)

titles = ""
for i in range(3):
    driver.execute_script('window.scrollBy(0, 1000);')
    # WebDriverWait(driver, timeout=10).until(document_initialised)
    time.sleep(1)
    # html = driver.page_source
    # soup = BeautifulSoup(html, "html.parser")
    # new_titles = soup.findAll('div', attrs = {'class':'content-title'})
    # if new_titles == titles:
    #     continue
    # titels = new_titles
    # print(titles)

html = driver.page_source
driver.quit()

soup = BeautifulSoup(html, "html.parser")
chunks = soup.findAll('div', attrs = {'class':'content-title content-title--short l-island-a'})
print(chunks)