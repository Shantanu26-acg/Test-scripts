from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# chrome_options=Options()
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('ignore-ssl-errors')
# chrome_options.add_argument('allow-insecure-localhost')
# chrome_options.add_argument('--disable-web-security')
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')

df_urls=pd.read_excel(
    "Master data.xlsx",
    sheet_name="URLs",
    header=None
)

dp=pd.read_excel("Master data.xlsx", sheet_name="Subject Master Data", engine="openpyxl", dtype={
    "GLN": str,
    "GS1 Company Prefix": str,
    "Remarks": str
})

masterdata_url=df_urls.iloc[1, 0]
login_url=df_urls.iloc[0, 0]

# service=Service(r"C:\Users\Shantanu\Downloads\chromedriver-win32\chromedriver.exe")
#
# driver=webdriver.Chrome(service=service, options=chrome_options)
# wait=WebDriverWait(driver, 15)

def create_location(driver, wait, location_name, subject_name, address, city, state, zip, country, gln):
    driver.get("https://172.16.70.109/?link=masterdata")
    driver.find_element(By.ID, 'datacontenttab_5').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@title='New location']"))).click()

    wait.until(EC.presence_of_element_located((By.NAME, 'location_name'))).send_keys(location_name)
    Select(driver.find_element(By.NAME, 'location_subject_id')).select_by_visible_text(subject_name)
    driver.find_element(By.NAME, 'location_address').send_keys(address)
    driver.find_element(By.NAME, 'location_city').send_keys(city)
    driver.find_element(By.NAME, 'location_state').send_keys(state)
    Select(driver.find_element(By.NAME, 'location_country')).select_by_visible_text(country)

    gln_location_field=wait.until(EC.presence_of_element_located((By.XPATH, "//input[@flag='gln' and contains(@class, 'locationpropertyvalue')]")))

    driver.execute_script("""
        arguments[0].value=arguments[1],
        arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
        arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
        arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
    """, gln_location_field, gln)

    driver.find_element(By.ID, 'savelocationbutton').click()

    ok_button=wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='OK']")))
    ok_button.click()

    try:
        alert_dialog = driver.find_element(By.CLASS_NAME, "ui-dialog-content")
        if "Location with same name already exists." in alert_dialog.text:
            driver.find_element(By.XPATH, "//button[normalize-space(.)='OK']").click()
            return
    except NoSuchElementException:
        pass

# driver.get(login_url)
# wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("shantanu")
# driver.find_element(By.NAME, "password").send_keys("tnt1234")
# driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']").click()
#
# for idx, row in dp.iterrows():
#     create_location(
#         driver=driver,
#         wait=wait,
#         location_name="loc_" + row['Subject Name'],
#         subject_name=row['Subject Name'],
#         address=row['Address'],
#         city=row['City'],
#         state=row['State'],
#         zip=row['Zip'],
#         country=row['Country'],
#         gln=row['GLN']
#     )
#
#     time.sleep(5)