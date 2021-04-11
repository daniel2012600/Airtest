# -*- encoding=utf8 -*-

__author__ = "Daniel"
__title__ = '帳號權限檢查'
__desc__ = '''測試項目:
一、區域門店是否關閉成功
二、報表列表權限是否關閉成功
三、其他權限是否關閉成功(確認菜單是否仍出現權限選項)
'''
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================權限功能檢查=============================
area_store = script_cfg.PERMISSION_SECTION['%s' % exe_owner ]
if exe_owner == 'wt' or exe_owner == 'cdppj':
    other_opt = script_cfg.PERMISSION_SECTION['%s_opt' % exe_owner ]
else:
    other_opt =  script_cfg.PERMISSION_SECTION['other_opt']
class Permission_Tool():

    def set_store_permission(self,area_store):
        if exe_owner == 'dub' or exe_owner == 'dpr':
            pass
        else:
            dfx("//li[contains(.,'區域及門店')]").click()
            for area_opt in area_store:
                ActionChains(driver).key_down(Keys.DOWN).perform()
                dfx("//span[contains(.,'%s')]/..//div[@class='md-switch-container']" % area_opt).click()
        
    def check_layout(self,area_store):
        result = True
        if exe_owner == 'wt':
            try:
                driver.get("https://cdppj-sit.eagleeye.com.tw/wt_store")
                driver.assert_exist("//p[contains(.,'沒有資料')]", "xpath", "區域及門店權限關閉成功")
            except:
                driver.assert_exist("//body", "xpath", "顯示斷言失敗畫面")
                result = False
        else:
            try:
                driver.get("https://cdppj-sit.eagleeye.com.tw")
                dfx("//div[@class='float-right el-cascader']").click()
                option_data = dfx("//div[@class='el-scrollbar el-cascader-menu']").text
                if area_store[0] not in option_data:
                    driver.assert_exist("//div[@class='el-scrollbar el-cascader-menu']", "xpath", "區域及門店權限關閉成功")
                else:
                    result = False
            except:
                driver.assert_exist("//body", "xpath", "顯示斷言失敗畫面")
        return result

    def check_menu(self):
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        menu_data = dfx("(//ul[@class='md-list md-theme-default'])[1]").text
        if '會員列表' in menu_data:
            return True
        else:
            return False
    # 角色變更
    def change_roles(self,roles):
        driver.get("https://cdppj-sit.eagleeye.com.tw/account")
        dfx("(//tr[contains(.,'%s')]//button[contains(.,'變更角色')])" % account ).click()
        dfx("(//input[@class='el-input__inner'])[5]").click()
        dfx("//li[contains(.,'%s')]" % roles).click()
        dfx("//button[contains(.,'確定')]").click()
        driver.refresh()

    # ==========帳號權限檢查使用，開啟關閉所有功能==================
    def click_other_option(self, exe_owner, other_opt):
        report_opt = ['銷售','營運','會員','商品','財務','監測']
        for report in report_opt:
            dfx("//li[@class='md-subheader md-theme-default'][contains(.,'報表列表')]/..//span/li[contains(.,'%s')]/div/div/div" % report).click()
        for other in other_opt:
            dfx("(//li//span[contains(.,'%s')]/../..//div[@class='md-switch-container'])[1]" % other).click()

def main_permisson(work_progress):
    try:
        PT = Permission_Tool()
        # 新增測試人員角色
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//li//button[contains(.,'角色列表')]").click()
        setting_page = driver.current_url
        dfx("//button[contains(.,'新增')]").click()
        dfx("(//input[@class='md-input'])[1]").send_keys('測試人員')
        dfx("(//input[@class='md-input'])[2]").send_keys('QA測試')
        # 關閉總覽區域及門店權限
        PT.set_store_permission(area_store)
        dfx("(//button[contains(.,'儲存')])").click()
        WebDriverWait(driver,30).until(lambda driver:dfx("//tr[contains(.,'測試人員')]" ))
        work_progress += 10
        # 角色變更並確認總覽區域及門店權限
        PT.change_roles('測試人員')
        layout_result = PT.check_layout(area_store)
        # 復原總覽區域及門店權限
        driver.get(setting_page)
        dfx("(//td[contains(.,'測試人員')]/..//span[contains(.,'編輯')])[2]").click()
        PT.set_store_permission(area_store)
        work_progress += 10
        # 關閉其他權限
        PT.click_other_option(exe_owner, other_opt)
        dfx("(//button[contains(.,'儲存')])").click()
        driver.refresh()
        result = PT.check_menu()
        try:
            if result:
                assert_equal(False,True,"權限關閉失敗")
            else:
                driver.assert_exist("//body", "xpath", "權限關閉成功")
        except:
            driver.assert_exist("//body", "xpath", "顯示斷言失敗畫面")
        work_progress += 20
        # 確認報表列表權限關閉成功
        driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
        img_count = driver.execute_script("return document.getElementsByClassName('el-image__inner').length")
        try:
            if img_count != 0:
                assert_equal(False,True,"報表列表權限關閉失敗")
            else:
                driver.assert_exist("//h2[contains(.,'報表列表')]", "xpath", "報表列表權限關閉成功")
        except:
            driver.assert_exist("//body", "xpath", "顯示斷言失敗畫面")
        work_progress += 20
        # 復原所有權限
        driver.get(setting_page)
        dfx("(//td[contains(.,'測試人員')]/..//span[contains(.,'編輯')])[2]").click()
        PT.click_other_option(exe_owner, other_opt)
        dfx("(//button[contains(.,'儲存')])").click()
        driver.get('https://cdppj-sit.eagleeye.com.tw/')
        result = PT.check_menu()
        try:
            if result:
                driver.assert_exist("//body", "xpath", "權限復原成功")
            else:
                assert_equal(False,True,"權限復原失敗")
        except:
            driver.assert_exist("//body", "xpath", "顯示斷言失敗畫面")
        work_progress += 20
        # 復原角色並刪除測試人員角色
        PT.change_roles('管理員')
        driver.get(setting_page)
        dfx("//div[@class='cell'][contains(.,'測試人員')]/../..//button[contains(.,'刪除')]").click()
        dfx("//button[contains(.,'確定')]").click()
        sleep(2)
        msg = dfx("//div[@class='el-message el-message--warning']").text
        assert_equal( msg,"已刪除角色「測試人員」",' 角色刪除成功' )
        work_progress += 20

    except AssertionError as e:
        ser.find_JSerror(driver)
        print('=============================================================')
        print(ser._error_msg(e))
        print('=============================================================')
    except NoSuchElementException as e:
        ser.find_JSerror(driver)
        print('=============================================================')
        print(ser._error_msg(e))
        print('=============================================================')
    except Exception as e:
        ser.find_JSerror(driver)
        print('=============================================================')
        print(ser._error_msg(e))
        print('=============================================================')
    return work_progress

if exe_owner == 'wt' and exe_time == '07':
    work_progress = 100
    pass
else:
    work_progress = main_permisson(work_progress)
