# -*- coding:utf8 -*-
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()

def ma_reset():
    driver.refresh()
    driver.get("https://cdppj-sit.eagleeye.com.tw")
    dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
    dfx("//button[contains(.,'行銷自動化')]").click()
    dfx("(//tr[@class='el-table__row']//div[contains(text(),'QA_test')]/../..//span[@class='el-checkbox__input'])[1]").click()
    dfx("//button[contains(.,'刪除')]").click()
    dfx("//div[@class='el-message-box']//span[contains(text(),'確定')]").click()

def account_reset():
    driver.refresh()
    driver.get("https://cdppj-sit.eagleeye.com.tw/account")
    page_number = driver.execute_script("return document.getElementsByClassName('number').length")
    element = "(//input[@class='el-input__inner'])[2]"
    dfx(element).send_keys(Keys.CONTROL+'a')
    dfx(element).send_keys(Keys.BACK_SPACE)
    dfx(element).send_keys(page_number)
    dfx(element).send_keys(Keys.ENTER)
    QA_cnt = len(driver.find_elements_by_xpath("//td//div[@class='name-pic__name'][contains(.,'QAtest_')]"))
    for index in range( QA_cnt ):
        WebDriverWait(driver,20).until(lambda driver:dfx("//tr[contains(.,'QAtest')]"))
        dfx("(//tr[contains(.,'QAtest')]//span[contains(.,'刪除')])[2]").click()
        dfx("//button[contains(.,'確定')]").click()
        sleep(2)

def ca_reset():
    driver.refresh()
    driver.get("https://cdppj-sit.eagleeye.com.tw/customer/customer_rule")
    dfx("(//a[contains(text(),'daniel')]/../../..//div[@class='cell'])[1]").click()
    dfx("//button[contains(.,'刪除')]").click()
    dfx("//button[contains(.,'確定')]").click()

def permission_reset():
    driver.get("https://cdppj-sit.eagleeye.com.tw/account")
    dfx("(//tr[contains(.,'%s')]//button[contains(.,'變更角色')])" % account ).click()
    dfx("(//input[@class='el-input__inner'])[5]").click()
    dfx("//li[contains(.,'管理員')]" ).click()
    dfx("//button[contains(.,'確定')]").click()
    driver.refresh()
    driver.get("https://cdppj-sit.eagleeye.com.tw/account_roles")
    dfx("//div[@class='cell'][contains(.,'測試人員')]/../..//button[contains(.,'刪除')]").click()
    dfx("//button[contains(.,'確定')]").click()

def taglist_reset():
    driver.refresh()
    driver.get("https://cdppj-sit.eagleeye.com.tw/prd_tag_list")
    dfx("(//td[contains(.,'QA_test')]/..//span)[1]").click()
    dfx("//button[contains(.,'刪除')]").click()
    dfx("//button[contains(.,'確定')]").click()

def handdle_error(case):
    try:
        eval(case)
    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')

def main_teardown():
    print('****************************************************')
    print('測試案例 %s 結束' % exe_script)
    print('工作完成率:',work_progress,'%')
    print('****************************************************')
    # 當工作進度未完成，檢查當前腳本是否有必須得還原的項目
    if work_progress < 100 :
        if  exe_script == 'ma_check.air'  :
            handdle_error("ma_reset()")
        elif  exe_script == 'account_check.air' :
            handdle_error("account_reset()")
        elif  exe_script == 'ca_check.air' :
            handdle_error("ca_reset()")
        # 還原管理員角色並刪除測試人員角色
        elif  exe_script == 'permission_check.air' :
            handdle_error("permission_reset()")
        elif  exe_script == 'taglist_check.air' :
            handdle_error("taglist_reset()")
    else:
        pass
    dfx("//*[@id=\"rule_layout\"]/div/div/main/div/div/button[2]/div").click()
    dfx("//button[@title='登出']").click()
    driver.assert_exist("//body", "xpath", '''測試完畢~<br>此測試完成率: %s %%'''% work_progress)
    driver.delete_all_cookies()
    driver.quit()

handdle_error("main_teardown()")
driver.quit()