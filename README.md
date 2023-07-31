# NU-Courses-Registration-Scraping

This project is a Python script that automates the process of logging in to the Nile University's PowerCampus Self-Service platform and scrapes course information using BeautifulSoup and Selenium.

## Requirements

1. Python (Already installed on your system)
2. Chromedriver (Included in the project directory)
3. Internet Connection

## Installation

To run this project, you need to install the required Python modules. To do this, follow these steps:

1. Make sure you have Python and pip installed.
2. Double-click the `Required_Modules.bat` batch file in the project directory. This batch file will install the necessary Python modules (BeautifulSoup, lxml, and Selenium).
3. If any errors occur during the installation, try running the batch file in an Anaconda environment (if Anaconda is installed) to resolve any potential dependency conflicts.

## How to Use

1. Double-click the `script.py` Python script in the project directory.
2. Enter your username and password when prompted (next steps are automated).
3. The script will open a Chrome browser and navigate to the Nile University's PowerCampus Self-Service platform.
4. It will log in using the provided credentials.
5. The script will then navigate to the courses registration page and perform an advanced search.
6. It will scrape course information from the search results and save it to a file named `course_info.txt` in the project directory.

## Note

- The `chromedriver.exe` file is present in the project directory. This file is required for Selenium to automate the Chrome browser (version 115.0.5790.110). If your version is different, please download the compatible driver for your version.

## Disclaimer

This project is intended for educational purposes only. Use it responsibly and at your own risk. I am not responsible for any misuse or violation of terms and conditions related to the Nile University's PowerCampus Self-Service platform.
