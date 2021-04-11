# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '會員列表檢查'
__desc__ = '''檢查會員列表:
一、正常進入會員資訊頁面
二、確認搜尋功能是否正常
'''
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================檢查會員列表=============================
def main_member(work_progress):
    try:
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//li[@class='md-list-item']//div[contains(.,'會員列表')]").click()
        WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='vxe-table--fixed-left-wrapper']"))
        work_progress += 20
        # element = dfx("(//td[contains(.,'查看')])[1]")
        # ActionChains(driver).move_to_element(element).click().perform()
        ser.check_loading(driver)
        driver.execute_script("document.getElementsByClassName('el-link--underline el-link el-link--primary is-underline')[0].click()")
        sleep(5)
        driver.switch_to_new_tab()
        ser.check_loading(driver)
        search_name = dfx("//div[@class='member-info__value member-info__name']").text
        driver.assert_exist("//div[@class='member-info__value member-info__name']","xpath","一、獲取會員資訊以供搜尋 : %s" % search_name)
        sleep(2)
        work_progress += 20
        driver.switch_to_previous_tab()
        dfx("//div[@class='el-select el-select--small']").click()
        dfx("//div[@class='el-scrollbar']//span[contains(text(),'姓名')]").click()
        dfx("//div[@class='el-input el-input--small el-input--prefix']//input").send_keys(search_name)
        dfx("//div[@class='el-form-item__content']//span[contains(text(),'查詢')]").click()
        driver.switch_to_new_tab()
        ser.check_loading(driver)
        driver.close()
        work_progress += 20
        driver.switch_to_previous_tab()
        WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='vxe-table--fixed-left-wrapper']"))        
        driver.assert_exist("//div[@class='vxe-table--fixed-left-wrapper']", "xpath", "二、搜尋功能正常")
        work_progress += 20
        # element = dfx("(//td[contains(.,'查看')])[1]")
        # ActionChains(driver).move_to_element(element).click().perform()
        driver.execute_script("document.getElementsByClassName('el-link--underline el-link el-link--primary is-underline')[0].click()")
        driver.switch_to_new_tab()
        ser.check_loading(driver)
        sleep(2)
        # WebDriverWait(driver,30).until_not(lambda driver: driver.execute_script('return  obj.loading.info = false') )
        driver.switch_to_previous_tab()
        work_progress += 20

    except TimeoutException :
        ser.find_JSerror(driver)
        driver.assert_template(Template(r"tpl1596791134459.png", threshold=0.39999999999999986, record_pos=(28.205, 4.095), resolution=(100, 100)), "資料載入中")
        sleep(10)
        driver.assert_template(Template(r"tpl1596791134459.png", threshold=0.39999999999999986, record_pos=(28.205, 4.095), resolution=(100, 100)), "資料載入失敗")
    except AssertionError as e:
        ser.find_JSerror(driver)
        driver.assert_template(Template(r"tpl1594883068901.png", threshold=0.49999999999999983, record_pos=(28.295, 4.055), resolution=(100, 100)), "請輸入正確資訊或無此會員資訊")
    except Exception as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    return work_progress

if exe_owner == 'wt' and exe_time == '07':
    work_progress = 100
    pass
else:
    work_progress = main_member(work_progress)