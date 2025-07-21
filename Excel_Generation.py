from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import pandas as pd
import re

chrome_options=Options()
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('ignore-ssl-errors')
chrome_options.add_argument('allow-insecure-localhost')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

service=Service(r"C:\Users\Shantanu\Downloads\chromedriver-win32\chromedriver.exe")
driver=webdriver.Chrome(service=service, options=chrome_options)
wait=WebDriverWait(driver, 15)

dp=pd.read_excel("Master data.xlsx", sheet_name='URLs', header=None)

serialization_url=dp.iloc[2, 0]
login_url=dp.iloc[0, 0]

print(serialization_url)

EXCEL_FILENAME="IP2.xlsx"

# def generate_excel(file_name=EXCEL_FILENAME):
#     columns=['ip', 'poid', 'teach', 'accepted', 'inprocess', 'rejected', 'damaged', 'specimen', 'sample', 'child', 'xml', 'ip2', 'regulatory', 'ip3', 'child2', 'xml2']
#
#     df=pd.DataFrame(columns=columns)
#
#     df.to_excel(file_name, index=False)
#
#     print(f"Excel file {file_name} generated with specified columns")
#
# def fill_excel(PO, file_name=EXCEL_FILENAME):
#     driver.get(serialization_url)
#
#     driver.find_element(By.LINK_TEXT, 'Production orders').click()
#
#     wait.until(EC.presence_of_element_located((By.ID, 'datacontent')))
#
#     row_xpath = f"//tr[td[normalize-space(text())='{PO}']]"
#     row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))
#
#     PO_overview_button = row.find_element(By.XPATH, ".//a[@title='Production order overview']")
#     driver.execute_script("arguments[0].click();", PO_overview_button)
#
#     time.sleep(5)
#
#     po_title_element=wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='bigtitle']")))
#
#     po_text=po_title_element.text.strip()
#     po_id=po_text.split("Production order:")[1].split()[0]
#
#     print(f"PO ID: {po_id}")
#
#     system_elements=driver.find_elements(By.XPATH, "//div[@class='systemname']")
#
#     ip_addresses=[]
#
#     for sys in system_elements:
#         text=sys.get_attribute("innerHTML").strip().replace("<br>", "\n")
#         lines=text.splitlines()
#         if len(lines)>1:
#             ip_addresses.append(lines[1].strip())
#
#     print(f"IP Addresses: {ip_addresses}")
#
#     # show_details=driver.find_element(By.CSS_SELECTOR, "span.detailsopened[onclick*='showTableDetails']")
#     show_details = driver.find_element(By.XPATH,"//span[contains(@onclick, 'showTableDetails') and contains(text(), 'Show details')]")
#     show_details.click()
#
#     regulation=driver.find_element(By.XPATH, "//td[b[text()='Regulation:']]/following-sibling::td[1]/input").get_attribute("value")
#
#     packaging_text=driver.find_element(By.XPATH, "//td[b[text()='Packaging version:']]/following-sibling::td[1]/input").get_attribute("value")
#
#     bracket_contents=re.findall(r'\((.*?)\)', packaging_text)
#
#     numbers=[]
#     for group in bracket_contents:
#         match=re.search(r'\d+', group)
#         if match:
#             numbers.append(int(match.group()))
#
#     child=numbers[0]
#     child2=numbers[1]
#
#     xml=1000/child
#     xml2=1000/child2
#
#
#     df=pd.read_excel(file_name)
#
#     teach=input("Enter Teach:")
#     accepted=input("Enter Accepted:")
#     inprocess=input("Enter Inprocess:")
#     rejected=input("Enter Rejected:")
#     damaged=input("Enter Damaged:")
#     specimen=input("Enter Specimen:")
#     sample=input("Enter Sample:")
#
#     new_row={
#         'poid': po_id,
#         'ip': ip_addresses[0] if len(ip_addresses)>0 else '',
#         'ip2': ip_addresses[1] if len(ip_addresses)>1 else '',
#         'ip3': ip_addresses[2] if len(ip_addresses)>2 else '',
#         'teach': teach,
#         'accepted': accepted,
#         'inprocess': inprocess,
#         'rejected': rejected,
#         'damaged': damaged,
#         'specimen': specimen,
#         'sample': sample,
#         'child': child,
#         'xml': xml,
#         'regulatory': regulation,
#         'child2': child2,
#         'xml2': xml2
#     }
#
#     df.loc[len(df)]=new_row
#     df.to_excel(file_name, index=False)
#
#     time.sleep(5)

def generate_excel(file_name=EXCEL_FILENAME, packaging_text=None):
    bracket_contents=re.findall(r'\((.*?)\)', packaging_text) if packaging_text else []
    num_levels=len(bracket_contents)

    columns=['ip', 'poid', 'teach', 'accepted', 'inprocess', 'rejected', 'damaged', 'specimen', 'sample']

    if num_levels>=1:
        columns.extend(['ip2', 'child', 'xml'])

    for i in range(1, num_levels):
        columns.extend([f'ip{i+2}', f'child{i+1}', f'xml{i+1}'])

    columns.append('regulatory')

    df=pd.DataFrame(columns=columns)

    df.to_excel(file_name, index=False)

    print(f"Excel file {file_name} generated with specified columns: {columns}")

def fill_excel(PO, file_name=EXCEL_FILENAME):
    driver.get(serialization_url)

    driver.find_element(By.LINK_TEXT, 'Production orders').click()

    wait.until(EC.presence_of_element_located((By.ID, 'datacontent')))

    row_xpath = f"//tr[td[normalize-space(text())='{PO}']]"
    row = wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

    PO_overview_button = row.find_element(By.XPATH, ".//a[@title='Production order overview']")
    driver.execute_script("arguments[0].click();", PO_overview_button)

    time.sleep(5)

    po_title_element=wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='bigtitle']")))

    po_text=po_title_element.text.strip()
    po_id=po_text.split("Production order:")[1].split()[0]

    print(f"PO ID: {po_id}")

    system_elements=driver.find_elements(By.XPATH, "//div[@class='systemname']")

    ip_addresses=[]

    for sys in system_elements:
        text=sys.get_attribute("innerHTML").strip().replace("<br>", "\n")
        lines=text.splitlines()
        if len(lines)>1:
            ip_addresses.append(lines[1].strip())

    print(f"IP Addresses: {ip_addresses}")

    # show_details=driver.find_element(By.CSS_SELECTOR, "span.detailsopened[onclick*='showTableDetails']")
    show_details = driver.find_element(By.XPATH,"//span[contains(@onclick, 'showTableDetails') and contains(text(), 'Show details')]")
    show_details.click()

    regulation=driver.find_element(By.XPATH, "//td[b[text()='Regulation:']]/following-sibling::td[1]/input").get_attribute("value")

    packaging_text=driver.find_element(By.XPATH, "//td[b[text()='Packaging version:']]/following-sibling::td[1]/input").get_attribute("value")

    bracket_contents=re.findall(r'\((.*?)\)', packaging_text)

    numbers=[]
    for group in bracket_contents:
        match=re.search(r'\d+', group)
        if match:
            numbers.append(int(match.group()))

    num_levels=len(numbers)

    generate_excel(EXCEL_FILENAME, packaging_text)

    df=pd.read_excel(file_name)

    teach=input("Enter Teach:")
    accepted=input("Enter Accepted:")
    inprocess=input("Enter Inprocess:")
    rejected=input("Enter Rejected:")
    damaged=input("Enter Damaged:")
    specimen=input("Enter Specimen:")
    sample=input("Enter Sample:")

    new_row={
        'poid': po_id,
        'teach': teach,
        'accepted': accepted,
        'inprocess': inprocess,
        'rejected': rejected,
        'damaged': damaged,
        'specimen': specimen,
        'sample': sample,
        'regulatory': regulation
    }

    new_row['ip']=ip_addresses[0] if len(ip_addresses)>0 else '';

    if num_levels>=1:
        new_row['child']=numbers[0]
        new_row['xml']=round(1000/numbers[0], 2)
        new_row['ip2']=ip_addresses[1] if len(ip_addresses)>1 else ''

    for i in range(1, num_levels):
        new_row[f'ip{i+2}']=ip_addresses[i+1] if len(ip_addresses)>i+1 else ''
        new_row[f'child{i+1}']=numbers[i]
        new_row[f'xml{i+1}']=round(1000/numbers[i], 2)

    for col in df.columns:
        if col not in new_row:
            new_row[col]=''


    df.loc[len(df)]=new_row
    df.to_excel(file_name, index=False)

    time.sleep(5)


driver.get(login_url)
wait.until(EC.visibility_of_element_located((By.NAME, "email"))).send_keys("shantanu")
driver.find_element(By.NAME, "password").send_keys("tnt1234")
driver.find_element(By.XPATH, "//input[@type='submit' and @value='Login']").click()

# generate_excel(EXCEL_FILENAME, "Item, Bundle (8 Item, 1 Layers), Shipper (2 Bundle, 1 Layers)")
fill_excel("14072025PO", EXCEL_FILENAME)