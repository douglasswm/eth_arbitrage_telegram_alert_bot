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
    coincola_url = "https://www.coincola.com/sell-ethereum?country_code=CN&pageNo=1"

    # CALL COINCOLA URL
    response_coincola = requests.get(coincola_url)

    # INITIALISE BS4 ON COINCOLA RESPONSE
    coincola_soup = BeautifulSoup(response_coincola.content, "html.parser")
    coincola = coincola_soup.find("div", class_ = "jsx-4262417281 price")

    # SANITISE COINCOLA ETH RATE
    string_coincola = unicodedata.normalize('NFKD', coincola.text).encode('ascii','ignore')

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
    driver.implicitly_wait(1000)

    # INITIALISE BS4 ON BINANCE RESPONSE
    time.sleep(4)
    soup2 = BeautifulSoup(driver.page_source, "html.parser")
    time.sleep(1)
    crypto_price = soup2.find_all("span", attrs={"class": "price"})

    # SEND TO TELE BITHUMB
    # requests.get("https://api.telegram.org/bot" + str(api_key) +"/sendMessage?chat_id=" + str(chat_id) + "&text=" + str(crypto_price))
    driver.quit()
    time.sleep(2)

    #KEB HANA
    driver2.get(kebhana_url)
    driver2.implicitly_wait(1000)
    time.sleep(4)
    element_to_hover_over = driver2.find_element_by_xpath('//*[@id="kebWrapper"]/div[2]/a')
    time.sleep(1)
    hover = ActionChains(driver2).move_to_element(element_to_hover_over)
    time.sleep(1)
    hover.perform()
    time.sleep(2)
    driver2.find_element_by_xpath('//*[@id="kebWrapper"]/div[2]/div/ul/li[4]/a').send_keys(Keys.CONTROL + Keys.RETURN)
    time.sleep(1)
    window_after = driver2.window_handles[1]
    driver2.switch_to.window(window_after)
    time.sleep(1)
    keb_soup = BeautifulSoup(driver2.page_source, "html.parser")
    time.sleep(1)
    kebhana = keb_soup.find("div", id = "searchContentDiv")
    time.sleep(1)
    kebhana_data = kebhana.find_all("tr")
    if kebhana_data == []:
        kebhana_data_re = kebhana.find_all("tr")
        print("FAIL")
        print(kebhana_data_re)
        time.sleep(1)
        kebhana_data2 = kebhana_data_re[11].find_all("td")
        time.sleep(1)
        driver2.quit()
        # CONVERT DATA TO FLOATS
        cola_eth = float(string_coincola.strip('CNY'))
        bi_eth = float(crypto_price[1].string.strip('SGD'))
        keb_rate = float(kebhana_data2[5].string)
        bithumb_eth = float(string_bithumb_rate.replace(',', ''))
        cny_rate_5 = float('5')
        cny_rate_49 = float('4.9')

        # CALCULATE PREMIUM
        compute = ((((bithumb_eth/keb_rate)/bi_eth)*100) - 100)
        compute_cola_5 = ((((cola_eth/cny_rate_5)/bi_eth)*100) - 100)
        compute_cola_49 = ((((cola_eth/cny_rate_49)/bi_eth)*100) - 100)

        # SEND ALERT TO TELGRAM BOT
        text = "KOREA MARKET" + "\r\n\r\n" + "ETH@BINANCE_SG: " + str(bi_eth) + "\r\n" +"ETH@BITHUMB: " + str(bithumb_eth) + "\r\n" + "KEBHANA SGD/KRW: " + str(keb_rate) + "\r\n" + "PREMIUM: " + str(compute) + "%"
        text2 = "CHINA MARKET" + "\r\n\r\n" + "ETH@BINANCE_SG: " + str(bi_eth) + "\r\n" + "ETH@COINCOLA: " + str(cola_eth) + "\r\n" + "PREMIUM@SGD/CNY[4.9]: " + str(compute_cola_49) + "%" + "\r\n" + "PREMIUM@SGD/CNY[5.0]: " + str(compute_cola_5) + "%"
        requests.get("https://api.telegram.org/bot" + str(api_key) +"/sendMessage?chat_id=" + str(chat_id) + "&text=" + str(text))
        time.sleep(1)
        requests.get("https://api.telegram.org/bot" + str(api_key) +"/sendMessage?chat_id=" + str(chat_id) + "&text=" + str(text2))
    else:
        print("PASS")
        print(kebhana_data)
        time.sleep(1)
        kebhana_data2 = kebhana_data[11].find_all("td")
        time.sleep(1)
        driver2.quit()
        # CONVERT DATA TO FLOATS
        cola_eth = float(string_coincola.strip('CNY'))
        bi_eth = float(crypto_price[1].string.strip('SGD'))
        keb_rate = float(kebhana_data2[5].string)
        bithumb_eth = float(string_bithumb_rate.replace(',', ''))
        cny_rate_5 = float('5')
        cny_rate_49 = float('4.9')

        # CALCULATE PREMIUM
        compute = ((((bithumb_eth/keb_rate)/bi_eth)*100) - 100)
        compute_cola_5 = ((((cola_eth/cny_rate_5)/bi_eth)*100) - 100)
        compute_cola_49 = ((((cola_eth/cny_rate_49)/bi_eth)*100) - 100)

        # SEND ALERT TO TELGRAM BOT
        text = "KOREA MARKET" + "\r\n\r\n" + "ETH@BINANCE_SG: " + str(bi_eth) + "\r\n" +"ETH@BITHUMB: " + str(bithumb_eth) + "\r\n" + "KEBHANA SGD/KRW: " + str(keb_rate) + "\r\n" + "PREMIUM: " + str(compute) + "%"
        text2 = "CHINA MARKET" + "\r\n\r\n" + "ETH@BINANCE_SG: " + str(bi_eth) + "\r\n" + "ETH@COINCOLA: " + str(cola_eth) + "\r\n" + "PREMIUM@SGD/CNY[4.9]: " + str(compute_cola_49) + "%" + "\r\n" + "PREMIUM@SGD/CNY[5.0]: " + str(compute_cola_5) + "%"
        requests.get("https://api.telegram.org/bot" + str(api_key) +"/sendMessage?chat_id=" + str(chat_id) + "&text=" + str(text))
        time.sleep(1)
        requests.get("https://api.telegram.org/bot" + str(api_key) +"/sendMessage?chat_id=" + str(chat_id) + "&text=" + str(text2))

# RUN CRON EVERY 4 MINUTE
schedule.every(4).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)












