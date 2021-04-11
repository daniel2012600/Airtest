# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '資料同步紀錄檢查'
__desc__ = '''確認資料同步紀錄頁面
order開頭資料筆數增量是否大於0
'''
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# ========================method==============================
def general_check(title_list,data_list):
    for order in title_list:
        order_name =  re.findall( r'^order_.*',order)
        if len(order_name) >=1 :
            order_index = title_list.index(order_name[0])
            data_index = int(order_index) * 2 + 1
            today_order_count = data_list[data_index]
        try:
            if today_order_count != '0':
                assert_equal(True,True,"%s %s 資料筆數增量正常,數值為:%s"%(data_list[0],order_name[0],today_order_count))
            else:
                assert_equal(False,True,"%s %s 資料筆數增量異常,數值為:%s"%(data_list[0],order_name[0],today_order_count))
        except Exception as e:
            ser.find_JSerror(driver)
            print('================================================================')
            print(ser._error_msg(e))
            print('================================================================')

# ======================檢查資料同步紀錄=========================
def main_datasync(work_progress):
    try:
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//div[@class='md-list-expand']//div[contains(text(),'資料同步紀錄 ')]").click()
        work_progress += 20
        title = dfx("(//tr[@data-v-a5e6c936])[1]").text
        title_list = title.split(' ')
        data = dfx("(//tr[@data-v-a5e6c936])[3]").text
        data_list = data.split(' ')
        if exe_owner  == 'mtth':
            mtth_check = driver.execute_script("return obj.datalist[0].資料筆數增量 >= 1300")
            assert_equal(mtth_check,True,"確認馬修每日資料是否遺漏")
        else:
            general_check(title_list,data_list)
        work_progress += 80
    except AssertionError as e:
        driver.assert_exist("//body", "xpath", "日期錯誤或資料未正常導入")
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    except NoSuchElementException as e:
        driver.assert_exist("//body", "xpath", "找不到元素")
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        driver.assert_exist("//body", "xpath", "確認頁面是否正常呈現")
    return work_progress

if exe_owner == 'sck':
    pass
else:
    work_progress = main_datasync(work_progress)