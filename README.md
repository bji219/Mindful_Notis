# Mindful Notification Customizer


### Selenium Web Scraper for YouTube
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

### Cron Job
The whole point of this code is to service as a notification generator. Using cron on my mac will allow me to run this Python code at regular intervals. Run ```crontab -e``` in your terminal to create a recurring job for your computer to run. I have set my cron job to run every monday at 3:33pm. 

```
SHELL=/bin/bash
PATH=/usr/local/bin/:/usr/bin:/usr/sbin
33 15 * * 1 export DISPLAY=:0 && cd /Path/To/Project && python3 MindfulNotis.py
```

### The result
Since the writing of this post, the only video that I am interested which has uploaded within the window I specified was from Wintergatan.

![](/)
