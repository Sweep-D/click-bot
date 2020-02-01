"""
This script automates clicking a button of the collect bonus in twitch.
Storing username, password, twitch channel in a separate location because uploading this to github.
"""
from __future__ import print_function
import json
import re
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from apiclient import errors

# If modifying these scopes, delete the file token.pickle
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
# ---------------------------------------------------------------------

def get_twitch_auth_code():
    creds = None
    # The file token.pickle stores the user"s access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("C:\\creds\\credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    service = build("gmail", "v1", credentials=creds)

    try:
        response = service.users().messages().list(userId="me", q="in:inbox from:no-reply@twitch.tv is:unread").execute()
        messages = []
        if "messages" in response:
            messages.extend(response["messages"])
            print(messages)
        response_msg = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()
        response_snip = response_msg["snippet"]
        auth_code = re.search("[0-9]{6}", response_snip)
        print(auth_code.group(0))
        return auth_code.group(0)
    except errors.HttpError:
        print("An error has occured:" % s) % errors

# Keep chrome Open
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)

# Import json details
twitch_d = "C:\\creds\\twitch_d.json"
with open(twitch_d, "r") as read_file:
    twitch_details = json.load(read_file)

# Load browser and  initiate variables
driver = webdriver.Chrome()
twitch_login = "https://www.twitch.tv/login"
twitch_url = "https://www.twitch.tv/" + twitch_details["channel"]


def twitch_site_login():
    print("Opening:", twitch_login)
    driver.get(twitch_login)
    driver.implicitly_wait(3)
    driver.find_element_by_id("login-username").send_keys(twitch_details["username"])
    driver.find_element_by_id("password-input").send_keys(twitch_details["password"])
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div[1]/div/div/div[3]/form/div/div[3]/button").click()
    time.sleep(30)
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div/div/div/div[1]/div/div/div[3]/div[2]/div/div[1]/div/input").send_keys(get_twitch_auth_code())
    time.sleep(10)


twitch_site_login()
driver.get(twitch_url)
flag = 1
bonus_click = "/html/body/div[1]/div/div[2]/div/div[2]/div/div[1]/div/div/section/div/div[5]/div[2]/div[2]/div[1]/div/div/div/div[2]/div/div/div/button"

# Actual program...
while flag == 1:
    try:
        driver.find_element_by_xpath(bonus_click).click()
        print("!!!---Claimed a bonus---!!!")
    except Exception:
        print("Can't find the bonus")
        time.sleep(30)
