
import threading
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

proxies = [
    "https://dmproxy698:dmproxy698@209.99.134.241:5937",
    "https://dmproxy698:dmproxy698@45.114.15.244:6225",
]


def automate_browser(phone_number, proxy):
    options = webdriver.ChromeOptions()
    options.add_argument(f'--proxy-server={proxy}')

    # for debugging force awake
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.tiktok.com/404?fromUrl=/phone-or-email")

    btn_login = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="header-login-button"]'))
    )
    btn_login.click()

    btn_phone = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginContainer"]/div/div/a[2]'))
    )
    btn_phone.click()

    btn_code_country = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginContainer"]/div[2]/form/div[2]/div/div[1]/div'))
    )
    btn_code_country.click()

    input_code_country = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="login-phone-search"]'))
    )
    input_code_country.send_keys("timor")

    btn_code_country = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="TL-670"]'))
    )
    btn_code_country.click()

    input_number = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginContainer"]/div[2]/form/div[2]/div/div[2]/input'))
    )
    input_number.send_keys(phone_number)

    btn_send_code = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="loginContainer"]/div[2]/form/div[3]/div/button'))
    )
    btn_send_code.send_keys(phone_number)


# Read numbers from an Excel file with a header named "number"
df = pd.read_excel('number.xlsx', header=0)  # Assuming the header is in the first row
numbers = df['number'].tolist()  # Extract the numbers from the 'number' column

total_numbers = len(numbers)  # Total number of data points
max_browsers = len(proxies)

# Split the list of numbers into chunks of max_browsers size
number_chunks = [numbers[i::max_browsers] for i in range(max_browsers)]

for i, chunk in enumerate(number_chunks):
    threads = []

    for number, proxy in zip(chunk, proxies):
        thread = threading.Thread(target=automate_browser, args=(number, proxy))
        threads.append(thread)

    print("-----")
    print(f"Starting chunk {i + 1} of numbers (Total: {len(chunk)} numbers)...")

    # Start all threads
    for thread in threads:
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

    print(f"Finished chunk {i + 1} of numbers.")

print(" ")
print("----")
print(f"All browsers closed.")
