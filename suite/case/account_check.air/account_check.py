# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '帳號列表檢查'
__desc__ = '''
一、新增帳號
二、批次新增帳號(僅測cdppj)
三、查詢帳號
四、刪除帳號
'''
# ========================module==============================
from library.basic import CaseService
import win32gui
import win32con
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
upload_path = r"C:\airtest_develop\suite\QA_Tool\account_multi_batch_list.xlsx"
# =======================檢查帳號列表==========================
def main_account(work_progress):
    try:
        # 進入帳號列表頁
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//div[@class='md-list-expand']//div[contains(text(),'帳號列表')]").click()
        
        # 新增帳號
        driver.execute_script("document.getElementsByClassName('el-button button-md el-button--primary')[1].click()")
        dfx("(//input[@class='el-input__inner'])[3]").send_keys("QAtest_1")
        dfx("(//input[@class='el-input__inner'])[4]").send_keys("QAtest_1+%s@reddoor.com.tw" % exe_owner)
        dfx("//input[@readonly='readonly']").click()
        dfx("//div[@class='el-scrollbar']//span[contains(text(),'管理員')]").click()
        dfx("//button[contains(.,'確定')]").click()
        ser.check_loading(driver)
        work_progress += 25

        # 批次新增帳號
        if exe_owner == 'cdppj':
            driver.execute_script("document.getElementsByClassName('el-button button-md el-button--primary')[0].click()")
            dfx("//div[@class='cdp-upload']").click()
            dialog = win32gui.FindWindow('#32770', u'開啟') # 對話方塊
            ComboBoxEx32 = win32gui.FindWindowEx(dialog, 0, 'ComboBoxEx32', None) 
            ComboBox = win32gui.FindWindowEx(ComboBoxEx32, 0, 'ComboBox', None)
            Edit = win32gui.FindWindowEx(ComboBox, 0, 'Edit', None)
            button = win32gui.FindWindowEx(dialog, 0, 'Button', None) # 確定按鈕Button
            win32gui.SendMessage(Edit, win32con.WM_SETTEXT, None, upload_path )
            sleep(2)
            win32gui.SendMessage(dialog, win32con.WM_COMMAND, 1, button) # 按button
            sleep(2)
            dfx("(//button[contains(.,'確定')])[2]").click()
            dfx("//button[contains(.,'確認')]").click()
            ser.check_loading(driver)
        work_progress += 25

        # 查詢帳號
        dfx("(//input[@class='el-input__inner'])[1]").send_keys("QAtest")
        dfx("//button[contains(.,'查詢')]").click()
        WebDriverWait(driver,20).until(lambda driver:dfx("//td[contains(.,'@reddoor.com.tw')]"))
        QA_cnt = driver.execute_script(" return document.getElementsByClassName('el-table_1_column_1 is-left ').length")
        try:
            if exe_owner == 'cdppj':
                assert_equal( str(QA_cnt),'6', "帳號及批次帳號新增成功，查詢功能正常")
            else:
                assert_equal( str(QA_cnt),'2', "帳號新增成功，查詢功能正常")
        except:
            pass
        work_progress += 25
        
        # 刪除批次帳號
        for index in range( QA_cnt-1 ):
            WebDriverWait(driver,20).until(lambda driver:dfx("//tr[contains(.,'QAtest')]"))
            dfx("(//tr[contains(.,'QAtest')]//span[contains(.,'刪除')])[2]").click()
            name = dfx("//div[@class='text__col text-danger'][1]").text
            dfx("//button[contains(.,'確定')]").click()
            sleep(2)
            msg = dfx("//div[@class='el-message el-message--warning']").text
            assert_equal( msg,"已刪除帳號「%s」" % name,'%s 刪除成功' % name)
        work_progress += 25
    except NoSuchElementException as e:
        ser.find_JSerror(driver)
        driver.assert_exist("//body", "xpath", "確認當前頁面! ") 
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    return work_progress
    
work_progress = main_account(work_progress)





        # # 進入帳號列表頁
        # dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        # dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        # dfx("//div[@class='md-list-expand']//div[contains(text(),'帳號列表')]").click()
        # work_progress += 25
        # # 新增帳號
        # driver.execute_script("document.getElementsByClassName('el-button button-md el-button--primary')[1].click()")
        # dfx("(//input[@class='el-input__inner'])[3]").send_keys("QAtest")
        # dfx("(//input[@class='el-input__inner'])[4]").send_keys("QAtest+%s@test.com" % exe_owner)
        # dfx("//input[@readonly='readonly']").click()
        # dfx("//div[@class='el-scrollbar']//span[contains(text(),'管理員')]").click()
        # dfx("//button[contains(.,'確定')]").click()
        # ser.check_loading(driver)
        # work_progress += 25

        # # 查詢帳號
        # dfx("(//input[@class='el-input__inner'])[1]").send_keys("QAtest")
        # dfx("//button[contains(.,'查詢')]").click()
        # WebDriverWait(driver,20).until(lambda driver:dfx("//td[contains(.,'@test.com')]"))
        # QA_cnt = driver.execute_script(" return document.getElementsByClassName('el-table_1_column_1 is-left ').length")
        # try:
        #     assert_equal( str(QA_cnt),'2', "帳號新增成功，查詢功能正常")
        # except:
        #     pass
        # work_progress += 25

        # # 刪除批次帳號
        # for index in range( QA_cnt-1 ):
        #     WebDriverWait(driver,20).until(lambda driver:dfx("//tr[contains(.,'QAtest')]"))
        #     dfx("(//tr[contains(.,'QAtest')]//span[contains(.,'刪除')])[2]").click()
        #     name = dfx("//div[@class='text__col text-danger'][1]").text
        #     dfx("//button[contains(.,'確定')]").click()
        #     sleep(2)
        #     msg = dfx("//div[@class='el-message el-message--warning']").text
        #     assert_equal( msg,"已刪除帳號「%s」" % name,'%s 刪除成功' % name)
        # work_progress += 25
        