import sys
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

#Korea Meteorological Administration
url = "https://www.weather.go.kr/pews/"
log_file = "log.txt"

simulated_video = False
simulation_status = False
last_origin = ""

#Selenium
browser_driver = Service('/usr/lib/chromium-browser/chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
page_to_scrape = webdriver.Chrome(service=browser_driver, options=chrome_options)
page_to_scrape.get(url)

#Mobius platform info
host = "203.253.128.177"
port = "7579"
ae = "KETIDGZ_earthquake"
con = "web_scrapping"

#Upload earthquake-related data to Mobius platform
def upload(value):
    keti_url = f'http://{host}:{port}/Mobius/{ae}/{con}'
    payload = f'{{\n    "m2m:cin": {{\n        "con": "{value}"\n    }}\n}}'.encode('utf-8')
    headers = {
        'Accept': 'application/json',
        'X-M2M-RI': '12345',
        'X-M2M-Origin': 'SOrigin',
        'Content-Type': 'application/json; ty=4'
    }
    requests.request("POST", keti_url, headers=headers, data=payload)

#Verify for Simulation
def check_sim_status():
    global simulation_status
    if sys.argv[1] == 'simulation':
        simulation_status = True

#Logging
def logging(msg):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a") as file:
        file.write(f"[{current_time}] {msg}\n")

#Connect to Korea Meteorological Administration
def get_connection():
    try:
        time.sleep(3)
        iframe_element = page_to_scrape.find_element(By.ID, 'iframe')
        page_to_scrape.switch_to.frame(iframe_element)
        logging('connection success')
    except:
        logging('connection fail')
        page_to_scrape.get(url)
        get_connection()

#Scraping
def scraping():
    global page_to_scrape
    global url
    global simulated_video
    global simulation_status
    global last_origin

    try:
        #Verify current connection is normal
        time.sleep(5)        
        time_element = page_to_scrape.find_element(By.ID, 'time')
        time_value = time_element.text

        #For simulation, run first time to generate virtual earthquake-related data
        if not simulated_video and simulation_status:
            #Click simulated Video Activation button
            page_to_scrape.find_element(By.XPATH, '//*[@id="fold"]').click()
            #Select historical earthquake cases
            page_to_scrape.find_element(By.XPATH, '//*[@id="body"]/div[5]/div/div[2]/div/ul/li[1]').click()
            logging('play simulated_video')
            time.sleep(30)

        #Get scale data
        scale = page_to_scrape.find_element(By.XPATH, '//*[@id="estScl"]').text
        time.sleep(5)

        #Get origin data
        origin = page_to_scrape.find_element(By.XPATH, '//*[@id="origin"]').text
        time.sleep(5)

        #Get magnitude data
        magnitude = page_to_scrape.find_element(By.XPATH, '//*[@id="estMag"]').text

        #Verify data validation and convert format
        if scale and origin and magnitude:
            if origin != last_origin:
                #Convert data format
                value = scale + "|" + origin + "|" + magnitude
                upload(value)
                last_origin = origin
                logging('http post' + ' value: ' + value)

        simulated_video = True
        logging('scraping success ' + 'server time: ' + time_value)

    except Exception as ex:
        logging('scraping error ' + str(ex))
        get_connection()
        simulated_video = False
        scraping()

def main():
    check_sim_status()
    get_connection()
    while True:
        scraping()

main()
