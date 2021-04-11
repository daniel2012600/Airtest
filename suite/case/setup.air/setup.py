# -*- coding:utf8 -*-
# ========================module==============================
from library.basic import *
from airtest_selenium.proxy import WebChrome
# ===================設定變數======================
# 設置driver
# Airtest自動建立初始化
auto_setup(__file__)
options = Options()
options.add_argument('--dns-prefetch-disable')
options.add_argument("--disable-features=VizDisplayCompositor")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument('start-maximized')
options.add_argument('enable-automation')
options.add_argument('--no-sandbox')
options.add_argument('--disable-infobars')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-browser-side-navigation')
options.add_argument('--disable-gpu')
options.add_argument('--disable-extensions')

driver = WebChrome(executable_path=chrome,options=options)
driver.implicitly_wait(40)
dfx = driver.find_element_by_xpath
ser = CaseService()

def main_setup():
    try:
        driver.get(test_url)
        driver.maximize_window()
        dfx("//button[@type='submit']").click()
    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(e.args)
        print('================================================================')
        driver.quit()
        
main_setup()
