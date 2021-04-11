# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '行銷自動化檢查'
__desc__ = '''
一、新增ma
二、刪除編輯器原有流程
三、新增流程(確認編輯器是否可正常拖曳)
四、確認流程修改內容後是否儲存成功
五、進入編輯頁確認頁面可否進入
六、複製ma
七、查詢ma
八、刪除ma
'''
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
class Ma_Tool():
    def check_schedule(self):
        dfx("//button[@class='el-button el-button--default'][contains(.,'下一步')]").click()
        dfx("//button[@class='el-button el-button--massive el-button--primary']").click()
        driver.find_element_by_id("back").click()
        dfx("//button[@class='el-button el-button--default'][contains(.,'上一步')]").click()
        dfx("//button[@class='el-button el-button--default'][contains(.,'上一步')]").click()
        dfx("//div[@class='el-radio-button__text'][contains(.,'售後再行銷')]").click()
        dfx("//button[@class='el-button el-button--default'][contains(.,'下一步')]").click()
        dfx("//button[@class='el-button el-button--default'][contains(.,'下一步')]").click()
        dfx("//button[@class='el-button el-button--massive el-button--primary']").click()
        dfx("//button[contains(.,'確定')]").click()
        
    def change_schedule(self):
        dfx("//div[@class='blockelem noselect block vaild-fail-block']").click()
        element = "(//input[@class='el-input__inner'])[1]"
        dfx(element).send_keys("daniel")
        dfx("//button[contains(.,'儲存設定')]").click()
        msg = driver.execute_script("return document.getElementsByClassName('blockyinfo')[0].textContent")
        assert_equal(msg,"當會員購買 daniel 時觸發下一流程",'購買某商品會員儲存成功')

        dfx("(//div[@class='blockelem noselect block vaild-pass-block'])[1]").click()
        dfx(element).send_keys(Keys.CONTROL+'a')
        dfx(element).send_keys(Keys.BACK_SPACE)
        dfx(element).send_keys(2)
        dfx(element).send_keys(Keys.ENTER)
        dfx("//button[contains(.,'儲存設定')]").click()
        msg = driver.execute_script("return document.getElementsByClassName('blockyinfo')[1].textContent")
        assert_equal(msg,"等待 2 天",'等待天數儲存成功')

        dfx("//div[@class='blockelem noselect block vaild-fail-block']").click()
        dfx(element).click()
        dfx("(//div[@class='el-picker-panel__content el-scrollbar__wrap']//div[contains(.,'08:30')])[2]").click()
        dfx("//div[@class='el-textarea']//textarea").send_keys("QA_test")
        dfx("//button[contains(.,'儲存設定')]").click()
        msg = driver.execute_script("return document.getElementsByClassName('blockyinfo')[3].textContent")
        assert_equal(msg,"於 08:30 , 發送短連結簡訊",'發送簡訊時間儲存成功')

# =======================檢查MA編輯器=============================
def main_ma(work_progress):
    try:
        MT = Ma_Tool()
        # 進入MA頁
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//button[contains(.,'行銷自動化')]").click()
        dfx("//button[contains(.,'新增')]").click()
        work_progress += 20
        # 新增MA
        dfx("//input[@type='text']").send_keys("QA_test")
        today = datetime.date.today()
        one_range = today + datetime.timedelta(days=1)
        two_range = today + datetime.timedelta(days=3)
        element1 = "(//input[@class='el-range-input'])[1]"
        dfx(element1).click()
        dfx(element1).send_keys(str(one_range))
        element2 = "(//input[@class='el-range-input'])[2]"
        dfx(element2).click()
        dfx(element2).send_keys(str(two_range))
        dfx("//span[@class='el-tooltip info-tooltip material-icons item']").click()
        dfx("//div[@class='el-input el-input--suffix']").click()
        dfx("//li[contains(.,'每日')]").click()
        dfx("//div[@class='el-radio-button__text'][contains(.,'售後再行銷')]").click()
        dfx("//button[@class='el-button el-button--default'][contains(.,'下一步')]").click()
        dfx("//button[@class='el-button el-button--default'][contains(.,'下一步')]").click()
        dfx("//button[@class='el-button el-button--massive el-button--primary']").click()

        # 取消目前編輯器流程內容
        actionChains = ActionChains(driver)
        source_element = dfx("(//div[@class='blockelem noselect block vaild-pass-block'])[1]")
        dest_element = driver.find_element_by_id("blocklist")
        ActionChains(driver).drag_and_drop(source_element, dest_element).perform()
        driver.assert_exist("//div[@class='blockelem noselect block vaild-fail-block']", "xpath", "刪除原有流程")
        work_progress += 20

        # 編輯新流程
        dfx("//div[@id='loggers'][contains(.,'等待')]").click()
        start = driver.find_element_by_name("等待幾天")
        end = dfx("//div[@class='blockelem noselect block vaild-fail-block']")
        ActionChains(driver).drag_and_drop(start, end).perform()

        dfx("//div[@id='triggers'][contains(.,'受眾')]").click()
        start = driver.find_element_by_name("有點擊連結的會員")
        element_wait = driver.find_element_by_id("newcomp1")
        ActionChains(driver).click_and_hold(start).move_to_element_with_offset(element_wait,150,150).release().perform()

        dfx("//div[@id='actions'][contains(.,'動作')]").click()
        start = driver.find_element_by_name("傳送簡訊")
        element_send = driver.find_element_by_id("newcomp2")
        ActionChains(driver).click_and_hold(start).move_to_element_with_offset(element_send,150,150).release().perform()
        work_progress += 10

        # 更改流程內容，檢查修改後是否儲存成功
        MT.change_schedule()
        work_progress += 10

        # 儲存
        driver.assert_exist("(//div[@class='blockelem noselect block vaild-pass-block'])[2]", "xpath", "新流程編輯成功")
        driver.find_element_by_id("back").click()
        dfx("//button[@class='el-button el-button--primary'][contains(.,'儲存')]").click()
        wait_ma = WebDriverWait(driver,30).until( EC.text_to_be_present_in_element((By.XPATH,"//tr[@class='el-table__row']//div[@class='cell'][contains(text(),'QA_test')]" ), u'QA_test'))
        driver.assert_exist("//tr[@class='el-table__row']//div[@class='cell'][contains(text(),'QA_test')]", "xpath", "新增成功")
        # 進入編輯頁確認頁面可否進入
        more_button = dfx("(//tr[@class='el-table__row']//div[contains(text(),'QA_test')]/../../td//span[contains(.,'更多')])[2]")
        ActionChains(driver).move_to_element(more_button ).click(more_button ).perform()
        index = driver.execute_script("return document.getElementsByClassName('el-dropdown-menu el-popper').length")
        dfx("(//ul//li[contains(.,'複製')])[%s]/../li[contains(.,'編輯')]" % index).click()
        w = ser.find_JSerror(driver)
        driver.assert_exist("//body", "xpath",  "編輯頁檢視")
        dfx("//button[contains(.,'取消')]").click()
        dfx("//button[contains(.,'確定')]").click()
        # 複製MA
        wait_ma
        more_button = dfx("(//tr[@class='el-table__row']//div[contains(text(),'QA_test')]/../../td//span[contains(.,'更多')])[2]")
        ActionChains(driver).move_to_element(more_button ).click(more_button ).perform()
        index = driver.execute_script("return document.getElementsByClassName('el-dropdown-menu el-popper').length")
        dfx("(//ul//li[contains(.,'複製')])[%s]" % index).click()
        dfx("//div[@class='el-message-box']//span[contains(text(),'確定')]").click()
        wait_ma
        driver.assert_exist("//tr[@class='el-table__row']//div[@class='cell'][contains(text(),'QA_test 複製於編號')]", "xpath", "複製功能正常")

        dfx("//div[@class='el-input el-input--small el-input--prefix']//input").send_keys('QA_test')
        dfx("//*[@id='rule_layout']/div/div/main/div[2]/div/div[1]/div[3]/div/div[1]/div/form/div/div[2]/div/button[2]").click()
        wait_ma
        driver.assert_exist("//tr[@class='el-table__row']//div[@class='cell'][contains(text(),'QA_test')]", "xpath", "查詢功能正常")
        work_progress += 20

        # 刪除複製及原有MA
        driver.execute_script("return document.getElementsByClassName('el-checkbox__inner')[1].click()")
        driver.execute_script("return document.getElementsByClassName('el-checkbox__inner')[2].click()")
        dfx("//button[contains(.,'刪除')]").click()
        dfx("//div[@class='el-message-box']//span[contains(text(),'確定')]").click()
        driver.assert_exist("//div[@class='el-message el-message--success']", "xpath", "刪除成功")
        work_progress += 20

    except AssertionError as e:
        ser.find_JSerror(driver)
        print('=============================================================')
        print(ser._error_msg(e))
        print('=============================================================')
    except NoSuchElementException as e:
        driver.assert_exist("//body", "xpath", "找不到元素")        
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
    except Exception  as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        driver.assert_exist("//body", "xpath", "確認頁面是否正常呈現")
    return work_progress

work_progress = main_ma(work_progress)