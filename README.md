# Mindful Notification Customizer
I enjoy learning from YouTube videos, but I hate falling into YouTube rabbit holes. Everyone has been there - first you're watching a video about the James Webb Space Telescope, next thing you know 4 hours later you somehow ended up 3 hours into a flat-earth conspiracy video narrated entirely with textbox subtitles that only has 27 views. I want to watch videos that genuinely interest me, but I don't want to have to open youtube.com to check if my favorite creators have posted. That's where this comes in!

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

## Things to Implement
- SSL safety: currently I am running SMTP without SSL which is unsafe, but I have no sensitive information on the sites I am scraping. I keep getting an error involving SSL certificartes, which seems to be common but I haven't handled it yet.
```
[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate
```
- Open to suggestions!
