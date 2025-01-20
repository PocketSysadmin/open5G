from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options  # Ensure this import is included
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
#chrome_options.binary_location ="/usr/bin/google-chrome"
   # Set up the Chrome WebDriver
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")  # Disable the sandbox for restricted environments
chrome_options.add_argument("--disable-dev-shm-usage")  # For shared memory issues in containers
chrome_options.add_argument("--headless=new")  # Optional: Headless mode for running without GUI

chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


    
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)



def visit_websites(urls):
    
    # Set up the Chrome WebDriver
    #chrome_options = Options()
    #chrome_options.add_argument("--no-sandbox")  # Disable the sandbox for restricted environments
    #chrome_options.add_argument("--disable-dev-shm-usage")  # For shared memory issues in containers
    #chrome_options.add_argument("--headless=new")  # Optional: Headless mode for running without GUI

#    chrome_options.add_argument("--headless")  # Optional: run in headless mode (no GUI)
    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    # Initialize WebDriver
   # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    #service = Service(ChromeDriverManager().install())
    #driver = webdriver.Chrome(service=service)
    
    for url in urls:
        # Open each URL
        driver.get(url)
        print(f"Visited {url}")
        time.sleep(5)  # Wait to observe each webpage

    # Close the browser
    #driver.quit()

def fill_and_submit_form(url):
    """
    Opens a browser, fills out a form on the specified URL, submits it, retrieves a message, and closes the browser.
    """
    # Set up the Chrome WebDriver
# Set up the Chrome WebDriver
    #chrome_options = Options()
    #chrome_options.add_argument("--no-sandbox")  # Disable the sandbox for restricted environments
    #chrome_options.add_argument("--disable-dev-shm-usage")  # For shared memory issues in containers
    #chrome_options.add_argument("--headless=new")  # Optional: Headless mode for running without GUI

    #driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    # Open the specified URL
    driver.get(url)

    # Locate form elements
    text_box = driver.find_element(By.NAME, "my-text")
    submit_button = driver.find_element(By.CSS_SELECTOR, "button")
    
    # Fill out the form and submit
    text_box.send_keys("Selenium")
    submit_button.click()

    # Retrieve and print the message text
    message = driver.find_element(By.ID, "message")
    text = message.text
    print("Form submission message:", text)
    
    time.sleep(5)  # Wait to observe the result
    
    # Close the browser
    #driver.quit()

def download_file_in_headless_mode(download_url, file_name, download_directory="downloads"):
    #chrome_options = Options()
    #chrome_options.add_argument("--headless=new")
    #chrome_options.add_argument("--no-sandbox")
    #chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--window-size=1920x1080")
    #chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    prefs = {
        "download.default_directory": os.path.abspath(download_directory),
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    }
    chrome_options.add_experimental_option("prefs", prefs)

    os.makedirs(download_directory, exist_ok=True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        print(f"Opening page: {download_url}")
        driver.get(download_url)

        # Wait for the file link
        print("Waiting for the file link...")
        file_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.LINK_TEXT, file_name))
        )

        # Click the file link
        print(f"Clicking on the file link: {file_name}")
        file_link.click()

        # Wait for the file to appear in the download directory
        downloaded_file_path = os.path.join(download_directory, file_name)
        timeout = 30
        start_time = time.time()
        while not os.path.exists(downloaded_file_path):
            if time.time() - start_time > timeout:
                print(f"Timeout: File not downloaded within {timeout} seconds.")
                break
            time.sleep(1)

        if os.path.exists(downloaded_file_path):
            print(f"File successfully downloaded: {downloaded_file_path}")
        else:
            print("File download failed.")
    except Exception as e:
        print(f"An error occurred: {e}")
    #finally:
    #    driver.quit()


def visit_and_click_rnd(url, link_text):
    # Set up Chrome WebDriver with options
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        # Open the specified website
        driver.get(url)
        print(f"Opened website: {url}")

        # Wait for and close the cookie consent popup
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.ID, "usercentrics-root"))
            )
            print("Cookie consent popup detected. Attempting to close it.")

            try:
                accept_button = driver.find_element(By.XPATH, "//button[contains(text(),'Accept')]")
                accept_button.click()
                print("Cookie consent popup closed.")
            except Exception as e:
                print("Couldn't find the Accept button with text 'Accept'. Trying JavaScript...")
                driver.execute_script("""
                    var consentButton = document.querySelector('button[data-testid="uc-accept-all-button"]') || 
                                         document.querySelector('button[aria-label="Accept all"]');
                    if (consentButton) consentButton.click();
                """)
                print("Popup closed using JavaScript.")

            # Wait for the overlay to disappear
            WebDriverWait(driver, 10).until(
                EC.invisibility_of_element_located((By.ID, "usercentrics-root"))
            )
            print("Cookie consent overlay is no longer visible.")
        except Exception as e:
            print(f"Error handling cookie consent popup: {e}")

        # Wait for the link to become clickable
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, link_text))
        )

        # Find the link and try clicking it
        link = driver.find_element(By.LINK_TEXT, link_text)
        try:
            link.click()
            print(f"Successfully clicked the link: {link_text}")
        except Exception as e:
            print(f"Direct click failed: {e}. Trying JavaScript...")
            driver.execute_script("arguments[0].click();", link)
            print(f"Clicked the link using JavaScript: {link_text}")

        # Optionally, wait for the new page to load
        time.sleep(5)

    except Exception as e:
        print(f"Error: {e}")
    #finally:
        # Close the browser session
    #    driver.quit()

# Example usage


# Example usage of visit_website
urls_to_visit = ["https://www.google.com","https://www.facebook.com"]
visit_websites(urls_to_visit)
# Example usage of fill_and_submit_form
url = "https://www.selenium.dev/selenium/web/web-form.html"
fill_and_submit_form(url)
# Example usage of download_file_from_filezilla
download_url = "https://filezilla-project.org/download.php?show_all=1"
file_name = "FileZilla_3.68.1_x86_64-linux-gnu.tar.xz"
download_file_in_headless_mode(download_url, file_name)
visit_and_click_rnd("https://www.upc.edu/en?set_language=en", "MENU")

#visit_and_click_rnd("https://www.upc.edu/en?set_language=en", "MENU")
driver.quit()