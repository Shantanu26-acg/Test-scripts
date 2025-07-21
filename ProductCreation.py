from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

dp=pd.read_excel(
    "Master data.xlsx",
    sheet_name="Product Master Data",
    dtype={
        "GS1 Company Prefix": str,
        "GTIN": str,
        "No. of items in this level": str,
        "SSCC Extenson Digit(Loose Pack)": str
    }
)

dp['Product No'] = dp['Product No'].ffill()

df_url=pd.read_excel(
    "Master data.xlsx",
    sheet_name="URLs",
    header=None
)

masterdata_url=df_url.iloc[1, 0]
login_url=df_url.iloc[0, 0]

def create_and_activate_product(driver, wait, df):
    df=df[df['Product name and description'].notna()]

    common_cols = ["Product No", "Product name and description", "NDC Code", "Dosage", "Strength"]
    unique_cols = [
        "Level No", "Manufacturer", "GS1 Company Prefix", "GTIN", "Packaging Level",
        "No. of Items in this level", "NDC Type",
        "SSCC Extenson Digit(Loose Pack)", "SSCC Extension Digit(Full Pack)"
    ]

    df[common_cols] = df[common_cols].ffill()

    for product_no, product_group in dp.groupby('Product No'):
        product_name = product_group.iloc[0]["Product name and description"]
        manufacturer = product_group.iloc[0]["Manufacturer"].strip()
        print(f"Creating product: {product_no}")

        print(f"Creating product {product_name}")

        time.sleep(5)

        driver.get(masterdata_url)
        driver.find_element(By.ID, 'datacontenttab_3').click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//i[@title='New product']"))).click()

        wait.until(EC.visibility_of_element_located((By.ID, 'product_name'))).send_keys(product_name)
        Select(driver.find_element(By.ID, 'manufacturer_id')).select_by_visible_text(manufacturer)

        driver.execute_script("arguments[0].click();", driver.find_element(By.LINK_TEXT, "Product properties"))

        product_name_field = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        "//table[@id='productproperties_table']//tr[td/input[@value='Product Name']]/td/input[contains(@class, 'productpropertyvalue')]")))
        generic_name_field = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                        "//table[@id='productproperties_table']//tr[td/input[@value='Generic Name']]/td/input[contains(@class, 'productpropertyvalue')]")))

        for field in [product_name_field, generic_name_field]:
            driver.execute_script("""
                    arguments[0].value=arguments[1];
                    arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                    arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                    arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
                """, field, product_name)

        storage_dropdown = wait.until(EC.presence_of_element_located((By.XPATH,
                                                                      "//tr[td/input[@value='Storage Condition']]/td/select[contains(@class, 'productpropertyvalue')]")))
        Select(storage_dropdown).select_by_visible_text("below 25°C")

        time.sleep(5)

        driver.execute_script("arguments[0].click();", driver.find_element(By.LINK_TEXT, "Product packaging"))
        driver.find_element(By.ID, 'productpackagingmodelink').click()

        num_levels = product_group['Level No'].nunique()
        product_group = product_group.reset_index(drop=True)

        for i in range(num_levels):
            row=product_group.iloc[i]

            level_no = row['Level No']
            gtin = str(row['GTIN'])
            gs1_prefix = str(row['GS1 Company Prefix'])
            item_indicator = str(row['Item Indicator'])
            item_ref = str(row['Item Reference'])
            packaging_level = row['Packaging Level']
            item_count = str(row['No. of Items in this level'])
            sscc_extension_digit = str(row['SSCC Extension Digit(Loose Pack)'])

            print(level_no, gtin, gs1_prefix, item_indicator, item_ref, packaging_level, item_count, sscc_extension_digit, num_levels)

            time.sleep(10)

            Select(driver.find_elements(By.CSS_SELECTOR, '.productpackagingunit')[-1]).select_by_visible_text(packaging_level)
            if gtin=='' or gtin=="-":
                Select(driver.find_elements(By.CSS_SELECTOR, '.productpackagingunitcodetype')[-1]).select_by_visible_text('SSCC')
            else:
                Select(driver.find_elements(By.CSS_SELECTOR, '.productpackagingunitcodetype')[-1]).select_by_visible_text('GTIN')

            Select(driver.find_elements(By.CSS_SELECTOR, '.productpackagingunitindicator')[-1]).select_by_visible_text(item_indicator)
            driver.find_elements(By.CSS_SELECTOR, '.productpackagingitemreference')[-1].send_keys(item_ref)
            driver.find_elements(By.CSS_SELECTOR, '.productpackagingintemslayers')[-1].clear()
            driver.find_elements(By.CSS_SELECTOR, '.productpackagingintemslayers')[-1].send_keys(item_count)

            time.sleep(1)

            if i<num_levels-1:
                driver.find_element(By.ID, 'addItemCase').click()
                time.sleep(2)
        time.sleep(5)

        driver.find_element(By.ID, 'saveproductbutton').click()
        time.sleep(10)
        ok_button=wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='OK']")))
        ok_button.click()
        print("Product saved")

        # driver.get(masterdata_url)
        # driver.find_element(By.ID, 'datacontenttab_3').click()
        # wait.until(EC.invisibility_of_element_located((By.ID, "ajaxloaderover")))

        time.sleep(5)

        try:
            activate_button=driver.find_element(By.CSS_SELECTOR, "a[title='Activate product']")
            driver.execute_script("arguments[0].click();", activate_button)
            ok_button=wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='OK']")))
            ok_button.click()
            print("Product Activated")
        except:
            print("Product already activated or activation button not found")

        time.sleep(3)

# driver.get(login_url)
# wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("shantanu")
# driver.find_element(By.NAME, "password").send_keys("tnt1234")
# driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']").click()
# # Filter only the rows related to 1 product
# product_name_to_test = dp.iloc[0]['Product name and description']
# df_product = dp[dp['Product name and description'] == product_name_to_test]
#
# # Call the function
# create_and_activate_product(driver, wait, df_product)
#
# # Optional: Close browser after testing
# driver.quit()


































# for i, row in df.iterrows():
    #     gtin=str(row.get("GTIN", "")).strip()
    #     sscc=str(row.get("SSCC Extension Digit(Loose Pack)", "")).strip()
    #     gs1_prefix=str(row.get("GS1 Company Prefix", "")).strip()
    #     packaging_unit=str(row.get("Packaging Level", "")).strip()
    #
    #     if gtin=="-" or gtin=="":
    #         print(f"[{packaging_unit} Using SSCC: {sscc}")
    #         Select(driver.find_elements(By.CSS_SELECTOR, "select.productpackagingunitcodetype")[-1]).select_by_visible_text("SSCC")
    #         driver.execute_script("""
    #             arguments[0].value=arguments[1];
    #             arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
    #             arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
    #             arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
    #         """, driver.find_elements(By.CSS_SELECTOR, "input.productpackagingitemreference")[-1], "1234")
    #
    #         Select(driver.find_elements(By.CSS_SELECTOR, "select.productpackagingunitindicator")[-1]).select_by_visible_text(sscc)
    #         time.sleep(5)
    #     else:
    #         first_digit=gtin[0]
    #         item_ref=gtin[1:1+(12-len(gs1_prefix))]
    #         print(f"[{packaging_unit}] GTIN: {gtin}, Item Ref: {item_ref}")
    #         print
    #         Select(driver.find_elements(By.CSS_SELECTOR, "select.productpackagingunitindicator")[-1]).select_by_visible_text(first_digit)
    #         driver.execute_script("""
    #             arguments[0].value=arguments[1];
    #             arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
    #             arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
    #             arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
    #         """, driver.find_elements(By.CSS_SELECTOR, "input.productpackagingitemreference")[-1], item_ref)
    #
    #     Select(driver.find_elements(By.CSS_SELECTOR, "select.productpackagingunit")[-1]).select_by_visible_text(packaging_unit)
    #     time.sleep(5)

    # for i, row in df.iterrows():
    #     gtin = str(row.get("GTIN", "")).strip()
    #     sscc = str(row.get("SSCC Extension Digit(Loose Pack)", "")).strip()
    #     gs1_prefix = str(row.get("GS1 Company Prefix", "")).strip()
    #     packaging_unit = str(row.get("Packaging Level", "")).strip()
    #     items_in_level = str(row.get("No. of Items in this level", "")).strip()
    #
    #     if gtin == "-" or gtin == "":
    #         print(f"[{packaging_unit}] Using SSCC: {sscc}")
    #         Select(driver.find_elements(By.CSS_SELECTOR, "select.productpackagingunitcodetype")[
    #                    -1]).select_by_visible_text("SSCC")
    #         driver.execute_script("""
    #             arguments[0].value = arguments[1];
    #             arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
    #             arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
    #             arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
    #         """, driver.find_elements(By.CSS_SELECTOR, "input.productpackagingitemreference")[-1], "1234")
    #         Select(driver.find_elements(By.CSS_SELECTOR, "select.productpackagingunitindicator")[
    #                    -1]).select_by_visible_text(sscc)
    #     else:
    #         first_digit = gtin[0]
    #         item_ref = gtin[1:1 + (12 - len(gs1_prefix))]
    #         print(f"[{packaging_unit}] GTIN: {gtin}, Item Ref: {item_ref}")
    #         Select(driver.find_elements(By.CSS_SELECTOR, "select.productpackagingunitindicator")[
    #                    -1]).select_by_visible_text(first_digit)
    #         driver.execute_script("""
    #             arguments[0].value = arguments[1];
    #             arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
    #             arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
    #             arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
    #         """, driver.find_elements(By.CSS_SELECTOR, "input.productpackagingitemreference")[-1], item_ref)
    #
    #     Select(driver.find_elements(By.CSS_SELECTOR, "select.productpackagingunit")[-1]).select_by_visible_text(
    #         packaging_unit)
    #
    #     # Set No. of Items in this level from Excel
    #     driver.execute_script("""
    #         arguments[0].value = arguments[1];
    #         arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
    #         arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
    #         arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
    #     """, driver.find_elements(By.CSS_SELECTOR, "input.productpackagingintemslayers")[-1], items_in_level)
    #
    #
    #     if i<len(df) -1:
    #         driver.execute_script("arguments[0].click();", driver.find_element(By.ID, "addItemCase"))
    #         time.sleep(1)
    #
    # time.sleep(15)



# Save product
# Please avoid use of \ ' "