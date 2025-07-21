from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

df_url=pd.read_excel(
    "Master data.xlsx",
    sheet_name="URLs",
    header=None
)

# chrome_options=Options()
# chrome_options.add_argument('--ignore-certificate-errors')
# chrome_options.add_argument('ignore-ssl-errors')
# chrome_options.add_argument('allow-insecure-localhost')
# chrome_options.add_argument('--disable-web-security')
# chrome_options.add_argument('--disable-blink-features=AutomationControlled')
#
# service=Service(r"C:\Users\Shantanu\Downloads\chromedriver-win32\chromedriver.exe")
#
# driver=webdriver.Chrome(service=service, options=chrome_options)
# wait=WebDriverWait(driver, 15)

masterdata_url=df_url.iloc[1, 0]
login_url=df_url.iloc[0, 0]

dp=pd.read_excel("Master data.xlsx", sheet_name="Line Data", dtype={
    "Location Number": str,
    "Line Number": str,
    "Systems": str
})

dp['Location Number'] = dp['Location Number'].ffill()

def line_creation(driver, wait, loc_name, line_name, line_key, no_of_systems, systems):
    driver.get(masterdata_url)
    wait.until(EC.element_to_be_clickable((By.ID, 'datacontenttab_5'))).click()

    row_xpath = f"//tr[td[normalize-space(text())='{loc_name}']]"
    row = wait.until(
        EC.presence_of_element_located((By.XPATH, row_xpath))
    )

    edit_button = row.find_element(By.XPATH, ".//a[@title='Edit location']")

    driver.execute_script("arguments[0].click();", edit_button)

    lines_tab = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Lines")))
    driver.execute_script("arguments[0].click();", lines_tab)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@title='New line']"))).click()

    wait.until(EC.element_to_be_clickable((By.ID, "line_name"))).send_keys(line_name)
    driver.find_element(By.ID, "line_number").send_keys(line_key)

    systems_tab = wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Systems")))
    driver.execute_script("arguments[0].click();", systems_tab)

    for i in range(no_of_systems-1):
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input.button_add_window.certificatebottombutton.wide[value='Add system']"))).click()

    system_blocks = wait.until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.window.linesystem"))
    )

    time.sleep(5)

    # Step 3: For each block, find its dropdown and select from the systems array
    for i, block in enumerate(system_blocks):
        if i < len(systems):
            dropdown = block.find_element(By.CSS_SELECTOR, "select.linesystemselect")
            time.sleep(5)
            Select(dropdown).select_by_visible_text(systems[i])
        else:
            print(f"⚠️ Not enough system names provided for {len(system_blocks)} dropdowns.")

    driver.find_element(By.ID, "savelinebutton").click()

    ok_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[normalize-space(.)='OK']"
        ))
    )

    ok_button.click()

    time.sleep(5)

# driver.get(login_url)
# wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("shantanu")
# driver.find_element(By.NAME, "password").send_keys("tnt1234")
# driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']").click()
# line_creation(driver, wait, dp, "a", "b", "c", 3, ["PALLET_249", "PALLET_249", "PALLET_249"])
#
# time.sleep(5)