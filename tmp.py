from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from PIL import Image
from io import BytesIO
import time

def login_and_take_screenshot(url, username, password, output_path):
    # Set up a headless Chrome browser
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    try:
        # Load the webpage
        driver.get(url)
        
        # Find the username and password input fields and enter credentials
        username_field = driver.find_element('name', 'username')
        username_field.send_keys(username)
        password_field = driver.find_element('name', 'password')
        password_field.send_keys(password)
        
        # Submit the login form
        driver.find_element('name', 'submit').click()

        time.sleep(1)


        driver.find_element('id', 'tdMenu').click()

        driver.find_element('id', 'tdeduGraph_common').click()

        time.sleep(1)

       # //////

        # Select options in dropdowns
        first_dropdown = Select(driver.find_element('id', 'repProfId'))
        first_dropdown.select_by_value("10")

        second_dropdown = Select(driver.find_element('id', 'repCourseId'))
        second_dropdown.select_by_index(2)


        time.sleep(1)

        third_dropdown = Select(driver.find_element('id', 'repWeekId'))
        third_dropdown.select_by_visible_text("12.02.2024 - 17.02.2024")

        time.sleep(1)


        driver.find_element('id', 'repGraph').click()
        # Wait for the login process to complete
        time.sleep(5)  # Adjust as needed

        # Get the full height of the webpage
        full_height = driver.execute_script("return document.body.scrollHeight")
        full_width = driver.execute_script("return document.body.scrollWidth")

        # Set the window size to match the full document height
        driver.set_window_size(full_width + 5, full_height)  # Adjust width as needed

      #  ////
        element = driver.find_element('id', 'divPrint')

        # Get the location and size of the element
        location = element.location
        size = element.size

        # Take a screenshot of the entire page
        screenshot = driver.get_screenshot_as_png()

        # Use Pillow to crop the screenshot to the element's dimensions
        img = Image.open(BytesIO(screenshot))
        img = img.crop((location['x'] - 1, location['y'] + 50, location['x'] + size['width'] + 1, location['y'] + size['height'] - 35 ))        
      #  ////

        # Use Pillow to open the screenshot and save it
        
        img.save(output_path)

    finally:
        # Close the browser
        driver.quit()






# Example usage
url = 'http://timetable.msu.az/'  # Update with the login page URL
username = 'msu'  # Update with your username
password = 'msu2013'  # Update with your password
output_path = 'screenshot.png'

try:
    login_and_take_screenshot(url, username, password, output_path)
except Exception as e:
    print("An error occurred:", e)
