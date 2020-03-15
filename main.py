# Import libraries
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup
import schedule
import time
import unicodedata
import os

load_dotenv()

def job():

    # TELEGRAM CREDENTIALS
    api_key = os.getenv("TELEGRAM_BOT_API_KEY")
    chat_id = "@krstonksspin"

    # WEBSITE URL
    bithumb_url = "https://www.bithumb.com/"
    binance_url = "https://www.binance.sg/en"
    kebhana_url = "https://www.kebhana.com/easyone_index_en.html"

    # CALL BITHUMB URL
    response_bithumb = requests.get(bithumb_url)

    # INITIALISE BS4 ON BITHUMB RESPONSE
    soup = BeautifulSoup(response_bithumb.content, "html.parser")
    bithumb = soup.find("strong", id = "assetRealETH_KRW")
    bithumb_rate = bithumb.attrs['data-sorting']
    
    # SANITISE BITHUMB ETH RATE
    string_bithumb_rate = unicodedata.normalize('NFKD', bithumb_rate).encode('ascii','ignore')

    # SEND TO TELE BITHUMB
    # requests.get("https://api.telegram.org/bot" + str(api_key) +"/sendMessage?chat_id=" + str(chat_id) + "&text=" + str(string_bithumb_rate))
    
    # INITIALISE CHROME SESSION
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=options)
    driver2 = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=options)

    # CALL BINANCE URL
    driver.get(binance_url)
    driver.implicitly_wait(2000)

    # INITIALISE BS4 ON BINANCE RESPONSE
    time.sleep(4)
    soup2 = BeautifulSoup(driver.page_source, "html.parser")
    crypto_price = soup2.find_all("span", attrs={"class": "price"})

    # SEND TO TELE BITHUMB
    # requests.get("https://api.telegram.org/bot" + str(api_key) +"/sendMessage?chat_id=" + str(chat_id) + "&text=" + str(crypto_price))
    driver.quit()
    time.sleep(2)

    #KEB HANA
    driver2.get(kebhana_url)
    driver2.implicitly_wait(2000)
    time.sleep(4)
    element_to_hover_over = driver2.find_element_by_xpath('//*[@id="kebWrapper"]/div[2]/a')
    hover = ActionChains(driver2).move_to_element(element_to_hover_over)
    hover.perform()
    time.sleep(2)
    driver2.find_element_by_xpath('//*[@id="kebWrapper"]/div[2]/div/ul/li[4]/a').send_keys(Keys.CONTROL + Keys.RETURN)
    window_after = driver2.window_handles[1]
    driver2.switch_to.window(window_after)
    time.sleep(10)
    keb_soup = BeautifulSoup(driver2.page_source, "html.parser")
    kebhana = keb_soup.find("div", id = "searchContentDiv")
    kebhana_data = kebhana.find_all("tr")
    kebhana_data2 = kebhana_data[11].find_all("td")
    
    # CONVERT DATA TO FLOATS
    bi_eth = float(crypto_price[1].string.strip('SGD'))
    keb_rate = float(kebhana_data2[5].string)
    bithumb_eth = float(string_bithumb_rate.replace(',', ''))

    # CALCULATE PREMIUM
    compute = ((((bithumb_eth/keb_rate)/bi_eth)*100) - 100)

    # SEND ALERT TO TELGRAM BOT
    text = "ETH@BINANCE: " + str(bi_eth) + "\r\n" +"ETH@BITHUMB: " + str(bithumb_eth) + "\r\n" + "KEBHANA SGD/KRW: " + str(keb_rate) + "\r\n" + "PREMIUM: " + str(compute) + "%"
    requests.get("https://api.telegram.org/bot" + str(api_key) +"/sendMessage?chat_id=" + str(chat_id) + "&text=" + str(text))
    driver2.quit()

# RUN CRON EVERY 5 MINUTE
schedule.every(5).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(3)












