from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def initialize_driver():
    chromedriver_path = "chromedriver.exe"
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    # options.add_argument('--window-size=1920x1080')
    driver = webdriver.Chrome(executable_path=chromedriver_path, options=options)
    return driver


def login(driver, username, password):
    url = 'https://register.nu.edu.eg/PowerCampusSelfService/Home'
    driver.get(url)

    user_name = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='text']")))
    user_name.clear()
    print("Sending user name")
    user_name.send_keys(username)
    time.sleep(0.5)

    next_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button']")))
    print("Click Next")
    next_btn.click()
    time.sleep(0.5)

    password_field = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']")))
    password_field.clear()
    print("Sending Password")
    password_field.send_keys(password)
    time.sleep(0.5)

    sign_in_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btnSignIn")))
    print("Click Sign In")
    sign_in_btn.click()
    time.sleep(0.5)


def navigate_to_courses(driver):
    print("Going to Courses")
    registration_url = 'https://register.nu.edu.eg/PowerCampusSelfService/Registration/Courses'
    driver.get(registration_url)
    time.sleep(0.5)
    advanced_search = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='button']")))
    advanced_search.click()
    time.sleep(0.5)
    search_btn = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, "btnSearch")))
    search_btn.click()


def multiple_classes(course, driver, course_name, section_details, instructor_name):
    course_link = course.find('h4').find('button')
    button_id = course_link['id']
    driver.find_element_by_id(button_id).click()

    popup = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="sectionDetailModal"]/div[3]/div'))
    )

    schedules = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="sectionDetailModal"]/div[3]/div/div[2]/div[5]/div')
        )
    ).find_elements_by_tag_name('p')

    # instructor_name_div = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located(
    #         (By.XPATH, '/html/body/div[2]/div[3]/div/div[2]/div[3]/div/div/div[2]')
    #     )
    # )
    # instructor_name = instructor_name_div.find_element_by_tag_name('p').text.strip()

    schedule_paragraphs_list = []

    for schedule in schedules:
        schedule_paragraphs_list.append(schedule.text.strip())

    course_info = {
        "Instructor Name": instructor_name,
        "Course Name": course_name,
        "Section Details": section_details,
        "Schedule": schedule_paragraphs_list
    }

    print(schedule_paragraphs_list)
    close_button = popup.find_element_by_class_name('dialog-close-button')
    close_button.click()
    WebDriverWait(driver, 5).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="sectionDetailModal"]/div[3]/div'))
    )
    return course_info


def scrape_course_info(driver):
    print("Fetching Courses Data")
    courses_div_element = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="contentPage"]/div[2]/div/div/div[1]/div[3]/div'))
    )
    courses_div = courses_div_element.get_attribute('innerHTML')
    soup = BeautifulSoup(courses_div, "lxml")

    all_courses = soup.find_all('div', class_='jss569 grid-item jss571 jss524 jss615 jss568 jss621 jss650')
    all_names = soup.find_all('div', class_='jss569 grid-item jss571 jss524 jss615 jss568 jss625 jss652')

    course_info_list = []
    course_count = 0
    for course, instructor_name in zip(all_courses, all_names):
        # time.sleep(0.25)
        course_count += 1
        course_name = course.find('h4').find('span').text.strip()
        section_details = course.find_all('span')[1].text.strip()
        inst_name = instructor_name.find('span').text.strip()

        schedules = course.find('div').find_all('p')
        schedule_list = []
        for schedule in schedules:
            schedule_content = schedule.text.strip()
            if schedule_content != "Nile University":
                schedule_list.append(schedule_content)

        print("COURSE NAME: ", course_name)
        print("INSTRUCTOR NAME: ", inst_name)
        print(section_details)

        if len(schedule_list) == 1 and schedule_list[0] == "This class has multiple meeting times":
            multiple_class_course = multiple_classes(course, driver, course_name, section_details, inst_name)
            course_info_list.append(multiple_class_course)
            print(f"{course_count} courses has been parsed")
            print("")
            continue

        course_info = {
            "Instructor Name": inst_name,
            "Course Name": course_name,
            "Section Details": section_details,
            "Schedule": schedule_list
        }
        course_info_list.append(course_info)

        print(f"SCHEDULE:\n{schedule_list}")
        print(f"{course_count} courses has been parsed")
        print("")

    return course_info_list


def save_course_info_to_file(course_info_list):
    print("Writing data to file")
    count = 0
    with open('course_info.txt', 'w', encoding='utf-8') as file:
        for course_info in course_info_list:
            count += 1
            file.write(f"Instructor Name: {course_info['Instructor Name']}\n")
            file.write(f"Course Name: {course_info['Course Name']}\n")
            file.write(f"{course_info['Section Details']} \n")
            file.write("Schedule:" + "\n")
            for course_schedule in course_info["Schedule"]:
                file.write(course_schedule + "\n")
            file.write("---------\n")
            print(f"{count} written to file")


def main():
    try:
        user_name = input("Enter your Username: ")
        pass_key = input("Enter your Password: ")

        driver = initialize_driver()
        login(driver, user_name, pass_key)
        time.sleep(2)
        navigate_to_courses(driver)
        course_info_list = scrape_course_info(driver)
        save_course_info_to_file(course_info_list)

        print("Mission Accomplished")
        driver.quit()
        print("Browser closed.")
    except Exception as e:
        driver.quit()
        print(f"An error Occurred Due To: \n{e}")


if __name__ == "__main__":
    main()
