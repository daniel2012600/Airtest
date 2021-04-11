# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '登入頁面檢查'
__desc__ = '確認登入成功'
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================檢查登入功能==========================
def main_login(work_progress):
    try:
        driver.assert_exist("//body", "xpath", "登入成功")
        work_progress += 100
    except AssertionError as e:
        try:
            print(e.args)
            driver.assert_template(Template(r"tpl1596505546554.png", threshold=0.4999999999999999, record_pos=(28.195, 5.54), resolution=(100, 100)), "異常，聯絡工程人員!")
        except Exception as e:
            print(e.args)
            driver.assert_exist("//button[@type='submit']", "xpath", "登入失敗，尚有帳密資訊未填寫或者輸入錯誤")
    except Exception as e:
        print('================================================================')
        print(e.args)
        print('================================================================')
        pass
    return work_progress


work_progress = main_login(work_progress)