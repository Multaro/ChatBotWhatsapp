import time

from selenium import webdriver
from simon.accounts.pages import LoginPage
from simon.chat.pages import ChatPage
from simon.chats.pages import PanePage
from simon.header.pages import HeaderPage


# Creating the driver (browser)
driver = webdriver.Firefox()
driver.maximize_window()

# Login
#       and uncheck the remember check box
#       (Get your phone ready to read the QR code)
login_page = LoginPage(driver)
login_page.load()
print('tempo')
time.sleep(20)
print('fim')

# 1. Get all opened chats
#       opened chats are the one chats or conversations
#       you already have in your whatsapp.
#       IT WONT work if you are looking for a contact
#       you have never started a conversation.
pane_page = PanePage(driver)
print(pane_page)

# get all chats
print('pegando chats')
opened_chats = pane_page.opened_chats

print(opened_chats)

for oc in opened_chats:
    print(oc.name)  # contact name (as appears on your whatsapp)
    print(oc.icon)  # the url of the image
    print(oc.last_message)
    print(oc.last_message_time)  # datetime object
    print(oc.has_notifications())  # are there unread messages?
    print(oc.notifications)  # returns a integer with the qty of new

first_chat = opened_chats[0]
first_chat.click()


# Logout
header_page = HeaderPage(driver)
header_page.logout()

# Close the browser
driver.quit()