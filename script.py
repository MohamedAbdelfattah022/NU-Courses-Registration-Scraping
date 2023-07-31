from bs4 import BeautifulSoup
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

usr = input("Enter your username")
pswrd = input("Enter your password")

# Initialize Chrome driver
chromedriver_path = "chromedriver.exe"
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)

# Load the web page in the new tab
url = 'https://register.nu.edu.eg/PowerCampusSelfService/Home'
driver.get(url)
time.sleep(2)

# Log in
user_name = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']")))
user_name.clear()
time.sleep(1)
print("Sending user name")
user_name.send_keys(usr)
time.sleep(1)

next_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button']")))
time.sleep(1)
print("Click Next")
next_btn.click()
time.sleep(1)

password = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
time.sleep(1)
password.clear()
time.sleep(1)
print("Sending Password")
password.send_keys(pswrd)
time.sleep(1)

sign_in_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btnSignIn")))
time.sleep(1)
print("Click Sign In")
sign_in_btn.click()
time.sleep(1)

registration = 'https://register.nu.edu.eg/PowerCampusSelfService/Registration/Courses'
time.sleep(2)
print("Going to Courses")
driver.get(registration)
time.sleep(2)

advanced_search = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button']")))
time.sleep(2)
advanced_search.click()

search_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btnSearch")))
search_btn.click()

# BeautifulSoup Scraping
courses_div_element = WebDriverWait(driver, 15).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="contentPage"]/div[2]/div/div/div[1]/div[3]/div')))
# Extract the innerHTML of the div using Selenium
courses_div = courses_div_element.get_attribute('innerHTML')

soup = BeautifulSoup(courses_div, "lxml")

# Find all course divs
all_courses = soup.find_all('div', class_='jss569 grid-item jss571 jss524 jss615 jss568 jss621 jss650')

# print(len(all_courses))


def get_course_info(all_courses):
    with open('course_info.txt', 'a', encoding='utf-8') as file:
        for course in all_courses:
            # Extract the text from the span inside the h4 tag
            course_name = course.find('h4').find('span').text.strip()
            # Extract the text from the first span with course details
            section_details = course.find_all('span', class_='jss426 jss413 jss768 jss761 jss429 jss425 jss455')[
                0].text.strip()
            # Extract the text from the second span with course details
            course_details = course.find_all('span', class_='jss426 jss413 jss768 jss761 jss429 jss425 jss455')[
                1].text.strip()

            # Write the course information to the file
            file.write(course_name + "\n")
            file.write(section_details + "\n")
            file.write(course_details + "\n")
            file.write("---\n")
        print("Mission Accomplished")
        file.close()


get_course_info(all_courses)
