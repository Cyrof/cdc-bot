# This project is to create a bot to crawl in the cdc website to book lessons and/or tests

''' Prerequisites
1. -- Driver (e.g. Chrome, Firefox)
2. -- Python venv
3. -- Selenium

'''
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as ffOptions
import time
# from selenium import webdriver

# driver = webdriver.Firefox()

# driver.get("https://www.youtube.com")

class Bot:
    def __init__(self):
        self.url = None
        self.ffOptions = None
        self.driver = None

    def get_url(self):
        self.driver.get(self.url)
    
    def setup_driver(self, opt):
        if opt is not None:
            self.ffOptions = ffOptions()
            for o in opt:
                print('working')
                try:
                    self.ffOptions.add_argument(o)
                except Exception as e:
                    print(e)
            print('still working')
            self.driver = webdriver.Firefox(options=self.ffOptions)
            self.driver.set_page_load_timeout(30)
            print('working done')
        else:
            self.driver = webdriver.Firefox()
            self.driver.set_page_load_timeout(30)
            print('done')
    
    def login(self):
        login_btn = self.driver.find_element(By.CLASS_NAME, 'login-btn')
        login_btn.click()
    
    def start(self, opt=None, **data):
        self.setup_driver(opt=opt)
        time.sleep(3)
        for o in data:
            if o == 'url':
                self.url = data[o]

        time.sleep(3)
        self.get_url()

        time.sleep(10)
        self.driver.close()

if __name__ == "__main__":
    b = Bot()
    options = ['Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0']
    # url="https://www.cdc.com.sg"
    url="https://www.youtube.com"
    b.start(options, url=url)