import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import time

df_urls=pd.read_excel(
    "Master data.xlsx",
    sheet_name="URLs",
    header=None
)

masterdata_url=df_urls.iloc[1, 0]

# def subject_creation(driver, wait, subject_name, group, address, city, zip, state, country, gln, gs1):
#     driver.get(masterdata_url)
#     driver.find_element(By.ID, "datacontenttab_4").click()
#     wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@title='New subject']"))).click()
#
#     wait.until(EC.visibility_of_element_located((By.ID, "subjectname"))).send_keys(subject_name)
#     Select(driver.find_element(By.ID, "subjectgroup_id")).select_by_visible_text(group)
#     driver.find_element(By.ID, 'subject_address').send_keys(address)
#     driver.find_element(By.ID, 'subject_city').send_keys(city)
#     driver.find_element(By.ID, 'subject_zip').send_keys(zip)
#     driver.find_element(By.ID, 'subject_state').send_keys(state)
#     time.sleep(5)
#     Select(driver.find_element(By.ID, 'subject_country')).select_by_visible_text(country)
#
#     driver.find_element(By.LINK_TEXT, "Subject properties")
#
    # gln_field = wait.until(
    #     EC.presence_of_element_located(
    #         (By.XPATH,
    #          "//table[@id='subjectproperties_table']//tr[td/input[@value='GLN']]/td/input[@class='certtitle subjectpropertyvalue ']")
    #     )
    # )
    #
    # driver.execute_script("""
    #     arguments[0].value = arguments[1];
    #     arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    #     arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    #     arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
    #     """, gln_field, gln)
    #
    # gs1_field = wait.until(
    #     EC.presence_of_element_located(
    #         (By.XPATH,
    #          "//table[@id='subjectproperties_table']//tr[td/input[@value='GS1 Company Prefix/GTIN Prefix']]/td/input[@class='certtitle subjectpropertyvalue  numeric']"
    #          )
    #     )
    # )
    #
    # driver.execute_script("""
    #     arguments[0].value=arguments[1];
    #     arguments[0].dispatchEvent(new Event('input', {bubbles:true}));
    #     arguments[0].dispatchEvent(new Event('change', {bubbles:true}));
    #     arguments[0].dispatchEvent(new Event('blur', {bubbles:true}));
    #     """, gs1_field, gs1)
#
#     driver.find_element(By.ID, 'savesubjectbutton').click()
#
    # ok_button=wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='OK']")))
    # ok_button.click()

#
#     time.sleep(5)


from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from datetime import datetime

def subject_creation(driver, wait, subject_name, group, address, city, zip, state, country, gln, gs1, remarks):
    driver.get(masterdata_url)
    driver.find_element(By.ID, "datacontenttab_4").click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@title='New subject']"))).click()

    wait.until(EC.visibility_of_element_located((By.ID, "subjectname"))).send_keys(subject_name)
    Select(driver.find_element(By.ID, "subjectgroup_id")).select_by_visible_text(group)
    driver.find_element(By.ID, 'subject_address').send_keys(address)
    driver.find_element(By.ID, 'subject_city').send_keys(city)
    driver.find_element(By.ID, 'subject_zip').send_keys(zip)
    driver.find_element(By.ID, 'subject_state').send_keys(state)
    time.sleep(2)
    Select(driver.find_element(By.ID, 'subject_country')).select_by_visible_text(country)

    driver.find_element(By.LINK_TEXT, "Subject properties").click()

    gln_field = wait.until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//table[@id='subjectproperties_table']//tr[td/input[@value='GLN']]/td/input[@class='certtitle subjectpropertyvalue ']")
        )
    )

    driver.execute_script("""
            arguments[0].value = arguments[1];
            arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
            arguments[0].dispatchEvent(new Event('blur', { bubbles: true }));
    """, gln_field, gln)

    gs1_field = wait.until(
        EC.presence_of_element_located(
            (By.XPATH,
             "//table[@id='subjectproperties_table']//tr[td/input[@value='GS1 Company Prefix/GTIN Prefix']]/td/input[@class='certtitle subjectpropertyvalue  numeric']"
             )
        )
    )

    driver.execute_script("""
            arguments[0].value=arguments[1];
            arguments[0].dispatchEvent(new Event('input', {bubbles:true}));
            arguments[0].dispatchEvent(new Event('change', {bubbles:true}));
            arguments[0].dispatchEvent(new Event('blur', {bubbles:true}));
    """, gs1_field, gs1)

    driver.find_element(By.ID, 'savesubjectbutton').click()

    ok_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='OK']")))
    ok_button.click()

    time.sleep(2)  # Let pop-up render if it's going to appear

    # Check for the duplicate subject dialog
    try:
        alert_dialog = driver.find_element(By.CLASS_NAME, "ui-dialog-content")
        if "Subject with same name already exists" in alert_dialog.text:
            print("⚠️ Duplicate subject detected.")
            remarks[0] = "subject already present"
            driver.find_element(By.XPATH, "//button[normalize-space(.)='OK']").click()
            return
    except NoSuchElementException:
        pass

        # 👇 Only run if no alert found
    remarks[0] = f"subject added on {datetime.today().strftime('%Y-%m-%d')}"