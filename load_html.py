from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import json

options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Example usage
url = 'http://timetable.msu.az/'  # Update with the login page URL
username = 'msu'  # Update with your username
password = 'msu2013'  # Update with your password

def login():
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




def write_schedule_to_file(facultiy_id, course):
  first_dropdown = Select(driver.find_element('id', 'repProfId'))
  first_dropdown.select_by_value(f'{facultiy_id}')

  second_dropdown = Select(driver.find_element('id', 'repCourseId'))
  second_dropdown.select_by_index(course)


  time.sleep(1)

  third_dropdown = Select(driver.find_element('id', 'repWeekId'))
  third_dropdown.select_by_visible_text("12.02.2024 - 17.02.2024")

  time.sleep(1)


  driver.find_element('id', 'repGraph').click()
  # Wait for the login process to complete
  time.sleep(3)  # Adjust as needed

  #  ////
  element = driver.find_element('id', 'divPrint')

  f = open(f"./schedules/{facultiy_id}-{course}.txt", "w", encoding='utf-8')
  f.write(element.get_attribute('innerHTML'))
  f.close()



def loadIds():
  faculty_ids = {}
  
  element = driver.find_element('id', 'repProfId')
  str = element.get_attribute("innerHTML")
  str = str[1:-1]

  while('><' in str):
      str = str.replace('><','')
  strs = str.split('option')
  strs = strs[2:]

  def remove(arr, str):
      new_arr = []
      for x in arr:
          x = x.replace(str, '')
          new_arr.append(x)
      return new_arr

  strs = remove(strs, "value=")
  strs = remove(strs, '"')
  strs = remove(strs, 'title=>')
  strs = remove(strs, '</')

  for x in strs:
      if(x[1:3]):
          id = int(x[1:3])
          faculty_ids[x[3:].removeprefix(" ")]=id

  json.dump(faculty_ids, open("faculty_ids.json", 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

def logout():
   driver.quit()


