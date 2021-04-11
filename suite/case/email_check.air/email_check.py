# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = 'Email行銷檢查'
__desc__ = '確認用戶可否正常進入email行銷頁面'
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================檢查email功能=============================
def main_email(work_progress):
    try:
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//div[@class='md-list-expand']//div[contains(text(),'Email行銷')]").click()
        work_progress += 50

        title = dfx("//h2[contains(.,'Email行銷')]").text
        work_progress += 50

    except TimeoutException as e: 
        driver.assert_exist("//body", "xpath", "元素不存在")
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    except AssertionError as e:
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    except NoSuchElementException as e:
        driver.assert_exist("//body", "xpath", "找不到元素")
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    except Exception as e:
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        driver.assert_exist("//body", "xpath", "確認頁面是否正常呈現")
    return work_progress

work_progress = main_email(work_progress)