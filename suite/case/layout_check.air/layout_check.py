# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '總覽頁面檢查'
__desc__ = '確認總覽頁面是否有資料'
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================檢查總覽畫面=============================
def main_layout(work_progress):
    try:
        if exe_owner == 'wt' and exe_time == '07':
            WebDriverWait(driver,10).until(lambda driver:driver.find_element_by_id("loading-mask"))
            # id = 'loading-mask'
            work_progress += 50
            driver.assert_exist("loading-mask", "id", "此頁面若存在代表正常")
            work_progress += 50
        else:
            WebDriverWait(driver,10).until(lambda driver:dfx("//div[@class='mainbox']"))
            work_progress += 50
            driver.assert_exist("//div[@class='mainbox']", "xpath", "總覽頁面正常!"   ) 
            work_progress += 50

    except TimeoutException as e: 
        print(e.args)
        driver.assert_exist("//body", "xpath", "確認當前頁面!"   ) 
    except AssertionError as e:
        try:
            print(e.args)
            driver.assert_exist("loading-mask", "id", "異常，聯絡工程人員!")
            sleep(5)
        except AssertionError as e:
            print(e.args)
            
        except Exception as e:
            print(e.args)
            driver.assert_exist("//button[@type='submit']", "xpath", "登入失敗，尚有帳密資訊未填寫或者輸入錯誤")
    except Exception  as e:
        print('================================================================')
        print(e.args)
        print('================================================================')
        driver.assert_exist("//body", "xpath", "確認頁面是否正常呈現")

    return work_progress

work_progress = main_layout(work_progress)