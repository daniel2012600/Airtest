# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '帳號列表密碼重送信檢查'
__desc__ = '''
一、確認是否可正常收取密碼重設信
二、確認信件連結是否正常
三、進入信件連結並修改密碼，檢視是否有異常
'''
# ========================module==============================
from library.basic import CaseService
import email 
import imaplib
from lxml import etree  
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
# =======================檢查密碼重送信=============================
class PwMail_Tool():
    # ========================檢視gmail是否收取成功郵件============================
    def check_mail(self,exe_owner):
        EMAIL_ACCOUNT ='daniel_0601@reddoor.com.tw'
        PASSWORD = 'kill810098'
        try:
            # 登入gmail 並進入收件夾
            mail = imaplib.IMAP4_SSL('imap.gmail.com')
            mail.login(EMAIL_ACCOUNT, PASSWORD)
            labels = mail.list()
            inbox = mail.select("inbox") # connect to inbox.
            # 透過收件人為 (帳號 + owner)  尋找最新一封密碼重設信
            account =  "daniel_0601@reddoor.com.tw"  if exe_owner == 'cdpdemo' else "daniel_0601+%s@reddoor.com.tw" % exe_owner
            result, data = mail.uid('search',None, '(TO "%s")' % account)
            ids = data[0] # data is a list.
            id_list = ids.split() # ids is a space separated string
            latest_email_id = None
            if len(id_list) == 1:
                latest_email_id = id_list[0] # get the latest
                pass
            else:
                latest_email_id = id_list[-1]
                pass
            # 解析信件內容
            result, data = mail.uid('fetch', latest_email_id, '(RFC822)') # fetch the email body (RFC822) for the given ID
            raw_email = data[0][1]
            raw_email_string = raw_email.decode('utf-8') 
            email_message = email.message_from_string(raw_email_string)
            # 獲取收件時間
            now = datetime.datetime.now()
            date_tuple = email.utils.parsedate_tz(email_message['Date'])
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            subject = str(email.header.make_header(email.header.decode_header(email_message['Subject'])))
            # 確認該信件是否超過當前時間正負5分鐘，若超過則為收信失敗
            time_lag = str(now-local_date)
            time_lag = time_lag.split('day, ')[1] if re.findall( r'day, ' ,time_lag) else time_lag
            hour = int(time_lag.split(':')[0])
            minutes = int(time_lag.split(':')[1])
            content_html = email_message.get_payload(decode=True).decode()
            html = etree.HTML(content_html)
            reset_url = html.xpath("//p[contains(.,'連結')]/a//@href")[0]
            # 收信成功則回傳收信結果及重設信連結
            if hour <= 0 and minutes <= 5 :
                return True ,reset_url
            elif hour == 23 and minutes >=55:
                return True , reset_url
            else:
                return False ,''

            mail.close()
            mail.logout()

        except Exception as e :
            print(ser._error_msg(e))
            print('Ex')

def main_pwmail(work_progress):
    try:
        PMT = PwMail_Tool()
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//div[@class='md-list-expand']//div[contains(text(),'帳號列表')]").click()
        acc_page = driver.current_url
        work_progress += 30
        WebDriverWait(driver,10).until( EC.text_to_be_present_in_element((By.XPATH,"//tr[contains(.,'%s')]"% account ), u'%s' % account))
        dfx("(//tr[contains(.,'%s')]//button[contains(.,'密碼重設')])" % account ).click()
        dfx("//div[@class='el-message-box']//span[contains(text(),'確定')]").click()
        work_progress += 30
        sleep(2)
        msg = dfx("//div[@class='el-message el-message--success']").text
        assert_equal( msg,"重設密碼Email已寄出",'Email已送出')
        sleep(120)
        result, reset_url = PMT.check_mail(exe_owner)
        assert_equal(result,True,"信封收取成功")
        driver.get(reset_url)
        dfx("(//input[@type='password'])[1]").send_keys(pwd)
        dfx("(//input[@type='password'])[2]").send_keys(pwd)
        dfx("//button[contains(.,'密碼更新')]").click()
        ser.find_JSerror(driver)
        driver.assert_exist("//body", "xpath",  "檢視修改密碼頁面")
        driver.get(acc_page)
        work_progress += 40
        
    except AssertionError as e:
        ser.find_JSerror(driver)
        print('================================================================')
        print(ser._error_msg(e))
        print('================================================================')
        
    except NoSuchElementException as e:
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

work_progress = main_pwmail(work_progress)


        # driver.execute_script("window.open('https://accounts.google.com/signin/v2/identifier?hl=zh-TW','_blank');")
        # print('=============================================================')
        # print(111111111111111111111111111111111111111111111)
        # print("find button =>", driver.find_elements_by_css_selector("div.cell button.el-button"))
        # print('=============================================================')


        # driver.find_elements_by_css_selector("div.cell button.el-button")[155].click()










