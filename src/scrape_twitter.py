from time import sleep
import streamlit as st
# from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TwitterBot:
    def __init__(self, username, password):
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.username = username
        self.password = password
        self.base_url = "https://twitter.com/"
        self.driver.maximize_window()
        self.driver.get(self.base_url)
        sleep(0.5)  # Allow page to load

    def close(self):
        self.driver.quit()

    def click_element(self, selector, by=By.CSS_SELECTOR):
        try:
            self.wait.until(EC.visibility_of_element_located((by, selector)))
            element = self.driver.find_element(by, selector)
            element.click()
            sleep(5)
        except Exception as ex:
            st.write(f"Error clicking element: {ex}")

    def input_text(self, selector, text, by=By.CSS_SELECTOR):
        try:
            element = self.driver.find_element(by, selector)
            element.send_keys(text)
            sleep(5)
        except Exception as ex:
            st.write(f"Error entering text: {ex}")

    def login(self):
        self.click_element('#react-root > div > div > div > main > div > div > div > div > a')
        self.input_text('#layers input[name="text"]', self.username)
        self.click_element('#layers div[data-testid="ocfEnterTextNextButton"]')
        self.input_text('#layers input[name="password"]', self.password)
        self.click_element('#layers div[data-testid="LoginForm_Login_Button"]')

    def search_topic(self, topic):
        search_input = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'
        self.input_text(search_input, topic, by=By.XPATH)

    def collect_tweets(self):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, '//article[@data-testid="tweet"]')))
        self.driver.execute_script("window.scrollTo(0, 600)")
        tweets = self.driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')[:5]
        sleep(3)
        result = {}
        for tweet in tweets:
            self.driver.execute_script("arguments[0].click();", tweet)
            sleep(3)
            replies = []
            reply_elements = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-testid="tweetText"]')))
            for reply in reply_elements[1:]:
                replies.append(reply.text)
            result[tweet.text] = replies
            self.driver.back()
            sleep(4)
        return result
