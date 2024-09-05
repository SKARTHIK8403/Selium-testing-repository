import unittest
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

class ECommerceTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.wait = WebDriverWait(self.driver, 10)
        
        # Load configuration
        with open('config.json') as f:
            self.config = json.load(f)
        
        self.base_url = self.config['base_url']
        self.username = self.config['login']['username']
        self.password = self.config['login']['password']
        self.invalid_username = self.config['login']['invalid_username']
        self.invalid_password = self.config['login']['invalid_password']
        self.product_id_1 = 1  # Adjust as needed for testing
        self.product_id_2 = 2  
        self.product_id_3 = 3
        self.excel_file = 'C:\\Users\\preethi\\Desktop\\ecommerced\\testcase.xlsx'


    def update_excel_status(self, row, status):
        try:
            # Load the existing Excel file
            df = pd.read_excel(self.excel_file)
            
            # Fill NA values to avoid ambiguity
            df = df.fillna('')
            
            # Update the status in the appropriate row
            df.loc[row, 'Status'] = status
            
            # Save the updated DataFrame back to Excel
            df.to_excel(self.excel_file, index=False)
        except Exception as e:
            print(f"Failed to update Excel file: {e}")

    def test_ecommerce_flow(self):
        driver = self.driver
        wait = self.wait

        # Test steps
        try:
            # Open home page
            driver.get(f"{self.base_url}/")
            time.sleep(2)
            self.assertIn("Welcome to our E-Commerce Store", driver.page_source, "Home page not displayed correctly.")
            self.update_excel_status(0, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(0, "Fail")  # Update status in Excel
            self.fail(f"Home page test failed: {e}")

        try:
            # Navigate to about page
            driver.get(f"{self.base_url}/description")
            time.sleep(2)
            self.assertIn("About", driver.page_source, "About page not displayed correctly.")
            self.update_excel_status(1, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(1, "Fail")  # Update status in Excel
            self.fail(f"About page test failed: {e}")

        try:
            # Navigate to login page
            driver.get(f"{self.base_url}/login")
            time.sleep(2)

            # Test invalid login
            username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
            password_field = driver.find_element(By.ID, 'password')
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            
            username_field.send_keys(self.invalid_username)
            password_field.send_keys(self.invalid_password)
            login_button.click()
            time.sleep(2)

            self.assertIn("Invalid credentials", driver.page_source, "Error message not displayed for invalid credentials.")
            self.update_excel_status(2, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(2, "Fail")  # Update status in Excel
            self.fail(f"Invalid login test failed: {e}")

        try:
            # Login with valid credentials
            driver.get(f"{self.base_url}/login")
            time.sleep(2)

            username_field = wait.until(EC.presence_of_element_located((By.ID, 'username')))
            password_field = driver.find_element(By.ID, 'password')
            login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
            
            username_field.clear()
            password_field.clear()
            username_field.send_keys(self.username)
            password_field.send_keys(self.password)
            login_button.click()
            time.sleep(2)

            wait.until(EC.url_contains(f"{self.base_url}/"))
            self.assertIn(f"Logout ({self.username})", driver.page_source, "Logout link not displayed after login.")
            self.update_excel_status(3, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(3, "Fail")  # Update status in Excel
            self.fail(f"Valid login test failed: {e}")

        try:
            # Add products to the cart from the home page
            add_to_cart_link_1 = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), 'Add to Cart') and contains(@href, '/add_to_cart/{self.product_id_1}')]")))
            add_to_cart_link_1.click()
            time.sleep(2)
            
            add_to_cart_link_2 = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), 'Add to Cart') and contains(@href, '/add_to_cart/{self.product_id_2}')]")))
            add_to_cart_link_2.click()
            time.sleep(2)

            add_to_cart_link_3 = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(text(), 'Add to Cart') and contains(@href, '/add_to_cart/{self.product_id_3}')]")))
            add_to_cart_link_3.click()
            time.sleep(2)
            self.update_excel_status(4, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(4, "Fail")  # Update status in Excel
            self.fail(f"Add to Cart test failed: {e}")

        try:
            # Open cart page and remove one product
            driver.get(f"{self.base_url}/cart")
            time.sleep(2)
            remove_button = wait.until(EC.presence_of_element_located((By.XPATH, f"//a[contains(@href, '/remove_from_cart/{self.product_id_1}')]")))
            remove_button.click()
            time.sleep(2)
            self.update_excel_status(5, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(5, "Fail")  # Update status in Excel
            self.fail(f"Remove from Cart test failed: {e}")

        try:
            # Checkout
            driver.get(f"{self.base_url}/checkout")
            time.sleep(2)
            back_to_home_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Back to Home')]")))
            back_to_home_link.click()
            time.sleep(2)
            self.update_excel_status(6, "Pass")  # Update status in Excel
        except Exception as e:
            print("Checkout page source:\n", driver.page_source)
            self.update_excel_status(6, "Fail")  # Update status in Excel
            self.fail(f"Checkout test failed: {e}")

        try:
            # Verify successful return to home page
            wait.until(EC.url_contains(f"{self.base_url}/"))
            self.assertIn("Welcome to our E-Commerce Store", driver.page_source, "Home page not displayed after checkout.")
            self.update_excel_status(7, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(7, "Fail")  # Update status in Excel
            self.fail(f"Return to Home verification failed: {e}")

        try:
            # Logout
            logout_link = wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Logout')]")))
            logout_link.click()
            time.sleep(2)
            self.update_excel_status(8, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(8, "Fail")  # Update status in Excel
            self.fail(f"Logout test failed: {e}")

        try:
            # Verify successful logout
            wait.until(EC.url_contains(f"{self.base_url}/"))
            self.assertIn("Login", driver.page_source, "Login page not displayed after logout.")
            self.update_excel_status(9, "Pass")  # Update status in Excel
        except Exception as e:
            self.update_excel_status(9, "Fail")  # Update status in Excel
            self.fail(f"Logout verification failed: {e}")

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
