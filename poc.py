import time
import chromedriver_autoinstaller
import pyautogui
import pyperclip

from selenium.webdriver.common.by import By
from selenium import webdriver
from modules.openai.chatGPT import chatGPT
from utils.constants import CHALLENGE_DESCRIPTION_CLASS, URL, VIEW_LINE_CLASS
from utils.files import read_file_lines, save_as_text_file


class POC():
    def __init__(self):
        chromedriver_autoinstaller.install()
        self.driver = webdriver.Chrome()
        self.chatGPT = chatGPT()
    
    def start(self) -> webdriver:
        self.driver.get(URL)
        self.driver.maximize_window()

    def select_course(self) -> None:
        time.sleep(2)
        courses_list = self.driver.find_elements(By.CLASS_NAME, "map-superblock-link")
        # for course in courses_list:
        #     course.click()
        #     print("makeRoutine")
        courses_list[0].click()

    def select_course_section(self) -> None:
        courses_section = self.driver.find_elements(By.CLASS_NAME, 'map-title')
        # courses_section[0].click() # Dropdown section button
        
        time.sleep(3)
        start_project_button = self.driver.find_elements(By.CLASS_NAME, 'btn-sm') # Start Project Button
        start_project_button[0].click()

    def click_start_coding_button(self):
        time.sleep(3.5)
        start_coding_button = self.driver.find_element(By.XPATH, '//*[@id="headlessui-dialog-panel-2"]/div[3]/button')
        start_coding_button.click()

    def get_challenge_description(self):
        time.sleep(6)
        
        challenge_description = self.driver.find_element(By.CLASS_NAME, CHALLENGE_DESCRIPTION_CLASS)
        
        self.prompt = challenge_description.text

        with open("challenge_description.txt", 'w+') as f:
            f.write(challenge_description.text)

    def set_current_code_state(self):
        time.sleep(5)
        
        view_line_elements = self.driver.find_elements(By.CLASS_NAME, VIEW_LINE_CLASS)
        
        for e in view_line_elements:
            try:
                e.click()
            except:
                print("Skipped Element")
        
        pyautogui.hotkey('ctrl', 'a') 
        pyautogui.hotkey('ctrl', 'c')
        self.current_code_state = pyperclip.paste()

        pyautogui.press("backspace") # Clean all the text in the code editor

    def get_chatgpt_response(self):
        save_as_text_file(text_string=self.current_code_state, filename="current_code_state.txt")

        self.response = self.chatGPT.make_request(self.prompt, self.current_code_state)

        save_as_text_file(text_string=self.response, filename="chat_gpt_response.txt")

    def submit_challenge(self):
        lines = read_file_lines("chat_gpt_response.txt")
        for line in lines:
            pyautogui.press("home")
            pyautogui.write(line)
        pyautogui.hotkey('ctrl', 'enter')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'enter')

    def action(self):
        self.start()
        self.select_course()
        self.select_course_section()
        self.click_start_coding_button()
        for _ in range(10):
            self.get_challenge_description()
            self.set_current_code_state()
            self.get_chatgpt_response()
            self.submit_challenge()
            time.sleep(2)


if __name__ == '__main__':
    b = POC()
    b.action()

