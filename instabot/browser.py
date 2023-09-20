from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchWindowException
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import pyautogui


class Browser:
    def __init__(self, user_data_dir: str, headless: bool = False) -> None:
        options = Options()
        options.add_argument(f'--user-data-dir={user_data_dir}')
        options.add_extension('chrome-extensions/inssist.crx')
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        self.driver = Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options,
        )

    def post_story(self, media_path: str, mentions: list[str] = []) -> None:
        while True:
            try:
                self.lazy_click('elements-images/plus-button.png', 0.9)
            except:
                break
            while True:
                try:
                    self.lazy_click('elements-images/story-button.png', 0.7)
                    sleep(3)
                    break
                except:
                    continue
        pyautogui.hotkey('ctrl', 'l')
        pyautogui.write(media_path)
        pyautogui.press('enter')
        for e, mention in enumerate(mentions):
            while True:
                try:
                    arroba_position = self.lazy_click('elements-images/arroba-button.png', 0.6)
                    break
                except:
                    sleep(1)
            if e == 0:
                pyautogui.write(mention)
            else:
                pyautogui.press('enter')
                pyautogui.write(f'@{mention}')
            sleep(1)
            pyautogui.click(arroba_position.left - 200, arroba_position.top)
            sleep(1)
            center = pyautogui.center(
                pyautogui.locateOnScreen(
                    'elements-images/arroba-button2.png', confidence=0.6
                )
            )
            pyautogui.moveTo(center.x, center.y)
            pyautogui.dragTo(
                arroba_position.left + 200,
                arroba_position.top,
                1,
                button='left',
            )
            sleep(1)
            pyautogui.moveTo(
                arroba_position.left + 130,
                arroba_position.top,
            )
            pyautogui.click(
                arroba_position.left + 130,
                arroba_position.top,
            )
            sleep(1)
        self.lazy_click('elements-images/add-story-button.png', confidence=0.9)

    def lazy_click(self, image_path: str, confidence: float):
        point = pyautogui.locateOnScreen(image_path, confidence=confidence)
        pyautogui.moveTo(point.left, point.top)
        pyautogui.click(point.left, point.top)
        return point

    def make_login(self, login: str, password: str) -> None:
        self.driver.get('https://www.instagram.com/accounts/login/')
        self.find_element('input[name=username]', wait=60).send_keys(login)
        input_password = self.find_element('input[name=password]')
        input_password.send_keys(password)
        input_password.submit()
        while True:
            try:
                self.find_element('a[href="/reels/"]')
                sleep(1)
                break
            except TimeoutException:
                continue

    def is_logged(self) -> bool:
        self.driver.get('https://www.instagram.com')
        try:
            self.find_element('a[href="/reels/"]', wait=10)
            return True
        except TimeoutException:
            return False


    def is_alive(self) -> bool:
        try:
            self.driver.execute_script('console.log("");')
            sleep(1)
            return True
        except NoSuchWindowException:
            return False

    def find_element(self, selector: str, element = None, wait: int = 30):
        return WebDriverWait(element if element else self.driver, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def find_elements(self, selector: str, element = None, wait: int = 30):
        return WebDriverWait(element if element else self.driver, wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )
