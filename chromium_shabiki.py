"""
A module to login in to Chromium browser and search for links
from the games and save them to txt files for each game.

The links will be found from duckduckgo.com.
"""

# Import some necessary modules
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC


load_dotenv()

# Set the credentials
MOBILE_NO = os.getenv("MOBILE_NO")
PASSWORD = os.getenv("PASSWORD")


EXECUTABLE_PATH = "/usr/bin/chromium"
# Update with the path to Chromium browser

CHROME_DRIVER = "/usr/bin/chromedriver"
# Update with the path to Chrome driver

service = Service(CHROME_DRIVER)

options = webdriver.ChromeOptions()
options.binary_location = EXECUTABLE_PATH

# For running brave browser in the background...
options.add_argument("--headless")
options.add_argument("--disable-gpu")

driver = webdriver.Chrome(service=service, options=options)


def acquire_live_games():
    """
    Will acquire the live games from the shabiki website
    """

    driver.get("https://www.shabiki.com/Login")

    driver.find_element(By.ID, "userMobile").send_keys(MOBILE_NO)

    driver.find_element(By.ID, "userPass").send_keys(PASSWORD)

    # Login
    driver.find_element(By.ID, "disableLoginButtonClick").send_keys(Keys.ENTER)

    # Wait for the page to load
    live_now_elem = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
        (By.CLASS_NAME, "SB-liveNow")))

    live_now_elem.click()

    elements = driver.find_elements(By.CLASS_NAME, "SB-leagueBox")

    # A list to hold the live games dict
    live_games: list[dict[str, str]] = []

    for tag_class in elements:
        elem_dct: dict[str, str] = {}

        elements_lst = ('SB-match__teamsInfo',
                        'SB-match__matchMinute',
                        'SB-match__scoreInfo',
                        'SB-btnOddsGroup')

        for element in elements_lst:
            inner_elem = tag_class.find_element(By.CLASS_NAME, element)
            elem_dct[element] = inner_elem.text

        live_games.append(elem_dct)

        # put_games_to_file(f"TEAMS :\n{elem_dct['SB-match__teamsInfo']}")
        # put_games_to_file(f"MINUTE :\n{elem_dct['SB-match__matchMinute']}")
        # put_games_to_file(f"SCORES :\n{elem_dct['SB-match__scoreInfo']}")
        # put_games_to_file(f"ODDS GROUP :\n{elem_dct['SB-btnOddsGroup']}")
        # put_games_to_file("\n\n\n")
        #
        # print(elem_dct)

    return live_games


def main():
    """our main function"""
    games_lst = acquire_live_games()
    print(games_lst)


if __name__ == "_acquire_live_games__":
    main()
