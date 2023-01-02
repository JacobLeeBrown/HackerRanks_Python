# References =
#   https://towardsdatascience.com/controlling-the-web-with-python-6fceb22c5f08
#   https://selenium-python.readthedocs.io/getting-started.html#simple-usage

import my_env as env
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    # Using Chrome to access web
    driver = webdriver.Chrome()
    # Open the website
    driver.get('https://www.e-rewards.com/login')

    # Check if we need to login or are already logged in
    if 'Login' in driver.title:
        user_box = driver.find_element(By.ID, 'username')
        user_box.clear()
        pass_box = driver.find_element(By.ID, 'password')
        pass_box.clear()

        user_box.send_keys(env.username)
        pass_box.send_keys(env.password)

        sign_in_button = driver.find_element(By.XPATH, "//input[@type='submit'][@value='Sign In']")
        sign_in_button.click()

    # Now signed-in
    # Select first available survey
    first_survey_button = driver.find_element(By.XPATH, "//ul[@class='widget-offers-list']//a[1]")

    while 'e-Rewards' in driver.title:
        # Pre-qualification questions
        question_text_elem = driver.find_element(By.CLASS_NAME, 'questionText')
        question_text = question_text_elem.text



    print('End of auto_survey')
