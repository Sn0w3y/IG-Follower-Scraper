import pandas as pd
from selenium import webdriver
import time
from datetime import datetime
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import random
import schedule
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# for Chrome users
from webdriver_nager.chrome import ChromeDriverManager

browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
username = "enter_user_here"
password = "enter_pass_here"

def auth(username, password):
    try:
        browser.get("https://instagram.com/login")
        time.sleep(random.randrange(5, 10))
        input_username = browser.find_element_by_name("username")
        input_password = browser.find_element_by_name("password")

        input_username.send_keys(username)
        time.sleep(random.randrange(2, 4))
        input_password.send_keys(password)
        time.sleep(random.randrange(2, 4))
        input_password.send_keys(Keys.ENTER)
        time.sleep(random.randrange(5, 10))

    except Exception as e:
        print(e)


def check_followers():
    browser.get("https://www.instagram.com/*****enter_user_here******/followers")

    time.sleep(5)

    fBody = browser.find_element_by_xpath("//div[@class='_aano']")

    # Scroll in the Followers List
    scroll = 0
    while scroll < 300:  # scroll 5 times
        browser.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(0.5)
        scroll += 1

    time.sleep(2)

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    usernames = soup.find_all('div', class_="_ab8y")

    # Load existing usernames from the Excel file
    df = pd.read_excel(r"C:/Users/User/Documents/test.xlsx")
    existing_usernames = df["Usernames"].tolist()

    new_users = []
    lost_users = []
    for username in usernames:
        username_text = username.text.strip()
        if username_text not in existing_usernames:
            # Add new username to the list of new users
            new_users.append(username_text)

            # Append the new username and date/time to the Excel file
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df = df.append({"Usernames": username_text, "Date/Time": now}, ignore_index=True)
            df.to_excel(r"C:/Users/User/Documents/test.xlsx", index=False)
        else:
            # Remove the username from the existing list
            existing_usernames.remove(username_text)

    # Check for lost users
    for lost_username in existing_usernames:
        lost_users.append(lost_username)

    if new_users:
        # Print the new usernames to the console
        print(f"New users: {new_users}")

    if lost_users:
        # Print the lost usernames to the console
        print(f"Lost users: {lost_users}")


auth(username, password)

# Schedule the function to run every 20 minutes
schedule.every(1).minutes.do(check_followers)

while True:
    # Run pending scheduled tasks
    schedule.run_pending()
    time.sleep(1)
