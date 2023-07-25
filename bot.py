# This project is to create a bot to crawl in the cdc website to book lessons and/or tests

""" Prerequisites
1. -- Driver (e.g. Chrome, Firefox)
2. -- Python venv
3. -- Selenium

"""
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as ffOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import requests
from bs4 import BeautifulSoup
import random
import os
from dotenv import load_dotenv

# from selenium import webdriver

# driver = webdriver.Firefox()

# driver.get("https://www.youtube.com")


class Bot:
    def __init__(self, **opt):
        self.url = None
        self.ffOptions = self.setup_driver(opt)
        self.proxy = self.get_proxy()
        self.driver = (
            webdriver.Firefox(options=self.ffOptions)
            if self.ffOptions is not None
            else webdriver.Firefox()
        )
        load_dotenv()
        

    def get_proxy(self):
        res = requests.get('https://free-proxy-list.net/')
        soup = BeautifulSoup(res.text, 'html.parser')
        table = soup.find('table', {'class', 'table-bordered'})
        rows = table.find_all('tr')
        proxies = []
        for row in rows[1:]:
            cols = row.find_all('td')
            proxies.append(cols[0].text + ':' + cols[1].text)

        return proxies

    def get_url(self):
        self.driver.get(self.url)

    def setup_driver(self, opt):
        profile = webdriver.FirefoxProfile()
        options = ffOptions()
        for k in opt:
            if opt[k] == "user-agent":
                profile.set_preference("general.useragent.override", opt[k])
            elif opt[k] == 'proxy':
                proxy = random.choice(self.proxy).split(':')
                options.set_preference('network.proxy.type', 1)
                options.set_preference('network.proxy.socks', proxy[0])
                options.set_preference('network.proxy.socks_port', int(proxy[1]))
                # profile.set_preference('network.proxy.socks_remote_dns', False)
        options.profile = profile
        return options

    def login(self):
        time.sleep(20)
        self.driver.find_element(By.XPATH, '/html/body/div[3]/div/ul/li[10]/a').click() # click login btn
        time.sleep(5)
        self.driver.find_element(By.XPATH, '//*[@id="userId"]').send_keys(os.getenv('LEARNER_ID')) # input learner id
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(os.getenv('PASS')) # input password
        time.sleep(5)
        WebDriverWait(self.driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[name^='a-'][src^='https://www.google.com/recaptcha/api2/anchor?']")))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='recaptcha-anchor']"))).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, '//*[@id="BTNSERVICE2"]').click()

    def start(self, **data):
        time.sleep(3)
        for o in data:
            if o == "url":
                self.url = data[o]

        time.sleep(3)
        self.get_url()

        self.login()

        time.sleep(10)
        self.driver.close()


if __name__ == "__main__":
    # options = ['Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0']
    options = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "proxy": True
    }
    b = Bot(opt=options)

    url="https://www.cdc.com.sg"
    # url = "https://www.youtube.com"
    b.start(url=url)
