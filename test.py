import unittest
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

class Script_10_45(unittest.TestCase):
    def setUp(self):
        self.random = random.randint(1000, 9999)
        self.newsubject = f"Subject_{self.random}"

    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--remote-allow-origins=*")

        service = Service(r"C:\Users\Shantanu\Downloads\chromedriver-win32\chromedriver.exe")
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.driver.implicitly_wait(20)

        cls.wait = WebDriverWait(cls.driver, 20)
        cls.ANSI_RESET = "\033[0m"
        cls.ANSI_RED_BACKGROUND = "\033[41m"

    def test_01_open_browser(self):
        self.driver.get("https://172.16.70.109/")
        self.driver.maximize_window()

        self.driver.find_element(By.ID, "details-button").click()
        self.driver.find_element(By.ID, "proceed-link").click()

    def test_02_verify_login_and_app_version(self):
        print("\nTest 1: Verify Login functionality------------------------------------------------------------")

        self.driver.find_element(By.NAME, "email").send_keys("shantanu")
        self.driver.find_element(By.NAME, "password").send_keys("tnt1234")
        self.driver.find_element(By.XPATH, "//*[@id='loginhoder']/input").click()

        user = self.driver.find_element(By.XPATH, "//*[@id='header']/div[2]/div[1]").text
        if "Selenium Automation" in user:
            print(f"Test passed: {user} logged in")
        else:
            print(self.ANSI_RED_BACKGROUND + "Test failed: Login unsuccessful" + self.ANSI_RESET)

        print("\nTest 2: Verify Application name and version is displayed properly--------------------------")
        title = self.driver.title
        expected_title = "VeriShield SM300 v.1.2.10.45"

        if title.strip().lower() == expected_title.lower():
            print(f"Test passed: Application title verified: {title}")
        else:
            print(self.ANSI_RED_BACKGROUND + f"Test failed: Unexpected title: {title}" + self.ANSI_RESET)

    def test_03_verify_dashboard(self):
        print("\nTest 3: Verify Dashboard page is displayed ------------------------------------------")
        dashboard_present = self.driver.find_element(By.PARTIAL_LINK_TEXT, "Dashboard").is_displayed()
        self.assertTrue(dashboard_present, "Dashboard link not visible")
        print("✅ Dashboard present")

        ser = self.driver.find_element(By.XPATH, "//a[@href='/?link=serialization']").text.strip().lower()
        mas = self.driver.find_element(By.XPATH, "//a[@href='/?link=masterdata']").text.strip().lower()
        adm = self.driver.find_element(By.XPATH, "//a[@href='/?link=admins']").text.strip().lower()

        self.assertEqual(ser, "serialization")
        self.assertEqual(mas, "master data")
        self.assertEqual(adm, "administration")
        print("✅ Dashboard menu items verified")

    def test_04_verify_dashboard_content(self):
        print("\nTest 4: Validate Dashboard contents ------------------------------------------")
        ccount = 0

        # 4A - Verify all 3 module names
        expected_modules = {"serialization", "master data", "administration"}
        found_modules = {
            el.text.strip().lower()
            for el in self.driver.find_elements(By.XPATH, "//div[@class='menudiv']")
        }
        if expected_modules.issubset(found_modules):
            print("✅ Sub-Test 4A passed - Dashboard modules are present")
            ccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Sub-Test 4A failed" + self.ANSI_RESET)

        # 4B - Verify all 8 sub-tabs
        expected_tabs = {
            "reporting", "production orders", "request sscc information", "as2",
            "stock", "shipping orders", "reconciliation", "vrs"
        }
        found_tabs = {
            el.text.strip().lower()
            for el in self.driver.find_elements(By.XPATH, "//div[@class='datacontenttab']/a")
        }
        if expected_tabs.issubset(found_tabs):
            print("✅ Sub-Test 4B passed - Dashboard sub-tabs are proper")
            ccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Sub-Test 4B failed - Sub-tabs missing" + self.ANSI_RESET)

        # 4C - Verify header widgets
        expected_panes = {
            "local serial numbers pool", "central serial numbers pool",
            "tasks", "latest events"
        }
        found_panes = {
            el.text.strip().lower()
            for el in self.driver.find_elements(By.XPATH, "//div[@class='head linearbackground']")
        }
        if expected_panes.issubset(found_panes):
            print("✅ Sub-Test 4C passed - Dashboard headers are proper")
            ccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Sub-Test 4C failed - Headers missing" + self.ANSI_RESET)

        # 4D - Language icon check
        if self.driver.find_element(By.ID, "languageactive").is_displayed():
            print("✅ Sub-Test 4D passed - Language icon visible")
            ccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Sub-Test 4D failed - Language icon not found" + self.ANSI_RESET)

        # 4E - Logout icon check
        if self.driver.find_element(By.XPATH, "//i[@class='fa fa-sign-out']").is_displayed():
            print("✅ Sub-Test 4E passed - Logout icon visible")
            ccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Sub-Test 4E failed - Logout icon not found" + self.ANSI_RESET)

        if ccount == 5:
            print("✅ Test 4: All dashboard content checks passed")
        else:
            print(self.ANSI_RED_BACKGROUND + f"❌ Test 4 failed: {5 - ccount} checks failed" + self.ANSI_RESET)

    def test_05_verify_production_orders_page(self):
        print(
            "\nTest 5: Verify Production orders tab is proper or not-----------------------------------------------------------")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Production orders')]").click()
        time.sleep(5)
        poccount = 0

        print("Sub-Test 5A: Check if search filter is available")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[2]").is_displayed():
            print("✅ Passed")
            poccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 5B: Check if page sorter is available")
        if self.driver.find_element(By.ID, "productionorders_list_pages").is_displayed():
            print("✅ Passed")
            poccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 5C: Check if 'Import from Excel' icon is available")
        if self.driver.find_element(By.XPATH, "//i[@title='Import from Excel']").is_displayed():
            print("✅ Passed")
            poccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 5D: Check if 'New Production Order' icon is visible")
        if self.driver.find_element(By.XPATH, "//i[@title='New production order']").is_displayed():
            print("✅ Passed")
            poccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 5E: Verify table headers on PO window")
        poheaderlist = self.driver.find_elements(By.XPATH,
                                                 "/html/body/div[4]/div[2]/div[2]/div[4]/table[2]/thead/tr/th")
        expected_headers = [
            "Id", "PO order name / number", "Product", "Location", "Regulation",
            "Production date", "Requested", "Produced", "Created", "Status", "Actions"
        ]
        phlcount = 0
        for phl in poheaderlist:
            label = phl.get_attribute("aria-label")
            if any(header in label for header in expected_headers):
                phlcount += 1

        if phlcount == 11:
            print("✅ Passed")
            poccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Production Orders Page Check Completed with {poccount}/5 Passed Sub-tests")

    def test_06_verify_reporting_tab(self):
        print(
            "\nTest 6: Verify Reporting tab is proper or not-------------------------------------------------------------")
        self.driver.find_element(By.XPATH, "//a[contains(text(), 'Reporting')]").click()
        repcount = 0

        print("Sub-Test 6A: Check if 'Outgoing Messages' and 'Incoming Messages' tabs exist")
        om = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Outgoing Messages')]").is_displayed()
        inc = self.driver.find_element(By.XPATH, "//a[contains(text(), 'Incoming Messages')]").is_displayed()
        if om and inc:
            print("✅ Passed")
            repcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 6B: Check if MMMP filters are available")
        if self.driver.find_element(By.ID, "MMMPFilter").is_displayed():
            print("✅ Passed")
            repcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 6C: Check if 'Clear filters' icon is available")
        if self.driver.find_element(By.XPATH, "//i[@title='Clear filters']").is_displayed():
            print("✅ Passed")
            repcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 6D: Check if Auto-refresh toggle is available")
        if self.driver.find_element(By.ID, "autorefreshicon").is_displayed():
            print("✅ Passed")
            repcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 6E: Verify 'Messages' table and headers")
        is_messages_displayed = self.driver.find_element(By.XPATH, "//div[contains(text(),'Messages')]").is_displayed()
        meslist = self.driver.find_elements(By.XPATH, "//table[@id='emvslogs_messages_table']/thead/tr/th")
        expected_msg_headers = [
            "Hub", "Message type", "Product", "Batch",
            "PO Number", "Status", "Date and time", "Actions"
        ]
        mescount = 0
        for th in meslist:
            if th.text.strip() in expected_msg_headers:
                mescount += 1

        if is_messages_displayed and mescount == 8:
            print("✅ Passed")
            repcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Reporting Tab Check Completed with {repcount}/5 Passed Sub-tests")

    def test_07_verify_stock_page(self):
        print(
            "\nTest 7: To verify Stock tab is proper or not-----------------------------------------------------------")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Stock')]").click()
        time.sleep(2)
        stcount = 0

        print("Sub-Test 7A: Verify search filter on Stock window")
        if self.driver.find_element(By.XPATH, "//*[@id='stock_list_pages']/following-sibling::div[1]").is_displayed():
            print("✅ Passed")
            stcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 7B: Verify page sorter on Stock window")
        if self.driver.find_element(By.ID, "stock_list_pages").is_displayed():
            print("✅ Passed")
            stcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 7C: Verify reload icon on Stock window")
        if self.driver.find_element(By.XPATH, "//*[@id='stock_list_pages']/preceding-sibling::a/i").is_displayed():
            print("✅ Passed")
            stcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 7D: Verify table headers on Stock window")
        st_headers = self.driver.find_elements(By.XPATH, "//table[@id='stock_list_table-sticky']/thead/tr/th")
        expected_headers = [
            "Id", "Product", "Lot/Batch", "Standard", "Expiration date",
            "Produced", "Reserved", "Shipped", "Stock", "Actions"
        ]
        match_count = 0
        for th in st_headers:
            label = th.get_attribute("aria-label")
            if any(h in label for h in expected_headers):
                match_count += 1
        if match_count == 10:
            print("✅ Passed")
            stcount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Stock Page Check Completed with {stcount}/4 Passed Sub-tests")

    def test_08_verify_shipping_orders_page(self):
        print(
            "\nTest 8: To verify Shipping orders tab is proper or not-----------------------------------------------------------")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Shipping orders')]").click()
        time.sleep(2)
        soccount = 0

        print("Sub-Test 8A: Verify search filter on Shipping orders window")
        if self.driver.find_element(By.XPATH,
                                    "//div[@id='shippingorders_list_pages']/following-sibling::div[1]").is_displayed():
            print("✅ Passed")
            soccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 8B: Verify page sorter on Shipping orders window")
        if self.driver.find_element(By.ID, "shippingorders_list_pages").is_displayed():
            print("✅ Passed")
            soccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 8C: Verify reload icon on Shipping orders window")
        if self.driver.find_element(By.XPATH,
                                    "//div[@id='shippingorders_list_pages']/preceding-sibling::a[1]/i").is_displayed():
            print("✅ Passed")
            soccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 8D: Download consignment logs icon")
        print("❎ Not applicable")  # You already marked it so in your Java code

        print("Sub-Test 8E: Verify 'New Shipping Order' icon")
        if self.driver.find_element(By.XPATH, "//*[@title='New shipping order']").is_displayed():
            print("✅ Passed")
            soccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 8F: Verify table headers on Shipping orders window")
        so_headers = self.driver.find_elements(By.XPATH, "//table[@id='shippingorders_list_table-sticky']/thead/tr/th")
        expected_headers = [
            "Id", "Name", "Regulation", "Type", "Source location", "Destination location",
            "Date and time of shipment", "Qty.", "Agg.", "Created", "Status", "Actions"
        ]
        header_match_count = 0
        for th in so_headers:
            label = th.get_attribute("aria-label")
            if any(h in label for h in expected_headers):
                header_match_count += 1

        if header_match_count == 12:
            print("✅ Passed")
            soccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Shipping Orders Page Check Completed with {soccount}/5 Passed Sub-tests")

    def test_09_verify_company_details_page(self):
        print("\n" + "-" * 100)
        print("Validation of Master Data module")
        self.driver.find_element(By.XPATH, "//a[@href='/?link=masterdata']").click()
        time.sleep(2)

        print("\nTest 9: To verify Company details page")
        cdccount = 0

        print("Sub-Test 9A: Verify Company name, address, GCP and GLN fields are present")
        try:
            company_fields = [
                self.driver.find_element(By.XPATH, "//*[@id='editcompanyntinner']/div/table/tbody/tr/td/b"),
                self.driver.find_element(By.XPATH,
                                         "//div[@class='upperform']/table/tbody/tr/td[contains(text(),'Address: ')]"),
                self.driver.find_element(By.XPATH,
                                         "//div[@class='upperform']/table/tbody/tr/td[contains(text(),'City: ')]"),
                self.driver.find_element(By.XPATH,
                                         "//div[@class='upperform']/table/tbody/tr/td[contains(text(),'Zip: ')]"),
                self.driver.find_element(By.XPATH,
                                         "//div[@class='upperform']/table/tbody/tr/td[contains(text(),'State ')]"),
                self.driver.find_element(By.XPATH,
                                         "//div[@class='upperform']/table/tbody/tr/td[contains(text(),'Country: ')]"),
                self.driver.find_element(By.XPATH, "//*[@value='GS1 Company Prefix/GTIN Prefix']"),
                self.driver.find_element(By.XPATH, "//*[@value='GLN']")
            ]
            if all(field.is_displayed() for field in company_fields):
                print("✅ Passed")
                cdccount += 1
            else:
                print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)
        except Exception:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed - One or more fields not found" + self.ANSI_RESET)

        print("Sub-Test 9B: Verify sub-tabs are present in Company Details")
        expected_tabs = ["Properties", "CRPT settings", "ERP settings", "Trusted counterparties"]
        tabs = self.driver.find_elements(By.XPATH, "//*[@id='editcompanyntinner']/div[2]/ul/li/a")
        matched_tabs = [tab.text for tab in tabs if tab.text in expected_tabs]

        if len(matched_tabs) == 4:
            print("✅ Passed")
            cdccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Company Details Page Check Completed with {cdccount}/2 Passed Sub-tests")

    def test_10_click_products_tab(self):
        print("\nTest 10: Click the Products tab")
        pccount = 0

        try:
            # Directly click the Products tab — assuming you're still on the Master Data page
            products_tab = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[@id='datacontenttab_3']/a[contains(text(),'Products')]"))
            )
            products_tab.click()
            time.sleep(5)
            print("✅ Products tab clicked successfully")
        except Exception as e:
            print(f"❌ Failed to click Products tab: {str(e)}")

        print("Sub-Test 10A: Verify Search filter is available")
        try:
            if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/div[2]").is_displayed():
                print("✅ Passed")
                pccount += 1
            else:
                print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)
        except Exception:
            print(self.ANSI_RED_BACKGROUND + "❌ Search filter not found" + self.ANSI_RESET)

        print("Sub-Test 10B: Verify Page sorter is available")
        try:
            if self.driver.find_element(By.ID, "products_pages").is_displayed():
                print("✅ Passed")
                pccount += 1
            else:
                print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)
        except Exception:
            print(self.ANSI_RED_BACKGROUND + "❌ Page sorter not found" + self.ANSI_RESET)

        print("Sub-Test 10C: Verify Reload icon is available")
        try:
            if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[2]/a[2]/i").is_displayed():
                print("✅ Passed")
                pccount += 1
            else:
                print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)
        except Exception:
            print(self.ANSI_RED_BACKGROUND + "❌ Reload icon not found" + self.ANSI_RESET)

        print("Sub-Test 10D: Verify Import Products icon is available")


        try:
            if self.driver.find_element(By.ID, "importproductsbutton").is_displayed():
                print("✅ Passed")
                pccount += 1
            else:
                print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)
        except Exception:
            print(self.ANSI_RED_BACKGROUND + "❌ Import Products icon not found" + self.ANSI_RESET)

        print("Sub-Test 10E: Verify New Product icon is available")
        try:
            if self.driver.find_element(By.XPATH, "//*[@title='New product']").is_displayed():
                print("✅ Passed")
                pccount += 1
            else:
                print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)
        except Exception:
            print(self.ANSI_RED_BACKGROUND + "❌ New Product icon not found" + self.ANSI_RESET)

        print("Sub-Test 10F: Verify Table headers are correct")
        try:
            headers = self.driver.find_elements(By.XPATH, "//table[@id='products_table-sticky']/thead/tr/th")
            expected_headers = ["ID", "Product name", "Manufacturer", "Group", "Description", "Created", "Status",
                                "Actions"]
            match_count = 0
            for h in headers:
                label = h.get_attribute("aria-label")
                if any(eh in label for eh in expected_headers):
                    match_count += 1

            if match_count == 8:
                print("✅ Passed")
                pccount += 1
            else:
                print(self.ANSI_RED_BACKGROUND + "❌ Table headers mismatch" + self.ANSI_RESET)
        except Exception:
            print(self.ANSI_RED_BACKGROUND + "❌ Table headers not found" + self.ANSI_RESET)

        print(f"Products Page Check Completed with {pccount}/6 Passed Sub-tests")

    def test_11_verify_product_groups_page(self):
        print("\nTest 11: To verify Product groups page")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Product groups')]").click()
        time.sleep(2)
        pgccount = 0

        print("Sub-Test 11A: Verify search filter on Product Groups page")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[4]/div[2]").is_displayed():
            print("✅ Passed")
            pgccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 11B: Verify page sorter on Product Groups page")
        if self.driver.find_element(By.ID, "product_groups_pages").is_displayed():
            print("✅ Passed")
            pgccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 11C: Verify Reload icon on Product Groups page")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[4]/a[2]/i").is_displayed():
            print("✅ Passed")
            pgccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 11D: Verify table headers on Product Groups page")
        headers = self.driver.find_elements(By.XPATH, "//table[@id='product_groups_table']/thead/tr/th")
        expected_headers = ["ID", "Product group", "Created", "Actions"]
        match_count = 0
        for h in headers:
            label = h.get_attribute("aria-label")
            if any(eh in label for eh in expected_headers):
                match_count += 1
        if match_count == 4:
            print("✅ Passed")
            pgccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 11E: Verify New Product Group icon")
        if self.driver.find_element(By.XPATH, "//*[@title='New product group']").is_displayed():
            print("✅ Passed")
            pgccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Product Groups Page Check Completed with {pgccount}/5 Passed Sub-tests")

    def test_12_verify_subjects_page(self):
        print("\nTest 12: To verify Subjects page")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Subjects')]").click()
        time.sleep(2)
        subjccount = 0

        print("Sub-Test 12A: Verify search filter on Subjects page")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[6]/div[2]").is_displayed():
            print("✅ Passed")
            subjccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 12B: Verify page sorter on Subjects page")
        if self.driver.find_element(By.ID, "subjects_list_pages").is_displayed():
            print("✅ Passed")
            subjccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 12C: Verify reload icon on Subjects page")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[6]/a[2]/i").is_displayed():
            print("✅ Passed")
            subjccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 12D: Verify table headers on Subjects page")
        headers = self.driver.find_elements(By.XPATH, "//table[@id='subjects_list_table-sticky']/thead/tr/th")
        expected = [
            "ID", "Name", "GS1 company prefix", "Group", "Description",
            "Created", "Status", "Actions"
        ]
        match = sum(1 for h in headers if any(e in h.get_attribute("aria-label") for e in expected))
        if match == 8:
            print("✅ Passed")
            subjccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 12E: Verify New Subject icon on Subjects page")
        if self.driver.find_element(By.XPATH, "//*[@title='New subject']").is_displayed():
            print("✅ Passed")
            subjccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Subjects Page Check Completed with {subjccount}/5 Passed Sub-tests")

    def test_13_verify_locations_page(self):
        print("\nTest 13: To verify Locations page")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Locations')]").click()
        time.sleep(2)
        locccount = 0

        print("Sub-Test 13A: Verify search filter on Locations page")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[8]/div[2]").is_displayed():
            print("✅ Passed")
            locccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 13B: Verify page sorter on Locations page")
        if self.driver.find_element(By.ID, "locations_list_pages").is_displayed():
            print("✅ Passed")
            locccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 13C: Verify reload icon on Locations page")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[8]/a[2]/i").is_displayed():
            print("✅ Passed")
            locccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 13D: Verify table headers on Locations page")
        headers = self.driver.find_elements(By.XPATH, "//table[@id='locations_list_table']/thead/tr/th")
        expected = [
            "ID", "Name", "Subject", "GLN", "Description", "Address",
            "City", "Country", "Created", "Actions"
        ]
        match = sum(1 for h in headers if any(e in h.get_attribute("aria-label") for e in expected))
        if match == 10:
            print("✅ Passed")
            locccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 13E: Verify New Location icon")
        if self.driver.find_element(By.XPATH, "//*[@title='New location']").is_displayed():
            print("✅ Passed")
            locccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Locations Page Check Completed with {locccount}/5 Passed Sub-tests")

    def test_14_verify_users_tab(self):
        print(
            "\n-----------------------------*********************************************************************----------------------")
        print("Validation of Administration module")
        self.driver.find_element(By.XPATH, "//a[@href='/?link=admins']").click()
        time.sleep(2)

        print("\nTest 14: To verify Users tab")
        usersccount = 0

        print("Sub-Test 14A: Verify search filter on Users page")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[1]/div[2]").is_displayed():
            print("✅ Passed")
            usersccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 14B: Verify page sorter on Users page")
        if self.driver.find_element(By.ID, "admins_list_pages").is_displayed():
            print("✅ Passed")
            usersccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        # print("Sub-Test 14C: Verify Synchronize with LDAP icon")
        # if self.driver.find_element(By.XPATH, "//*[@title='Synchronize with LDAP']").is_displayed():
        #     print("✅ Passed")
        #     usersccount += 1
        # else:
        #     print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 14D: Verify Print icon on Users page")
        if self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[1]/a[1]/i").is_displayed():
            print("✅ Passed")
            usersccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 14E: Verify table headers on Users page")
        headers = self.driver.find_elements(By.XPATH, "//table[@id='admins_list_table-sticky']/thead/tr/th")
        expected = [
            "Lastname, Firstname", "Username", "E-mail", "Logged In", "Machine Name",
            "User Status", "Login Status", "Role", "Updated Date", "Creation Date", "Actions"
        ]
        matched = sum(1 for h in headers if any(e in h.get_attribute("aria-label") for e in expected))
        if matched == 11:
            print("✅ Passed")
            usersccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 14F: Verify New user icon")
        if self.driver.find_element(By.XPATH, "//*[@title='New user']").is_displayed():
            print("✅ Passed")
            usersccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Users Tab Check Completed with {usersccount}/6 Passed Sub-tests")

    def test_15_verify_roles_tab(self):
        print("\nTest 15: To verify Roles tab")
        self.driver.find_element(By.XPATH, "//*[contains(text(),'Roles')]").click()
        time.sleep(3)
        roleccount = 0

        print("Sub-Test 15A: Verify search filter on Roles page")
        if self.driver.find_element(By.XPATH, "//*[@id='roles_list_pages']/following-sibling::div[1]").is_displayed():
            print("✅ Passed")
            roleccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 15B: Verify page sorter on Roles page")
        if self.driver.find_element(By.ID, "admins_list_pages").is_displayed():
            print("✅ Passed")
            roleccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 15C: Verify table headers on Roles page")
        headers = self.driver.find_elements(By.XPATH, "//table[@id='roles_list_table-sticky']/thead/tr/th")
        expected = ["Role title", "Actions"]
        matched = sum(1 for h in headers if any(e in h.get_attribute("aria-label") for e in expected))
        if matched == 2:
            print("✅ Passed")
            roleccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 15D: Verify New Role icon")
        if self.driver.find_element(By.XPATH, "//*[@title='New role']").is_displayed():
            print("✅ Passed")
            roleccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Roles Tab Check Completed with {roleccount}/4 Passed Sub-tests")

    def test_16_verify_audit_trail_tab(self):
        print("\nTest 16: To verify Audit trail tab")
        self.driver.find_element(By.XPATH, "//*[contains(text(),'Audit trail')]").click()
        time.sleep(4)

        atccount = 0

        print("Sub-Test 16A: Verify page sorter on Audit trail page")
        if self.driver.find_element(By.XPATH, "//*[@id='audits_list_pages']").is_displayed():
            print("✅ Passed")
            atccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 16B: Verify table headers on Audit trail page")
        headers = self.driver.find_elements(By.XPATH, "//table[@id='audits_list_table']/thead/tr/th")
        expected = ["Date and time", "Event", "User", "Message", "Details"]
        matched = sum(1 for h in headers if any(e in h.text for e in expected))
        if matched == 5:
            print("✅ Passed")
            atccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        # print("Sub-Test 16C: Verify Export to Excel icon")
        # if self.driver.find_element(By.XPATH, "//*[@title='Export to Excel']").is_displayed():
        #     print("✅ Passed")
        #     atccount += 1
        # else:
        #     print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 16D: Verify Reload icon")
        if self.driver.find_element(By.XPATH, "//*[@id='audits_list_pages']/preceding-sibling::a[1]/i").is_displayed():
            print("✅ Passed")
            atccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 16E: Verify Print icon")
        # if self.driver.find_element(By.XPATH, "//*[@id='audits_list_pages']/preceding-sibling::a[3]/i").is_displayed():
        #     print("✅ Passed")
        #     atccount += 1
        # else:
        #     print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Audit Trail Tab Completed with {atccount}/5 Passed Sub-tests")

    def test_17_verify_serial_number_providers_tab(self):
        print("\nTest 17: To verify Serial Number Providers tab")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Serial numbers providers')]").click()
        time.sleep(3)

        snpccount = 0

        print("Sub-Test 17A: Page sorter availability")
        if self.driver.find_element(By.XPATH, "//*[@id='sngproviders_list_pages']").is_displayed():
            print("✅ Passed")
            snpccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 17B: Table headers validation")
        headers = self.driver.find_elements(By.XPATH, "//table[@id='sngproviders_list_table-sticky']/thead/tr/th")
        expected = ["Title", "Actions"]
        match = sum(1 for h in headers if any(e in h.get_attribute("aria-label") for e in expected))
        if match == 2:  # NOTE: In your Java code it says == 11, but only 2 headers are being checked.
            print("✅ Passed")
            snpccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 17C: Search option availability")
        if self.driver.find_element(By.XPATH,
                                    "//div[@id='sngproviders_list_pages']/following-sibling::div[1]").is_displayed():
            print("✅ Passed")
            snpccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 17D: Add provider icon availability")
        if self.driver.find_element(By.XPATH,
                                    "//div[@id='sngproviders_list_pages']/following-sibling::div[2]").is_displayed():
            print("✅ Passed")
            snpccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 17E: Cron job status icon availability")
        if self.driver.find_element(By.XPATH, "//i[@id='cronjobicon']").is_displayed():
            print("✅ Passed")
            snpccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"Serial Number Providers Tab: {snpccount}/5 Passed")

    def test_18_verify_cmo_integration_tab(self):
        print("\nTest 18: To verify CMO Integration tab")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'CMO Integration')]").click()
        time.sleep(3)

        ciccount = 0

        print("Sub-Test 18A: Page sorter availability")
        if self.driver.find_element(By.XPATH, "//*[@id='cmointegration_list_pages']").is_displayed():
            print("✅ Passed")
            ciccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 18B: Table headers validation")
        headers = self.driver.find_elements(By.XPATH, "//table[@id='cmointegration_list_table']/thead/tr/th")
        expected = ["Title", "Actions"]
        match = sum(1 for h in headers if any(e in h.get_attribute("aria-label") for e in expected))
        if match == 2:
            print("✅ Passed")
            ciccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 18C: Search option availability")
        if self.driver.find_element(By.XPATH,
                                    "//div[@id='cmointegration_list_pages']/following-sibling::div[1]").is_displayed():
            print("✅ Passed")
            ciccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 18D: Reload icon availability")
        if self.driver.find_element(By.XPATH,
                                    "//div[@id='cmointegration_list_pages']/preceding-sibling::a[1]/i").is_displayed():
            print("✅ Passed")
            ciccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print("Sub-Test 18E: New FTP Destination icon availability")
        if self.driver.find_element(By.XPATH,
                                    "//div[@id='cmointegration_list_pages']/preceding-sibling::a[2]/i").is_displayed():
            print("✅ Passed")
            ciccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed" + self.ANSI_RESET)

        print(f"CMO Integration Tab: {ciccount}/5 Passed")

    def test_19_verify_settings_page(self):
        print("\nTest 19: To verify Settings tab")
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Settings')]").click()
        time.sleep(3)

        sccount = 0
        expected_settings = [
            "maximum allowed quantity for production order item", "session timeout in minutes",
            "allow login from multiple machines (0 - No, 1 - Yes)", "siteID (0-SNG, 1,2,3... site number)",
            "API_URL", "CLIENT_URL", "APP_URL", "CERT_URL", "PIC_URL", "ROOT", "CLIENTROOT", "APIROOT",
            "Minimum password length", "Lockout attempts", "Password expiry", "Password complexity",
            "Username type", "password_expiry_notification_days",
            "External serial numbers providers minimum_quantity (max value)",
            "External serial numbers providers renewal_quantity (max value)",
            "GTIN is unique across products (0 - No, 1 - Yes)",
            "Allow same product name across products (0 - No, 1 - Yes)",
            "Maximum serial numbers download attempts", "Serial numbers download interval in minutes",
            "use quarantine status for production order (0 - No, 1 - Yes)",
            "Allow same lot number for different products (0 - No, 1 - Yes)",
            "Is Manufacturing Date mandatory? (0 - no,1 - yes)", "Verishield Proxy Server URL",
            "Proxy Server Alias Id", "Date Formats", "Product fetch from FG Code(SAP)(0 - No,1 -Yes)",
            "VRS add email list max count", "Validate password for last used? 0-N0, 1-Yes",
            "Provision to download the consignment XML", "Automatically Download Reporting Message?",
            "Export audittrial to excel? (0 - no,1 - yes)",
            "Is serial numbers to be discarded? (0-> No, 1-> Yes)",
            "Allow users to run Multiple Production Order on same machine ? (0-> Yes, 1-> No)",
            "Allow user to select past date for production date in production order? (0-> Yes, 1-> No)",
            "Display option to select request/response format (PURE URI ID) for Rfxcel (1=>Display, 0=>Hide)",
            "Allow a production order to be internally transferred (1=>YES,0=>NO)",
            "Allow sending ASN 856 Message File (1=>YES, 0=>NO)",
            "Display option to select SFTP based request/response format for tracelink (1=>Display, 0=>Hide)",
            "Enable Force Password Change (1=>YES, 0=>NO)", "Enable contact details in subject (1=>YES,0=>NO)",
            "Enable Default Filter Value (1=>YES, 0=>NO)", "Enable Default subject Value (1=>YES, 0=>NO)"
        ]

        self.driver.find_element(By.XPATH, "//*[@id=\"datacontenttab_7\"]/a").click()
        time.sleep(2)

        settings_elements = self.driver.find_elements(By.XPATH,
                                                      "//div[@id='datacontentinner_tab_7']/div/table/tbody/tr/td[1]")
        found_settings = [el.text.strip() for el in settings_elements]

        matches = sum(1 for setting in expected_settings if setting in found_settings)

        if matches == len(expected_settings):
            print("✅ Passed: All expected settings found.")
            sccount += 1
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Failed: Some settings are missing." + self.ANSI_RESET)

        print(f"Settings Tab: {sccount}/1 Passed")

    # def test_20_verify_adding_subject(self):
    #     print("\nTest 20: Verify adding a subject")
    #
    #     self.driver.find_element(By.XPATH, "//a[@href='/?link=masterdata']").click()
    #     self.driver.find_element(By.XPATH, "//a[@href='javascript:subjectsList(1)']").click()
    #
    #     earlier_gcp = self.driver.find_element(By.XPATH, "//table[@id='subjects_list_table']/tbody/tr/td[3]").text
    #     gcpn = int(earlier_gcp) + 1
    #     gcp = str(gcpn)
    #     GLN_for_subject = self.getGLN(gcp)
    #
    #     self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[6]/a[1]/i").click()
    #     random_number = random.randint(1, 100)
    #     subject_name = f"Test_Subject_{random_number}"
    #     # self.newsubject = subject_name
    #     self.__class__.newsubject = subject_name
    #
    #     print(self.newsubject)
    #
    #     self.driver.find_element(By.ID, "subjectname").send_keys(subject_name)
    #     Select(self.driver.find_element(By.ID, "subjectgroup_id")).select_by_visible_text("Manufacturer")
    #     self.driver.find_element(By.XPATH, "//input[@class='certtitle subjectpropertyvalue  numeric']").send_keys(gcp)
    #     self.driver.find_element(By.XPATH,
    #                              "//input[@id='property_28' and @class='certtitle subjectpropertyvalue ']").send_keys(
    #         GLN_for_subject)
    #     self.driver.find_element(By.ID, "savesubjectbutton").click()
    #     time.sleep(3)
    #
    #     self.driver.find_element(By.XPATH, "/html/body/div[11]/div[3]/div[1]/button[2]").click()
    #
    #     WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located((By.XPATH, "/html/body/div[11]/div[3]/div[1]/button[2]/span"))
    #     ).click()
    #
    #     time.sleep(10)
    #     self.driver.find_element(By.XPATH, "//div[@class='ui-dialog-buttonset']/button").click()
    #     time.sleep(10)
    #
    #     table = self.driver.find_element(By.XPATH, "//table[@id='subjects_list_table']")
    #     newsubject = table.find_elements(By.XPATH, ".//tr")[1].find_elements(By.XPATH, ".//td")[1].text
    #
    #     subjectwait = WebDriverWait(self.driver, 10)
    #     subjectwait.until(EC.visibility_of_element_located(
    #         (By.XPATH, "//*[@id='subjects_list_table']/tbody/tr[1]/td[8]/a[@title='Activate subject']"))).click()
    #     subjectwait.until(
    #         EC.visibility_of_element_located((By.XPATH, "/html/body/div[11]/div[3]/div[1]/button[2]/span"))).click()
    #
    #     if newsubject.lower() == subject_name.lower():
    #         print(f"✅ Test 20 Passed - Subject '{subject_name}' added successfully")
    #     else:
    #         print(self.ANSI_RED_BACKGROUND + "❌ Test 20 Failed - Subject not added correctly" + self.ANSI_RESET)

    def test_20_verify_adding_subject(self):
        print("\nTest 20: Verify adding a subject")

        self.driver.find_element(By.XPATH, "//a[@href='/?link=masterdata']").click()
        self.driver.find_element(By.XPATH, "//a[@href='javascript:subjectsList(1)']").click()

        earlier_gcp = self.driver.find_element(By.XPATH, "//table[@id='subjects_list_table']/tbody/tr/td[3]").text
        gcpn = int(earlier_gcp) + 1
        gcp = str(gcpn)
        GLN_for_subject = self.getGLN(gcp)

        self.driver.find_element(By.XPATH, "/html/body/div[4]/div[2]/div[6]/a[1]/i").click()
        random_number = random.randint(1, 100)
        subject_name = f"Test_Subject_{random_number}"
        # self.newsubject = subject_name

        self.__class__.newsubject = subject_name  # ✅ stores it at the class level

        print(self.__class__.newsubject)

        self.driver.find_element(By.ID, "subjectname").send_keys(subject_name)
        Select(self.driver.find_element(By.ID, "subjectgroup_id")).select_by_visible_text("Manufacturer")
        self.driver.find_element(By.XPATH, "//input[@class='certtitle subjectpropertyvalue  numeric']").send_keys(gcp)
        self.driver.find_element(By.XPATH,
                                 "//input[@id='property_28' and @class='certtitle subjectpropertyvalue ']").send_keys(
            GLN_for_subject)
        self.driver.find_element(By.ID, "savesubjectbutton").click()
        time.sleep(3)

        self.driver.find_element(By.XPATH, "/html/body/div[11]/div[3]/div[1]/button[2]").click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[11]/div[3]/div[1]/button[2]/span"))
        ).click()

        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located((By.ID, "ajaxloaderover"))
        )

        row_xpath = f"//tr[td[normalize-space(text())='{self.__class__.newsubject}']]"
        row = self.wait.until(EC.presence_of_element_located((By.XPATH, row_xpath)))

        activate_button = row.find_element(By.XPATH, ".//a[contains(@href, 'activateSubject')]")
        self.driver.execute_script("arguments[0].click();", activate_button)

        # WebDriverWait(self.driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, "(//a[contains(@title, 'Activate subject')])[1]"))
        # ).click()

        ok_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space(.)='OK']")))
        ok_button.click()

        # time.sleep(10)
        # self.driver.find_element(By.XPATH, "//div[@class='ui-dialog-buttonset']/button").click()
        # time.sleep(10)

        # table = self.driver.find_element(By.XPATH, "//table[@id='subjects_list_table']")
        # newsubject = table.find_elements(By.XPATH, ".//tr")[1].find_elements(By.XPATH, ".//td")[1].text
        #
        # subjectwait = WebDriverWait(self.driver, 10)
        # subjectwait.until(EC.visibility_of_element_located(
        #     (By.XPATH, "//*[@id='subjects_list_table']/tbody/tr[1]/td[8]/a[@title='Activate subject']"))).click()
        # subjectwait.until(
        #     EC.visibility_of_element_located((By.XPATH, "/html/body/div[11]/div[3]/div[1]/button[2]/span"))).click()
        #
        # if newsubject.lower() == subject_name.lower():
        #     print(f"✅ Test 20 Passed - Subject '{subject_name}' added successfully")
        # else:
        #     print(self.ANSI_RED_BACKGROUND + "❌ Test 20 Failed - Subject not added correctly" + self.ANSI_RESET)

    def test_21_verify_adding_product(self):
        print("\nTest 21: Verify addition of product")
        time.sleep(2)

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//a[@href='/?link=masterdata']"))
        ).click()

        self.driver.find_element(By.XPATH, "//*[@id='datacontenttab_3']/a").click()
        self.driver.find_element(By.XPATH, "//i[@title='New product']").click()

        product_name = f"Product_test_{self.random}"
        self.driver.find_element(By.ID, "product_name").send_keys(product_name)

        Select(self.driver.find_element(By.ID, "manufacturer_id")).select_by_visible_text(self.__class__.newsubject)
        print(self.newsubject)

        self.driver.find_element(By.XPATH, "//a[contains(text(),'Product packaging')]").click()
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Switch to advanced mode')]").click()
        self.driver.find_element(By.XPATH, "//img[@src='/img/add.png']").click()
        self.driver.find_element(By.XPATH, "//img[@src='/img/add.png']").click()

        # Packaging levels
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[3]/td[3]/select")).select_by_visible_text(
            "Item")
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[5]/td[3]/select")).select_by_visible_text(
            "Shipper")
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[7]/td[3]/select")).select_by_visible_text(
            "Palette")

        # Unit code type
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[3]/td[4]/select")).select_by_visible_text(
            "GTIN")
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[5]/td[4]/select")).select_by_visible_text(
            "GTIN")
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[7]/td[4]/select")).select_by_visible_text(
            "SSCC")

        # Indicators
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[3]/td[5]/select")).select_by_visible_text(
            "0")
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[5]/td[5]/select")).select_by_visible_text(
            "1")
        Select(self.driver.find_element(By.XPATH,
                                        "//*[@id='productpackaging_table']/tbody/tr[7]/td[5]/select")).select_by_visible_text(
            "2")

        # GTINs
        for row in [3, 5, 7]:
            self.driver.find_element(By.XPATH,
                                     f"//*[@id='productpackaging_table']/tbody/tr[{row}]/td[6]/input").send_keys(
                "12345")

        # Content count
        self.driver.find_element(By.XPATH, "//*[@id='productpackaging_table']/tbody/tr[3]/td[7]/input").send_keys(
            "1")

        # Quantity per next level
        self.driver.find_element(By.XPATH, "//*[@id='productpackaging_table']/tbody/tr[3]/td[8]/input").send_keys(
            "1")
        self.driver.find_element(By.XPATH, "//*[@id='productpackaging_table']/tbody/tr[5]/td[8]/input").send_keys(
            "4")
        self.driver.find_element(By.XPATH, "//*[@id='productpackaging_table']/tbody/tr[7]/td[8]/input").send_keys(
            "2")

        # Save
        self.driver.find_element(By.ID, "saveproductbutton").click()
        self.driver.find_element(By.XPATH, "//div[@class='ui-dialog-buttonset']/button[2]").click()
        time.sleep(10)

        latest_product_name = self.driver.find_element(By.XPATH,
                                                       "//table[@id='products_table']/tbody/tr[1]/td[2]").text

        if latest_product_name.lower() == product_name.lower():
            print(f"✅ Test 21 Passed: Product '{product_name}' added successfully")
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Test 21 Failed: Product addition failed" + self.ANSI_RESET)

    # def test_22_verify_adding_location(self):
    #     print("\nTest 22: Verify adding of Location")
    #
    #     self.driver.find_element(By.XPATH, "//a[contains(text(),'Locations')]").click()
    #     self.driver.find_element(By.XPATH, "//i[@title='New location']").click()
    #
    #     location_name = f"Test_Location_{self.random}"
    #     self.driver.find_element(By.ID, "location_name").send_keys(location_name)
    #
    #     # Select(self.driver.find_element(By.ID, "location_subject_id")).select_by_visible_text(self.__class__.newsubject)
    #     Select(self.driver.find_element(By.ID, "location_subject_id")).select_by_visible_text(self.__class__.newsubject)
    #     print(self.newsubject)
    #     Select(self.driver.find_element(By.ID, "location_country")).select_by_visible_text("India")
    #
    #     GLN_for_location = self.GLN_for_subject.replace(self.gcp, "")
    #     self.driver.find_element(By.XPATH, "//table[@id='locationproperties_table']/tbody/tr[6]/td[2]/input").send_keys(
    #         GLN_for_location)
    #
    #     self.driver.find_element(By.ID, "savelocationbutton").click()
    #
    #     WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located((
    #             By.XPATH,
    #             "//span[contains(text(),'Save location')]/ancestor::div/div[3]/div/button/span[contains(text(),'OK')]"
    #         ))
    #     ).click()
    #
    #     time.sleep(5)
    #     actual_location_name = self.driver.find_element(By.XPATH,
    #                                                     "//table[@id='locations_list_table']/tbody/tr[1]/td[2]").text
    #
    #     if actual_location_name == location_name:
    #         print(f"✅ Test 22 Passed: Location '{location_name}' added successfully")
    #     else:
    #         print(self.ANSI_RED_BACKGROUND + "❌ Test 22 Failed: Location addition failed" + self.ANSI_RESET)

    # def test_22_verify_adding_location(self):
    #     print("\nTest 22: Verify adding of Location")
    #
    #     self.driver.find_element(By.XPATH, "//a[contains(text(),'Locations')]").click()
    #     self.driver.find_element(By.XPATH, "//i[@title='New location']").click()
    #
    #     location_name = f"Test_Location_{self.random}"
    #     self.driver.find_element(By.ID, "location_name").send_keys(location_name)
    #
    #     # Select(self.driver.find_element(By.ID, "location_subject_id")).select_by_visible_text(self.newsubject)
    #     Select(self.driver.find_element(By.ID, "location_subject_id")).select_by_visible_text(self.__class__.newsubject)
    #     print(self.newsubject)
    #     Select(self.driver.find_element(By.ID, "location_country")).select_by_visible_text("India")
    #
    #     GLN_for_location = self.GLN_for_subject.replace(self.gcp, "")
    #     self.driver.find_element(By.XPATH, "//table[@id='locationproperties_table']/tbody/tr[6]/td[2]/input").send_keys(
    #         GLN_for_location)
    #
    #     self.driver.find_element(By.ID, "savelocationbutton").click()
    #
    #     WebDriverWait(self.driver, 10).until(
    #         EC.visibility_of_element_located((
    #             By.XPATH,
    #             "//span[contains(text(),'Save location')]/ancestor::div/div[3]/div/button/span[contains(text(),'OK')]"
    #         ))
    #     ).click()
    #
    #     time.sleep(5)
    #     actual_location_name = self.driver.find_element(By.XPATH,
    #                                                     "//table[@id='locations_list_table']/tbody/tr[1]/td[2]").text
    #
    #     if actual_location_name == location_name:
    #         print(f"✅ Test 22 Passed: Location '{location_name}' added successfully")
    #     else:
    #         print(self.ANSI_RED_BACKGROUND + "❌ Test 22 Failed: Location addition failed" + self.ANSI_RESET)

    def test_22_verify_adding_location(self):
        print("\nTest 22: Verify adding of Location")

        self.driver.find_element(By.XPATH, "//a[contains(text(),'Locations')]").click()
        self.driver.find_element(By.XPATH, "//i[@title='New location']").click()

        location_name = f"Test_Location_{self.random}"
        self.driver.find_element(By.ID, "location_name").send_keys(location_name)

        # Select(self.driver.find_element(By.ID, "location_subject_id")).select_by_visible_text(self.newsubject)
        Select(self.driver.find_element(By.ID, "location_subject_id")).select_by_visible_text(self.__class__.newsubject)
        print(self.newsubject)
        Select(self.driver.find_element(By.ID, "location_country")).select_by_visible_text("India")

        gln_location_field = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[@flag='gln' and contains(@class, 'locationpropertyvalue')]")))

        existing_value = gln_location_field.get_attribute("value").strip()

        GLN_for_location = self.generate_full_gln(existing_value)
        print("✅ Final GLN:", GLN_for_location)

        self.driver.execute_script("""
                arguments[0].value=arguments[1],
                arguments[0].dispatchEvent(new Event('input', {bubbles: true}));
                arguments[0].dispatchEvent(new Event('change', {bubbles: true}));
                arguments[0].dispatchEvent(new Event('blur', {bubbles: true}));
        """, gln_location_field, GLN_for_location)

        self.driver.find_element(By.ID, "savelocationbutton").click()

        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((
                By.XPATH,
                "//span[contains(text(),'Save location')]/ancestor::div/div[3]/div/button/span[contains(text(),'OK')]"
            ))
        ).click()

        time.sleep(5)
        actual_location_name = self.driver.find_element(By.XPATH,
                                                        "//table[@id='locations_list_table']/tbody/tr[1]/td[2]").text

        if actual_location_name == location_name:
            print(f"✅ Test 22 Passed: Location '{location_name}' added successfully")
        else:
            print(self.ANSI_RED_BACKGROUND + "❌ Test 22 Failed: Location addition failed" + self.ANSI_RESET)



    def test_23_verify_user_permissions(self):
        print("\nTest 23: To verify all the required user permissions are present and in proper sequence")

        self.driver.find_element(By.XPATH, "//a[@href='/?link=admins']").click()
        self.driver.find_element(By.XPATH, "//a[contains(text(),'Roles')]").click()
        self.driver.find_element(By.XPATH, "//i[@title='New role']").click()
        self.driver.find_element(By.XPATH, "//a[contains(text(),'User permissions')]").click()

        expected_permissions = [
            "Get production orders list", "Get production order's items", "Edit production order", "Batch Repack",
            "Delete production order", "Send production order to production", "Download production order codes",
            "Download aggregated production order codes", "Import production order serial numbers",
            "Aggregate production order codes", "Finalize production order",
            "Create shipping order from production order",
            "Get production order issues", "Edit production order issue", "Send production order issue to production",
            "Download production order issue codes", "Delete production order issue", "Reopen production order",
            "Get production orders codes aggregated", "Deaggregate production order codes",
            "Decommison production order codes", "Get production orders statuses", "Recall batch", "Damage batch",
            "Import production orders", "Production order calculator", "Prepare product pack data for EMVS",
            "Get stock list", "Get stock items", "Get shipping orders list", "Edit shipping order",
            "Delete shipping order",
            "Delete shipping order's item", "Shipping Orders aggregate codes", "Ship shipping order",
            "Get shipping orders types", "Get standards", "Download shipping order codes", "Process shipping order",
            "Cancel shipping order", "Download shipping order codes with excluded codes", "Get products list",
            "Save product", "Delete product", "Get product properites", "Get product units", "Get product stock",
            "Get products groups list", "Save products group", "Delete products group",
            "Get product packaging versions",
            "Delete product packaging version", "Activate product", "Get subjects list", "Edit subject",
            "Delete subject",
            "Get subject properites", "Get subject locations", "Get subjects groups list", "Activate subject",
            "Get locations", "Edit location", "Delete location", "Get location properties", "Get production lines",
            "Edit production line", "Delete production line", "Get location line properties", "Get line systems",
            "Get systems", "Edit system", "Get application identifiers", "Get special fields list",
            "Get Standards List",
            "Get serial numbers templates list", "Get serialization events", "Get serialization event XML",
            "Get latest events", "Get Regulatory PRN's/Delete PRN", "Get code statuses",
            "Get product info certificates list",
            "Get product info certificate details", "Insert product info", "Delete product info certificate",
            "Get product info users", "Get certificate users", "Download certificates codes", "Get certificates codes",
            "Get notifications list", "Get notification details", "Save notification", "Delete notification",
            "Notifications users", "Acivate notification", "List end users", "Get special mobile users",
            "Insert special user", "Delete mobile user", "Get mobile user certificates", "Reports - scans per month",
            "Reports - scans per country", "Reports - scans per gender", "Reports - scans per age", "Get events list",
            "Get users list", "Edit user", "Activate/Deactivate User.", "Get user roles types", "Get roles",
            "Edit role",
            "Delete role", "Get audits", "Get audit details", "Get settings", "Update settings",
            "Get general record statuses", "Take Backup", "Get machine permissions", "Get FTP destinations",
            "Get FTP destination details", "Save FTP destination", "Log FTP upload",
            "Save serial numbers provider settings",
            "Get external serials pools", "Edit external serials pool", "Delete external serials pool",
            "Get external serials pools for providers MAH", "Edit external serials pool for providers MAH",
            "Edit connection owner name - serial number provider", "Re-upload of rfXcel event files",
            "Edit digital signature settings", "View company details", "Edit company details", "Get feedbacks",
            "Get feedback templates", "Insert feedback", "cancelShippingOrderPartial", "Get code browser",
            "Code browser update", "Get certificate issues", "Get certificates types", "Get module log",
            "Get machine types", "Get serial numbers pools", "Edit serial numbers pool settings",
            "Change user language", "Reporting Data Staging", "sp_get_turon_crypto_order_details",
            "Response from EMVS for product pack data", "CMO - get serial numbers", "CMO - return production data",
            "Trusted Counter Party", "Request SSCC Information", "Contract Information", "Reporting",
            "VRS Configuration settings", "iVEDA Products Xml Download",
            "serial number providers dynamic client token updated",
            "serial number providers oms connection detail updated",
            "serial number providers oms connection detail inserted", "import_crpt_turon", "Import crypto code",
            "Save CMO Provider", "Edit CMO Integration Serials Pools", "Internal Transfer", "Generate ASN XML FILE",
            "Send ASN XML File", "Client-Get serial weblinks for production", "Download ShippingOrder Weblinks Codes",
            "import_crpt_nutra", "Archive"
        ]

        actual_permissions = []
        permission_elements = self.driver.find_elements(By.XPATH, "//table[@id='rolestable']/tbody/tr/td[1]")
        for elem in permission_elements:
            if elem.text in expected_permissions:
                actual_permissions.append(elem.text)

        if expected_permissions == actual_permissions:
            print("✅ Test 23 Passed: All user permissions are present and in correct order")
        else:
            print(
                self.ANSI_RED_BACKGROUND + "❌ Test 23 Failed: User permissions missing or out of order" + self.ANSI_RESET)

    @staticmethod
    def getGLN(m):
        length = len(m)
        b_map = {
            1: "12345678912", 2: "1234567891", 3: "123456789", 4: "12345678",
            5: "1234567", 6: "123456", 7: "12345", 8: "1234", 9: "123", 10: "12", 11: "1"
        }
        b = b_map.get(length, "12345")
        c = m + b
        d = int(c)

        mk = [int(x) for x in reversed(str(d))]
        a1 = sum(mk[i] for i in range(0, 12, 2))
        a2 = sum(mk[i] for i in range(1, 12, 2))
        addi = a1 * 3 + a2

        prop = ((addi // 10) + 1) * 10
        check_digit = prop - addi
        check_digit = 0 if check_digit == 10 else check_digit

        GLN1 = c + str(check_digit)
        GLN1 = GLN1[:13]

        return GLN1

    @staticmethod
    def generate_full_gln(existing_prefix: str) -> str:
        # Pad with random digits to make length 12
        while len(existing_prefix) < 12:
            existing_prefix += str(random.randint(0, 9))

        digits = [int(x) for x in existing_prefix]
        checksum = (10 - ((sum(digits[-1::-2]) * 3 + sum(digits[-2::-2])) % 10)) % 10
        return existing_prefix + str(checksum)





    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()



if __name__ == "__main__":
    unittest.main()

