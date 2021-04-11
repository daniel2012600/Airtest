# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '自訂受眾檢查'
__desc__ = '''檢查自訂受眾:
一、新增受眾
二、選取條件組合，確認查詢功能是否正常
三、取消條件後是否原有條件消失或異常
四、檔案下載
五、刪除受眾
悟饕7點則檢查:
一、新增功能
二、刪除功能
'''
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================檢查自訂受眾=============================
class Ca_Tool():
    def del_files(self,path):
        for root , dirs, files in os.walk(path):
            for name in files:
                if ("daniel" in name):
                    os.remove(os.path.join(root, name))
                    print ("Delete File: " ,os.path.join(root, name))
                elif ("忠實老會員(VVIP)" in name):
                    os.remove(os.path.join(root, name))
                    print ("Delete File: " ,os.path.join(root, name))
                elif ("QA測試" in name):
                    os.remove(os.path.join(root, name))
                    print ("Delete File: " ,os.path.join(root, name))
        
def main_ca(work_progress):
    try:
        CT = Ca_Tool()
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//button[contains(.,'自訂受眾')]").click()
        dfx("//button[contains(.,'新增')]").click()
        work_progress += 20
        dfx("(//div[@class='el-form-item__content']//input[@class='el-input__inner'])[1]").send_keys("daniel")
        dfx("//div[@class='el-form-item__content']//textarea").send_keys("測試功能是否運作正常")
        # 選取條件
        dfx("//div[@class='el-cascader']//input[@class='el-input__inner']").click()
        dfx('//div[@class="el-popper el-cascader__dropdown"]//span[contains(text(),"消費行為")]').click()
        dfx('//div[@class="el-popper el-cascader__dropdown"]//span[contains(text(),"消費商品名稱包含")]').click()
        dfx("(//div[@class='el-select'])[4]").click()
        dfx("//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']//span[contains(text(),'幾天前')]").click()
        dfx("(//div[@class='el-input']//input)[4]").send_keys("daniel")
        # 增加第二條件
        dfx("(//button[contains(.,'增加')])[1]").click()
        dfx("(//input[@class='el-input__inner'])[12]").click()
        dfx('(//div[@class="el-popper el-cascader__dropdown"]//span[contains(text(),"會員資訊")])[2]').click()
        dfx('//div[@class="el-popper el-cascader__dropdown"]//span[contains(text(),"性別")]').click()
        dfx("(//input[@class='el-input__inner'])[19]").click()
        dfx("//ul//li[contains(.,'女')]").click()
        # 增加第三條件並做刪除條件測試
        dfx("(//button[contains(.,'增加')])[1]").click()
        dfx("(//input[@class='el-input__inner'])[21]").click()
        dfx('(//div[@class="el-popper el-cascader__dropdown"]//span[contains(text(),"演算法")])[3]').click()
        dfx("//ul//li[contains(.,'最近消費(R)')]").click()
        dfx("(//div[@class='el-select'])[15]").click()
        dfx("(//div[@class='el-select-dropdown__wrap el-scrollbar__wrap']//span[contains(text(),'一週內')])[2]").click()
        dfx("(//div[@class='el-select'])[16]").click()
        dfx("//ul//li[contains(.,'>')]").click()
        dfx("(//input[@class='el-input__inner'])[28]").click()
        dfx("//ul//li[contains(.,'2')]").click()
        driver.assert_exist("(//div[@class='el-col el-col-24'])[1]", "xpath", "當前條件")
        dfx("(//button[contains(.,'cancel')])[4]").click()
        check_condition = dfx("(//div[@class='el-col el-col-24'])[1]").text
        assert_equal(check_condition,"包含「 1天前 消費商品名稱包含 daniel 」 、 包含「 性別 女 」","取消最近消費(R)條件後原有條件無異常")
        # 增加第四條件
        dfx("(//button[contains(.,'增加')])[1]").click()
        dfx("(//div[@class='el-select'])[12]").click()
        dfx("(//ul//li[contains(.,'排除')])[3]").click()
        dfx("(//input[@class='el-input__inner'])[21]").click()
        dfx('(//div[@class="el-popper el-cascader__dropdown"]//span[contains(text(),"AI")])[3]').click()
        dfx("//ul//li[contains(.,'回購預測')]").click()
        dfx("(//input[@class='el-input__inner'])[28]").click()
        dfx("//ul//li[contains(.,'未來 30 天內不會消費')]").click()

        work_progress += 20
        # 檢視查詢功能
        if exe_owner == 'wt' and exe_time == '07':
            dfx("//button[@class='el-button el-button--default']//span[contains(.,'儲存')]").click()
        else:
            dfx("//button[@class='el-button el-button--primary']//span[contains(.,'查詢受眾')]").click()
            body = driver.find_element_by_css_selector('body')
            body.click()
            body.send_keys(Keys.END)
            driver.assert_template(Template(r"tpl1597890803983.png", threshold=0.49999999999999983, record_pos=(28.225, 8.015), resolution=(100, 100)), "查詢功能正常")
            dfx("//button[@class='el-button el-button--default']//span[contains(.,'儲存')]").click()
        work_progress += 20
        wait_result = WebDriverWait(driver,30).until( EC.text_to_be_present_in_element((By.XPATH,"//tr[@class='el-table__row']//a[contains(text(),'daniel')]" ), u'daniel'))
        # 下載檔案
        driver.assert_exist("(//tr[@class='el-table__row']//a[contains(.,'daniel')])[2]", "xpath", "新增成功")
        WebDriverWait(driver,30).until( EC.text_to_be_present_in_element((By.XPATH,"//tr[@class='el-table__row']//a[contains(.,'daniel')]/../../..//td[@class='el-table_1_column_7  ']" ), u'0'))
        dfx("(//a[contains(.,'daniel')]/../../..//div[@class='cell'])[1]").click()
        dfx("//button[@class='el-button el-button--default']").click()
        dfx("(//div[@class='el-dialog__footer']//span[@class='el-checkbox__label'])[2]").click()
        driver.execute_script("document.getElementsByClassName('el-button el-button--primary')[4].click()") # 下載按鈕
        work_progress += 20
        sleep(3)
        download_dir = r"C:/Users/Daniel/Downloads"
        msg = dfx("//div[@class='el-message el-message--success is-closable']").text
        assert_equal( msg,"請確認資料下載，並妥善保管個人資料",'檔案下載成功')
        CT.del_files(download_dir)
        # 刪除受眾
        dfx("//button[contains(.,'刪除')]").click()
        dfx("//button[contains(.,'確定')]").click()
        work_progress += 20
    except AssertionError as e:
        ser.find_JSerror(driver)
        driver.assert_exist("//body", "xpath", '確認斷言失敗畫面' )
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')

    except TimeoutException as e :
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')

    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')

    return work_progress

work_progress = main_ca(work_progress)






# =======================檢視目錄最新更新時間=============================
# import os
# import shutil
# import time
# def listdir(path, list_name): #傳入儲存的list
#   for file in os.listdir(path):
#     file_path = os.path.join(path, file)
#     if os.path.isdir(file_path):
#         listdir(file_path, list_name)
#     else:
#         list_name.append((file_path,os.path.getctime(file_path)))

# def newestfile(target_list):
#     newest_file = target_list[0]
#     for i in range(len(target_list)):
#         if i < (len(target_list)-1) and newest_file[1] < target_list[i+1][1]:
#             newest_file = target_list[i+1]
#         else:
#             continue
#     return newest_file

# # =======================確認檔案下載成功及刪除=============================
# def check_file(download_dir):
#     list = []
#     listdir(download_dir, list)
#     new_file = newestfile(list)
#     t = time.localtime()
#     now = int(time.mktime(t))
#     file_ctime= int(new_file[1])
#     if now - file_ctime <= 10:
#         return True
#     else:
#         return False

# def del_files(path):
#     for root , dirs, files in os.walk(path):
#         for name in files:
#             print(name)
#             if ("daniel" in name):
#                 os.remove(os.path.join(root, name))
#                 print ("Delete File: " ,os.path.join(root, name))