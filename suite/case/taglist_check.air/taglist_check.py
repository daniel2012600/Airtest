# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '標籤列表檢查'
__desc__ = '''確認標籤列表:
一、新增標籤
二、查詢功能
三、編輯名稱
四、刪除標籤
'''
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================標籤列表檢查==========================
def main_taglist(work_progress):
    try:
        # 進入標籤列表頁面並新增標籤
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//button[contains(.,'標籤列表')]").click()
        WebDriverWait(driver,30).until( EC.visibility_of_element_located((By.XPATH,"//button[contains(.,'查詢')]")))
        dfx("//button[contains(.,'新增')]").click()
        dfx("(//input[@class='el-input__inner'])[3]").send_keys("QA_test")
        dfx("(//button[contains(.,'新增')])[2]").click()
        driver.assert_exist("//td[contains(.,'QA_test')]", "xpath", "新增成功")
        work_progress += 20
        # 查詢新增的標籤
        dfx("//div[@class='el-select__tags']").click()
        dfx("//li[contains(.,'QA_test')]").click()
        dfx("//button[contains(.,'查詢')]").click()
        driver.assert_exist("//td[contains(.,'QA_test')]", "xpath", "查詢功能正常")
        work_progress += 20
        # 編輯標籤名稱
        dfx("(//td[contains(.,'QA_test')]/..//span)[1]").click()
        dfx("//td[contains(.,'QA_test')]/..//span[contains(.,'更多')]").click()
        dfx("//li[contains(.,'修改標籤')]").click()
        dfx("(//input[@class='el-input__inner'])[3]").send_keys("(modify)")
        dfx("//button[contains(.,'修改')]").click()
        driver.assert_exist("//td[contains(.,'QA_test(modify)')]", "xpath", "編輯功能正常")
        sleep(2)
        work_progress += 20
        # 刪除標籤
        dfx("//button[contains(.,'刪除')]").click()
        dfx("//button[contains(.,'確定')]").click()
        msg = dfx("//div[@class='el-message el-message--success']").text
        assert_equal( msg,"刪除成功",'刪除成功')
        work_progress += 40
    except TimeoutException as e: 
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        driver.assert_exist("//body", "xpath", "確認頁面是否正常呈現")
    except AssertionError as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        driver.assert_exist("//body", "xpath", "斷言失敗頁面顯示")
    except NoSuchElementException as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        driver.assert_exist("//body", "xpath", "確認頁面是否正常呈現")
    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        driver.assert_exist("//body", "xpath", "確認頁面是否正常呈現")

    return work_progress

work_progress = main_taglist(work_progress)