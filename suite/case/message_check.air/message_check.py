# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '簡訊行銷檢查'
__desc__ = '檢查簡訊行銷功能是否可正常進入新增頁面'
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================簡訊功能檢查=============================
def main_message(work_progress):
    try:
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//div[@class='md-list-expand']//div[contains(.,'簡訊行銷')]").click()
        work_progress += 100

    except NoSuchElementException as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    return work_progress
work_progress = main_message(work_progress)