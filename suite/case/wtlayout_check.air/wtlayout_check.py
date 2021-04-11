# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '悟饕總覽頁面檢查'
__desc__ = '確認全國、區域、門店總覽頁面頁面是否正常呈現'
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =====================悟饕總覽頁面檢查========================
def wtlayout_main(work_progress):
    try:
        if exe_time == '07':
            WebDriverWait(driver,10).until(lambda driver:driver.find_element_by_id("loading-mask"))
            # id = 'loading-mask'
            work_progress += 50
            driver.assert_exist("loading-mask", "id", "此頁面若存在代表正常")
            work_progress += 50
        else:
            # 檢查全國總覽
            driver.get('https://cdppj-sit.eagleeye.com.tw/wt_national')
            WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='mainbox']"))
            driver.assert_exist("//div[@class='mainbox']", "xpath", "全國總覽頁面正常!")
            sleep(2)
            work_progress += 20
            # 檢查區域總覽
            driver.get('https://cdppj-sit.eagleeye.com.tw/wt_district')
            WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='mainbox']"))
            driver.assert_exist("//div[@class='mainbox']", "xpath", "區域總覽頁面正常!")
            sleep(2)
            work_progress += 30
            # 檢查門店總覽
            driver.get('https://cdppj-sit.eagleeye.com.tw/wt_store')
            WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='mainbox']"))
            driver.assert_exist("//div[@class='mainbox']", "xpath", "門店總覽頁面正常!")
            sleep(2)
            work_progress += 50
    except AssertionError as e:
        ser.find_JSerror(driver)
        try:
            print(e.args)
            driver.assert_template(Template(r"tpl1596505546554.png", threshold=0.4999999999999999, record_pos=(28.195, 5.54), resolution=(100, 100)), "異常，聯絡工程人員!")
        except Exception as e:
            print(e.args)
            driver.assert_exist("//button[@type='submit']", "xpath", "登入失敗，尚有帳密資訊未填寫或者輸入錯誤")
    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(e.args)
        print('================================================================')
        pass
    return work_progress

work_progress = wtlayout_main(work_progress)