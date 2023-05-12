# Example
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import datetime
import smtplib
from email.message import EmailMessage

# Spotify details
SPOTIPY_CLIENT_ID='8996b929c79941c9a16d5a53971b4c28'
SPOTIPY_CLIENT_SECRET='17e4a4c5410f46468c19497b35a62df2'
SPOTIPY_REDIRECT_URI='https://localhost:8888/callback'

# Authenticate/login to spotify API
scope = "user-library-read"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

# Spotify podcasts to scrape
spt = {
    'Your Undivided Attention': '4KI3PtZaWJbAWK89vgttoU', # Spotify show ID
    'The Always Sunny Podcast': '0xDEeqWuoMNBUFGNrhIz6L', # It's always sunny in Philadelphia podcast
    'On Purpose with Jay Shetty': '5EqqB52m2bsr4k1Ii7sStc',
    'Approachable Music': '2d0fpifQoLn230QaGjrW7w'
}

# Google app password
pw = 'blfwsvqfbormfbcj'
email = 'inglisbrendan39@gmail.com'

def no_new_email():
    # Create a text/plain message
    msg = EmailMessage()
    # initialize message
    body = 'No new podcasts this week. Have a great day!'

    msg.set_content(body)

    msg['Subject'] = 'No New Podcasts This Week!'
    msg['From'] = email
    msg['To'] = email

    # context = ssl.create_default_context()
    # with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, pw)
        smtp.sendmail(email, email, msg.as_string())

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
                         'description'] + '\n\n'

        body = body + individual

    msg.set_content(body)

    msg['Subject'] = 'New Podcast Alert!'
    msg['From'] = email
    msg['To'] = email

    # Send email with SMTP
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email,pw)
        smtp.sendmail(email,email, msg.as_string())

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

    # Query release date and find difference from today
    t_split = (data[0]['r_date'].split('-'))
    y = int(t_split[0])
    m = int(t_split[1])
    d = int(t_split[2])

    # Release of podcast latest episode
    latest_release = datetime.datetime(y,m,d)

    # current date
    todays_date = datetime.datetime.today()

    # Difference between today's date and the release date
    date_diff = str(todays_date-latest_release).split(' ')

    # Error handling if less than 1 day difference
    if len(date_diff) == 1:
        day_diff = 0
    else:
        # Get num of days
        day_diff = int(date_diff[0])

    # If it has been over a week
    if day_diff <= 7:
        return True, data
    else:
        return False, data

'''MAIN EXECUTION'''
# array of new podcasts to send
p_array = []

# Initialize counter
c = 0

# List of Spotify Podcasts (keys of dict)
p_list = list(spt.keys())

# Run scraper for podcasts in array
for val in spt.values():
    to_send, data = pod_scrape(val)

    if to_send:
        p_array.append(data)
    c+=1

# Send Email if v_array is not empty
if p_array:
    print("Sending Email")
    send_email(p_array)
else:
    no_new_email()