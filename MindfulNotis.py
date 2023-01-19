#!/usr/bin/env python3
# MindfulNotis.py
# web scraper for youtube and spotify to notify me by email when something I actually care about happens
# Brendan Inglis
# January 2023

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import ssl
import smtplib
from email.message import EmailMessage
import requests
import zipfile
import shutil

# ssl._create_default_https_context = ssl._create_unverified_context

# Get latest chromedriver zip file for mac, extract into same folder
try:
    version = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE').text
    url = 'https://chromedriver.storage.googleapis.com/{0}/{1}'.format(version, 'chromedriver_mac64.zip')
    r = requests.get(url, allow_redirects=True)
    open('chromedriver.zip', 'wb').write(r.content)
    with zipfile.ZipFile("chromedriver.zip", "r") as zip_ref:
        zip_ref.extractall()

    # Place chromedriver in the cron job path
    shutil.copyfile('chromedriver','/usr/local/bin')
except:
    pass

# Google app password
pw = 'Your_App_Pwd_Here' # this must be set generated on your Google profile security settings
email = 'Email_Here' # In this case, I only provide one email address because I am messaging myself

# Chrome/Selenium Option
options = webdriver.ChromeOptions()
options.add_argument('headless')
# declare driver as chrome headless instance
driver = webdriver.Chrome(options=options)
# Initialize web driver wait
wait = WebDriverWait(driver, 10)

# URLS for checking new releases - create a dictionary containing the name of the channel and the link to the channels "Videos" page
# I have two examples here
yt = {
    'Wintergatan': 'https://www.youtube.com/@Wintergatan/videos',
    'Adam Neely': 'https://www.youtube.com/@AdamNeely/videos'
}

def send_email(url_pairs):
  
    # Create a text/plain message
    msg = EmailMessage()
    # initialize message
    body = ''
    for pair in url_pairs:
        individual = 'Here is the latest video from ' + pair[0] + ':\n' + pair[1] + '\n\n'
        body = body + individual

    msg.set_content(body)

    msg['Subject'] = 'New Video Alert!'
    msg['From'] = email
    msg['To'] = email

    # Use SMTP library to send the email
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email,pw)
        smtp.sendmail(email,email, msg.as_string())

# YouTube video info scraper. Writes to a data structure
def scrape_vids():
    data = []
    try:
        for e in WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#details'))):
            title = e.find_element(By.CSS_SELECTOR, 'a#video-title-link').get_attribute('title')
            vurl = e.find_element(By.CSS_SELECTOR, 'a#video-title-link').get_attribute('href')
            views = e.find_element(By.XPATH,
                                    './/*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][1]').text
            date_time = e.find_element(By.XPATH,
                                    './/*[@id="metadata"]//span[@class="inline-metadata-item style-scope ytd-video-meta-block"][2]').text
            data.append({
             'video_url': vurl,
                'title': title,
                'date_time': date_time,
                'views': views
            })
    except:
        pass

    # Most Recent Videos Publish Date
    recent_vid = data[0].get('date_time')
    link = data[0].get('video_url')

    # Split string to get info
    split_time = recent_vid.split(" ")

    # Determine if the video was publishd in the last week (note, must be in conjunction with cron job)
    if split_time[1] == 'hours' or split_time[1] == 'days':
        return True, link
    elif split_time[1] == 'weeks' and int(split_time[0]) < 2:
        return True, link
    else:
        link = []
        return False, link

'''Main Execution'''
# array of new videos to send
v_array = []

# Counter initalize 
c = 0

# List of YouTube channels (the dict keys)
k_list = list(yt.keys())

# Loop through URL's
for value in yt.values():
    driver.get(value)
    time.sleep(3)

    # Call scraping function
    to_send, url_ = scrape_vids()
    if to_send:
        v_array.append([k_list[c],url_])
    c+=1

 # Send Email if v_array is not empty
if v_array:
  send_email(v_array)
  
