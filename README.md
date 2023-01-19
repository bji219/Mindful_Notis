# Mindful Notification Customizer
I enjoy learning from YouTube videos, but I hate falling into YouTube rabbit holes. Everyone has been there - first you're watching a video about the James Webb Space Telescope, next thing you know 4 hours later you somehow ended up 3 hours into a flat-earth conspiracy video narrated entirely with textbox subtitles that only has 27 views. I want to watch videos that genuinely interest me, but I don't want to have to open youtube.com to check if my favorite creators have posted. That's where this comes in!

## Features 
- Selenium Web Scraper for YouTube videos
- Spotify Web API interface for Podcasts
- Email notification and message
- Cron Job implementation 

## Selenium Web Scraper for YouTube
I included the meat and potatoes of what is going on below- using Selenium and Chromedriver for Python 3 I find the video metadata on the homepage of the YouTube creators that I specify. 

```python
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
```

## Spotify Web API
Check out the [Spotify Web API](https://developer.spotify.com/documentation/web-api/). You will need to set up some background info on the Spotify Developer portal, but afterwards it is pretty simple. In my case I am using a library called [Spotipy](https://spotipy.readthedocs.io/en/2.22.0/) which is basically a python wrapper for the web API. I used this tool to find podcast metadata for the scraper! See below. 
```python
# Podcast Scraping Function
def pod_scrape(val):
    data = []
    pod = sp.shows([val],market='US')
    des = pod['shows'][0]['html_description']
    pub = pod['shows'][0]['publisher']
    link = pod['shows'][0]['external_urls']['spotify']
    pod_title = pod['shows'][0]['name']

    # Get latest episode metadata from podcast
    show_eps = sp.show_episodes(val,limit=1)
    desc = show_eps['items'][0]['description']
    show_link = show_eps['items'][0]['external_urls']['spotify']
    show_title = show_eps['items'][0]['name']
    show_release = show_eps['items'][0]['release_date']
    ep_num = show_eps['total']
    data.append({
                'pod_title':pod_title,
                'pod_url': show_link,
                'show_title': show_title,
                'authors': pub,
                'r_date': show_release,
                'description': desc,
                'ep_num': ep_num
                })
```

## Emails with Python
This is essentially the same function for both scrapers minus the message text. This isn't exactly safe because we bypass SSL but more on that below.
```python
# Email function
def send_email(data):
    # Create a text/plain message
    msg = EmailMessage()
    # initialize message
    body = ''
    for i in data:
        individual = 'Here is the latest podcast from ' + i[0]['pod_title'] + ':\n\n' + 'Episode #' + str(
            i[0]['ep_num']) + ', \"' + i[0]['show_title'] + '\"\n\n' + i[0][
                         'pod_url'] + '\n\n' + 'Release date: ' + i[0]['r_date'] + '\n\n' + 'Show Notes:\n\n' + i[0][
                         'description']

        body = body + individual

    msg.set_content(body)

    msg['Subject'] = 'New Podcast Alert!'
    msg['From'] = email
    msg['To'] = email

    # Send email with SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email,pw)
        smtp.sendmail(email,email, msg.as_string())
```
A Google App password _must be generated_ for this to interface with Gmail. This can be configured [here](https://myaccount.google.com/security?hl=en). This variable in the code ```pw = '' ``` is looking for the app password, _not_ your normal email account password. 

## Cron Job
The whole point of this code is to service as a notification generator. Using cron on my mac will allow me to run this Python code at regular intervals. Run ```crontab -e``` in your terminal to create a recurring job for your computer to run. I have set my cron job to run every monday at 3:33pm. 

```
SHELL=/bin/bash
PATH=/usr/local/bin/:/usr/bin:/usr/sbin
33 15 * * 1 export DISPLAY=:0 && cd /Path/To/Project && python3 MindfulNotis.py
```

## The result
Since the writing of this post, the only video that was uploaded within the window I specified was from Wintergatan. It is worth noting you can add many channels to your dictionary.

![](/MindfulNoti.png)

![](/SpotiMind.png)

## Features to Implement
- SSL safety: currently I am running SMTP without SSL which is unsafe, but I have no sensitive information on the sites I am scraping. I keep getting an error involving SSL certificartes, which seems to be common but I haven't handled it yet.
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```
- Convert from selenium web scraping to YouTube API calls for faster code
- Open to suggestions!
