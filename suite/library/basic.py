# -*- coding:utf8 -*-

from airtest.core.api import *
from selenium import webdriver
from selenium.common import exceptions
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException , StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from airtest_selenium.proxy import WebChrome
from pydash import py_
import os,sys
import traceback
import re
import datetime
import shutil
import time
import random
class CaseService():
# ======================偵測JSerror==========================
    def find_JSerror(self,driver,title=None):
        error = driver.get_log('browser')
        result = 'nothing'
        if len(error) != 0:
            try:
                message = py_.map_(error, 'message')
                str1 = ''.join(str(e) for e in message)
                message = str1.replace('()','<br>')
                refresh_condition = "Failed to load resource: the server responded with a status of"
                if re.findall(refresh_condition, message):
                    driver.refresh()
                else:
                    if title == None:
                        driver.assert_exist("//body", "xpath", "有JSError! ") 
                    else:
                        driver.assert_exist("//body", "xpath", "有JSError! : %s" % title ) 
                    result = 'warning'
                    assert_equal(False,True,"JSerror:<br>%s"%(message))
            except:
                pass
            finally:
                return result
            
    # ======================等待頁面加載完成======================
    def check_loading(self,driver):
        while True:
            check = driver.execute_script('return document.readyState;')
            sleep(2)
            if check == 'complete':
                break
            
    # =======================偵錯方法=============================
    def _error_msg(self,e):
        error_class = e.__class__.__name__ #取得錯誤類型
        detail = e.args[0] #取得詳細內容
        cl, exc, tb = sys.exc_info() #取得Call Stack
        lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
        fileName = lastCallStack[0] #取得發生的檔案名稱
        lineNum = lastCallStack[1] #取得發生的行號
        funcName = lastCallStack[2] #取得發生的函數名稱
        errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
        return errMsg
