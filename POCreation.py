from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time
import random
import pandas as pd

chrome_options=Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--allow-insecure-localhost')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

service=Service(r"C:\Users\Shantanu\Downloads\chromedriver-win32\chromedriver.exe")
driver=webdriver.Chrome(service=service, options=chrome_options)
wait=WebDriverWait(driver, 15)

df_urls=pd.read_excel(
    "Master data.xlsx",
    sheet_name="URLs",
    header=None
)

login_url=df_urls.iloc[0, 0]
masterdata_url=df_urls.iloc[1, 0]
serialization_url=df_urls.iloc[2, 0]

df=pd.read_excel("Master Data.xlsx", sheet_name="PO Data", dtype={
    "Lot/Batch Number": str,
    "Production Date": str,
    "MFG Date": str,
    "Expiration Date": str
})

def create_po(driver, wait, po_name, serial_numbers_provider, product_name, packaging_version, lot_number, production_date, mfg_date, expiration_date, regulation, manufacturing_location, quantity, production_line):
    driver.get(serialization_url)

    driver.find_element(By.ID, 'datacontenttab_2').click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@title='New production order']"))).click()

    wait.until(EC.element_to_be_clickable((By.ID, "po_name"))).send_keys(po_name)
    Select(driver.find_element(By.ID, "production_provider_id")).select_by_visible_text(serial_numbers_provider)
    time.sleep(5)

    driver.find_element(
        By.XPATH,
        "//span[@id='select2-packaging_product_id-container']/ancestor::span[contains(@class,'select2-selection')]"
    ).click()

    search_input = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(@class,'select2-dropdown')]//input[@type='search']")
    ))

    search_input.send_keys(product_name)
    search_input.send_keys(Keys.ENTER)

    Select(driver.find_element(By.ID, "packaging_product_version_id")).select_by_visible_text(packaging_version)
    driver.find_element(By.ID, "production_lot").send_keys(lot_number)
    driver.find_element(By.ID, "productiondate").send_keys(production_date)
    driver.find_element(By.ID, "manufacturedate").send_keys(mfg_date)
    driver.find_element(By.ID, "expirationdate").send_keys(expiration_date)
    Select(driver.find_element(By.ID, "po_standard_id")).select_by_visible_text(regulation)

    wait.until(EC.invisibility_of_element_located((By.ID, "lightbox-overlay")))

    driver.find_element(
        By.XPATH,
        "//span[@id='select2-location_id-container']/ancestor::span[contains(@class,'select2-selection')]"
    ).click()

    location_search_input = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[contains(@class,'select2-dropdown')]//input[@type='search']")
    ))

    location_search_input.send_keys(manufacturing_location)

    location_search_input.send_keys(Keys.ENTER)

    time.sleep(5)

    Select(driver.find_element(By.ID, "location_line_id")).select_by_visible_text(production_line)

    time.sleep(5)

    quantity_props_tab = driver.find_element(By.LINK_TEXT, "Quantity and packaging")
    driver.execute_script("arguments[0].click();", quantity_props_tab)

    sources = driver.find_elements(By.CSS_SELECTOR, "div.qp_line_system.ui-draggable[unitid]")

    containers = driver.find_elements(By.CSS_SELECTOR, "div.qp_line_system[linesystemid]")

    drop_targets = []
    for container in containers:
        try:
            dest = container.find_element(By.CSS_SELECTOR, "div.packdrop")
            drop_targets.append((container, dest))
        except:
            continue

    actions = ActionChains(driver)

    for (source, (container, dest)) in zip(sources, drop_targets):
        driver.execute_script("arguments[0].scrollIntoView(true);", source)
        driver.execute_script("arguments[0].scrollIntoView(true);", dest)

        actions.click_and_hold(source).pause(0.5).move_to_element(dest).pause(0.5).release().perform()
        time.sleep(2)

    for container in containers:
        dest = container.find_element(By.CSS_SELECTOR, "div.packdrop")
        driver.execute_script("arguments[0].scrollIntoView(true);", dest)
        time.sleep(1)

        select_element = container.find_element(By.XPATH, ".//select[contains(@class, 'qp_link_system_prn_id')]")
        options = select_element.find_elements(By.TAG_NAME, "option")
        if len(options) > 1:
            Select(select_element).select_by_index(1)
        else:
            print("No PRN options available. Skipping.")

        time.sleep(2)

        quantity_input = container.find_element(By.XPATH, ".//input[contains(@class, 'qp_link_system_quantity')]")
        try:
            wait.until(EC.element_to_be_clickable((By.XPATH, ".//input[contains(@class, 'qp_link_system_quantity')]")))
            quantity_input.clear()
            quantity_input.send_keys(quantity)
        except:
            print("Quantity input not clickable. Skipping.")

        # try:
        #     subject_field = container.find_element(By.XPATH, ".//span[contains(@class, 'select2-selection--single')]")
        #     subject_field.click()
        #
        #     search_input = wait.until(EC.visibility_of_element_located(
        #         (By.XPATH, "//span[contains(@class,'select2-dropdown')]//input[@type='search']")
        #     ))
        #
        #     search_input.clear()
        #     search_input.send_keys(manufacturing_location)
        #     wait.until(EC.text_to_be_present_in_element_value(
        #         (By.XPATH, "//span[contains(@class,'select2-dropdown')]//input[@type='search']"),
        #         manufacturing_location
        #     ))
        #     search_input.send_keys(Keys.ENTER)
        #
        #     time.sleep(1)
        # except Exception as e:
        #     print("Subject field not present or could not select. Skipping.", e)

        time.sleep(2)

    driver.find_element(By.ID, "saveproductionbutton").click()

    ok_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[normalize-space(.)='OK']"
        ))
    )

    ok_button.click()




driver.get("https://172.16.70.109/login/")
wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("shantanu")
driver.find_element(By.NAME, "password").send_keys("tnt1234")
driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']").click()

po_name=df.loc[0, "PO Name"]
serial_numbers_provider=df.loc[0, "Serial Numbers Provider"]
product_name=df.loc[0, "Product"]
packaging_version=df.loc[0, "Packaging Version"]
lot_number=df.loc[0, "Lot/Batch Number"]
production_date=df.loc[0, "Production Date"]
mfg_date=df.loc[0, "MFG Date"]
expiration_date=df.loc[0, "Expiration Date"]
regulation=df.loc[0, "Regulation"]
manufacturing_location=df.loc[0, "Manufacturing Location"]
production_line=df.loc[0, 'Production Line']
create_po(driver, wait, po_name, serial_numbers_provider, product_name, packaging_version, lot_number, production_date, mfg_date, expiration_date, regulation, manufacturing_location, 100, production_line)
time.sleep(5)