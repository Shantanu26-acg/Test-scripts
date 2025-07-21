from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time
import random
import pandas as pd

chrome_options=Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('ignore-ssl-errors')
chrome_options.add_argument('allow-insecure-localhost')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

service=Service(r"C:\Users\Shantanu\Downloads\chromedriver-win32\chromedriver.exe")

driver=webdriver.Chrome(service=service, options=chrome_options)
wait=WebDriverWait(driver, 15)

df=pd.read_excel("Master Data.xlsx", sheet_name="URLs", header=None)

login_url=df.iloc[0, 0]
serialization_url=df.iloc[2, 0]

def run_batch(driver, wait, po_name):
    driver.get(serialization_url)

    time.sleep(5)

    driver.find_element(By.ID, "datacontenttab_2").click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//table[@id='productionorders_list_table']")))

    row_xpath = f"//tr[td[normalize-space(text())='{po_name}']]"
    row = wait.until(
        EC.presence_of_element_located((By.XPATH, row_xpath))
    )

    edit_button = row.find_element(By.XPATH, ".//a[@title='Production order overview']")

    driver.execute_script("arguments[0].click();", edit_button)

    wait.until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sendtoproductionbutton']"))).click()

    time.sleep(5)

driver.get(login_url)
wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("shantanu")
driver.find_element(By.NAME, "password").send_keys("tnt1234")
driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']").click()

run_batch(driver, wait, "Po_Irbesartan1")