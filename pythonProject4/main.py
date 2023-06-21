from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

from url import alertBoxURL

import serial
import time

# starting arduino
PORT = "COM3"
print(f'Opening port {PORT}...')
try:
    arduino = serial.Serial(port=PORT, baudrate=115200, timeout=.1)
    print (f'Success, {PORT} open')
except:
    print(f'Failed to open port {PORT}, exiting program...')
    quit()


def write_read(x, machine):
    machine.write(bytes(x, 'utf-8'))
    time.sleep(0.05)


def run_machine():
    write_read('1', arduino)
    # time.sleep(COOLDOWN)
    time.sleep(0.1)


# Set up Chrome driver
service = Service(r'C:\Users\garbo\OneDrive\Desktop\Sonali Python\pythonProject4\chromedriver.exe')  # Provide the path to your chromedriver executable
options = Options()
options.add_argument('--autoplay-policy=no-user-gesture-required')
options.add_argument('--headless')  # Run the browser in headless mode (without GUI)
driver = webdriver.Chrome(service=service, options=options)
# Navigate to the website
count = 0
try:
    # Navigate to the website
    driver.get(alertBoxURL)

    # Wait for the div to change its class from 'fadeOut' to 'fadeIn'
    wait = WebDriverWait(driver, 3600)
    previous_class = None
    try:
        while True:
            element = wait.until(EC.presence_of_element_located((By.ID, 'alerts')))
            current_class = element.get_attribute('class')

            if previous_class != current_class and current_class == 'fadeIn':
                count += 1
                print(f"{count} SHOCK WOOO")
                run_machine()
                # Perform additional actions here
                # ...
            previous_class = current_class

    except TimeoutException:
        print("Timeout occurred while waiting for the div to change.")
    except NoSuchElementException:
        print("The 'alerts' div element was not found.")
    except Exception as e:
        print("An error occurred:", str(e))


except TimeoutException:
    print("Timeout occurred while waiting for the div to change.")
except NoSuchElementException:
    print("The 'alerts' div element was not found.")
except Exception as e:
    print("An error occurred:", str(e))
finally:
    # Quit the browser driver
    driver.quit()