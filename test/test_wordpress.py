
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys


HOST = "bobsblog.australia.ai"
USER = "bob"
PASS = "f=~uzR]hz*mpZQtStTuXLQti("

def fetch_page():
    options = webdriver.FirefoxOptions()
    # options.headless = True

    with webdriver.Firefox(firefox_options=options, executable_path='/home/snape/Downloads/geckodriver') as driver:
        driver.get("http://{}/wp-login.php".format(HOST))

        if "WordPress" not in driver.title:
            print ("gave login page title: %s", driver.title)
            return

        time.sleep(1)

        elem = driver.find_element_by_id("user_login")
        if not elem:
            print("login page does not have login field")
            return
        elem.send_keys(USER)

        time.sleep(1)

        elem = driver.find_element_by_id("user_pass")
        if not elem:
            print("login page does not have password field")
            return
        elem.send_keys(PASS)

        time.sleep(1)
        elem.send_keys(Keys.RETURN)

        time.sleep(10)

        if "WordPress" not in driver.title or "Dashboard" not in driver.title:
            print("did not load dashboard page, title: %s", driver.title)
            return

        driver.quit()



def main():

    fetch_page()
    return 0


if __name__ == "__main__":
    main()