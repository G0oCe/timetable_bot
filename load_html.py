import os
import json
import time
import logging
from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Chrome options for headless browsing
options = webdriver.ChromeOptions()
#options.add_argument('--headless')  # Run in headless mode (no GUI)

# Define the login URL and user credentials
url = 'http://timetable.msu.az/'  # Update with the actual URL
username = os.getenv('TT_USER')  # Fetch username from environment variables
password = os.getenv('TT_PASSWORD')  # Fetch password from environment variables

# Initialize WebDriver globally
driver = None

def setup_driver():
    """Sets up the WebDriver."""
    global driver
    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(10)  # Optional: Set a timeout for loading pages

def login():
    """Logs into the timetable website using provided credentials."""
    try:
        driver.get(url)  # Load the login page
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
        
        driver.find_element(By.NAME, 'username').send_keys(username)
        driver.find_element(By.NAME, 'password').send_keys(password)
        driver.find_element(By.NAME, 'submit').click()

        # Wait for the menu element to be clickable
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'tdMenu'))).click()
        driver.find_element(By.ID, 'tdeduGraph_common').click()
        logging.info("Login successful and navigated to schedule section.")
    except Exception as e:
        logging.error(f"Login failed: {e}")
        logout()

def write_schedule_to_file(faculty_id, course, week = "21.10.2024 - 26.10.2024"):
    """Writes the schedule for a given faculty and course to a text file."""
    try:
        # Convert faculty_id and course from int to str
        faculty_id_str = str(faculty_id)
        course_str = str(course)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'repProfId')))
        
        # Select faculty by ID
        Select(driver.find_element(By.ID, 'repProfId')).select_by_value(faculty_id_str)
        
        # Select course by index (assumed to be an integer that represents the index)
        Select(driver.find_element(By.ID, 'repCourseId')).select_by_index(int(course_str))
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'repWeekId')))
        Select(driver.find_element(By.ID, 'repWeekId')).select_by_visible_text(week)

        driver.find_element(By.ID, 'repGraph').click()
        
        # Wait for the schedule to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'divPrint')))
        schedule_element = driver.find_element(By.ID, 'divPrint')

        # Write schedule to a file
        with open(f"./schedules/{faculty_id_str}-{course_str}.txt", "w", encoding='utf-8') as f:
            f.write(schedule_element.get_attribute('innerHTML'))
            logging.info(f"Schedule for {faculty_id_str} - Course {course_str} written to file.")
    except Exception as e:
        logging.error(f"Failed to write schedule for {faculty_id} - Course {course}: {e}")

def load_faculty_ids():
    """Loads faculty IDs from the dropdown and saves them to a JSON file."""
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'repProfId')))
        faculty_ids = {}
        options = driver.find_elements(By.CSS_SELECTOR, '#repProfId option')

        for option in options[2:]:  # Skip the first two entries
            faculty_id = option.get_attribute('value')
            faculty_name = option.text.strip()
            faculty_ids[faculty_name] = faculty_id

        with open("faculty_ids.json", 'w', encoding='utf-8') as json_file:
            json.dump(faculty_ids, json_file, indent=4, ensure_ascii=False)
            logging.info("Faculty IDs loaded and saved to faculty_ids.json.")
    except Exception as e:
        logging.error(f"Failed to load faculty IDs: {e}")

def logout():
    """Closes the WebDriver session."""
    if driver:
        driver.quit()
        logging.info("WebDriver session closed.")

if __name__ == "__main__":
    setup_driver()
    try:
        login()  # Attempt to log in
        
        # Assuming you have valid faculty_id and course
        faculty_id = "3"  # Replace with actual faculty ID
        course = 0  # Replace with actual course index (0 for the first course)

        # Attempt to write the schedule to a file
        write_schedule_to_file(faculty_id, course)
    
    except Exception as e:
        logging.error(f"An error occurred during the process: {e}")
    
    finally:
        logout()  # Ensure logout happens regardless of success or failure

