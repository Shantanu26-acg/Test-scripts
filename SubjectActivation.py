from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time
import pandas as pd

df_urls=pd.read_excel(
    "Master data.xlsx",
    sheet_name="URLs",
    header=None
)

masterdata_url=df_urls.iloc[1, 0]

def activate_subject(driver, wait, name):
    driver.get(masterdata_url)

    driver.find_element(By.XPATH, "//a[@class='tabtitle' and contains(@href, 'subjectsList')]").click()

    wait.until(EC.presence_of_element_located((By.ID, 'datacontent')))

    row_xpath = f"//tr[td[normalize-space(text())='{name}']]"
    row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

    try:
        activate_button = row.find_element(By.XPATH, ".//a[contains(@href, 'activateSubject')]")
        driver.execute_script("arguments[0].click();", activate_button)

        time.sleep(2)

        ok_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[normalize-space(.)='OK']")
            )
        )
        ok_button.click()
        print(f"Subject '{name}' activated successfully.")
    except NoSuchElementException:
        # The button is not there; assume already active
        print(f"Subject '{name}' is already active.")
    except TimeoutException:
        # Optionally handle cases where dialog didn't appear
        print(f"Timeout occurred while activating '{name}'. It may already be active or the UI did not respond.")

    # row_xpath=f"//tr[td[normalize-space(text())='{name}']]"
    # row=wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))
    #
    # activate_button=row.find_element(By.XPATH, ".//a[contains(@href, 'activateSubject')]")
    #
    # driver.execute_script("arguments[0].click();", activate_button)
    #
    # time.sleep(2)
    #
    # ok_button=wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='OK']")))
    # ok_button.click()