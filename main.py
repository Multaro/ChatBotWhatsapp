import time

from selenium import webdriver
from simon.accounts.pages import LoginPage
from simon.header.pages import HeaderPage
from simon.pages import BasePage

driver = webdriver.Firefox()
driver.maximize_window()

login_page = LoginPage(driver)
login_page.load()
login_page.remember_me = False
time.sleep(7)

base_page = BasePage(driver)
base_page.is_title_matches()
base_page.is_welcome_page_available()
base_page.is_nav_bar_page_available()
base_page.is_search_page_available()
base_page.is_pane_page_available()

base_page.is_chat_page_available()

header_page = HeaderPage(driver)
header_page.logout()

driver.quit()