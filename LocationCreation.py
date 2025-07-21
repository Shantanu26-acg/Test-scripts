from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

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