# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '智慧名單檢查'
__desc__ = '確認智慧名單資料更新日期'
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================檢查智慧名單==========================
def check_BI_list(index):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    yesterday = today - oneday
    match= re.search(r'(\d+-\d+-\d+)',index)
    index_day = match.group(1)
    if exe_owner == 'wt' and exe_time == '07':
        if index_day == str(yesterday):
            return True
        else:
            return False
    else:
        if index_day == str(today):
            return True
        else:
            return False
            
def main_BI(work_progress):
    try:
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//*[@id=\"list_ta\"]/div/div[2]/ul/li/button/div").click()
        work_progress += 50
        index = dfx("//*[@id=\"rule_layout\"]/div/div/main/div[2]/div/div/div[3]/div/div/div/div[2]/div/div[3]/table/tbody/tr/td[4]/div").text
        if exe_owner == 'wt' and  exe_time == '07':
            assert_equal(check_BI_list(index),True,"確認日期是否為執行日前一天,日期為:%s"%(index))
        else:
            assert_equal(check_BI_list(index),True,"確認日期是否為執行日當天,日期為:%s"%(index))
        work_progress += 50
        
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
        print('================================================================')
        ser.find_JSerror(driver)
        print(ser._error_msg(e))
        print('================================================================')
        driver.assert_exist("//body", "xpath", "確認頁面是否正常呈現")
    finally:
        return work_progress

work_progress = main_BI(work_progress)
