# -*- encoding=utf8 -*-
__author__ = "Daniel"
__title__ = '報表列表檢查'
__desc__ = '確認報表列表是否正常呈現畫面'
# ========================module==============================
from library.basic import CaseService
# ========================設定變數=============================
dfx = driver.find_element_by_xpath
ser = CaseService()
report_dict = script_cfg.REPORT_SECTION['%s_dict' % exe_owner ]
check_date_dict = script_cfg.REPORT_SECTION['check_date_dict']
error_dict = {'error': [],'jserror':[]}
# =======================報表列表檢查=============================
# =======報表檢查使用，變更報表內日期，觀察每張報表近30天===========
def change_date(report_name):
    try:
        sleep(2)
        if report_name in check_date_dict['have_date_button']:
            WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='el-date-editor el-range-editor el-input__inner el-date-editor--daterange']"))
            dfx("//div[@class='el-date-editor el-range-editor el-input__inner el-date-editor--daterange']").click()
            dfx("//button[contains(.,'最近30天')]").click()
            dfx("//button[contains(.,'分析計算')]").click()
        elif report_name in check_date_dict['have_date']:
            WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='el-date-editor el-range-editor el-input__inner el-date-editor--daterange']"))
            dfx("//div[@class='el-date-editor el-range-editor el-input__inner el-date-editor--daterange']").click()
            dfx("//button[contains(.,'最近30天')]").click()
    except TimeoutException as e:
        driver.assert_exist("//body", "xpath", '%s' % e )
    except Exception as e:
        driver.assert_exist("//body", "xpath", '%s' % e )

# ==========報表檢查使用，判斷當前報表需檢查內容==================
def judge_report(index,report_name,img_list,url):
    #   判斷表格型報表
    if report_name in report_dict['table_data']:
        sleep(2)
        change_date(report_name)
        WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='vxe-table--body-wrapper body--wrapper']"))
        driver.assert_exist("//div[@class='vxe-table--body-wrapper body--wrapper']", "xpath", "正常有資料: 第%s張報表 %s 共%s張"%(index+1,report_name, len(img_list) ))
    #   判斷地圖型報表
    elif report_name in report_dict['map_data']:
        sleep(2)
        change_date(report_name)
        WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='leaflet-top leaflet-left']"))
        driver.assert_exist("//div[@class='leaflet-top leaflet-left']", "xpath", "正常有資料: 第%s張報表 %s 共%s張"%(index+1,report_name, len(img_list) ))
    #   判斷圖表型報表
    elif report_name in report_dict['get_canvas']:
        sleep(2)
        change_date(report_name)
        WebDriverWait(driver,30).until(lambda driver:dfx("//canvas"))
        driver.assert_exist("//canvas", "xpath", "正常有資料: 第%s張報表 %s 共%s張"%(index+1,report_name, len(img_list) ))
    #   判斷圖表型報表
    elif report_name in report_dict['no_canvas']:
        sleep(2)
        change_date(report_name)
        WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='el-table__body-wrapper is-scrolling-none']"))
        driver.assert_exist("//div[@class='el-table__body-wrapper is-scrolling-none']", "xpath", "正常有資料: 第%s張報表 %s 共%s張"%(index+1,report_name, len(img_list) ))
    #   確認報表是否有JSError
    elif report_name in report_dict['check_JsError']:
        sleep(4)
        w = ser.find_JSerror(driver,report_name)
        if w == 'warning':
            error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
        driver.assert_exist("//body", "xpath",  "確認JSError:第%s張報表 %s 共%s張"%(index+1,report_name, len(img_list) ))
    #   判斷此報表頁面是否正常呈現
    elif '受眾區間比較' in report_name:
        sleep(4)
        change_date(report_name)
        WebDriverWait(driver,30).until(lambda driver:dfx("//span[@class='el-radio-button__inner'][contains(.,'銷售額')]"))
        driver.assert_exist("//span[@class='el-radio-button__inner'][contains(.,'銷售額')]", "xpath", "正常有資料: 第%s張報表 %s 共%s張"%(index+1,report_name, len(img_list) ))
    #   判斷此報表頁面是否正常呈現
    elif '業績結構圖' in report_name:
        sleep(2)
        change_date(report_name)
        WebDriverWait(driver,30).until(lambda driver:dfx("//div[@class='databox__chart databox-second__chart']"))
        driver.assert_exist("//div[@class='databox__chart databox-second__chart']", "xpath", "正常有資料: 第%s張報表 %s 共%s張"%(index+1,report_name, len(img_list) ))
    #   報表暫無資料
    elif report_name in report_dict['non_data']:
        sleep(2)
        change_date(report_name)
        driver.assert_exist("//body", "xpath", "暫無資料: 第%s張報表 %s 共%s張"%(index+1,report_name, len(img_list) ))

def report_main(work_progress):
    try:
        dfx("//div[@class='md-button-content']//i[contains(.,'menu')]").click()
        dfx("//button[contains(.,'清空瀏覽器報表快取')]").click()
        dfx("//li[contains(.,'報表列表')]").click()
        img_list = driver.find_elements_by_css_selector('img.el-image__inner')
        js = '  return obj.list.map((d) => { return d["content"].map(u => u["url"])  })'
        url_list = driver.execute_script(js)
        url_list = py_.flatten_deep(url_list)
        analytics_url = ["/report/sales_conversion_analytics","/report/web_traffic_analytics","/report/member_web_traffic_analytics","/report/product_traffic_analytics"]
        have_analytics = ['dub','bt']
        new_url_list = []
        if exe_owner not in have_analytics:
            url_list = [item for item in url_list if item not in set(analytics_url)]
        for i in url_list:
            first_url =  'https://cdppj-sit.eagleeye.com.tw/'
            edition_url = first_url+ i
            new_url_list.append(edition_url)
        for index, report_url in enumerate(new_url_list):
            try:
                driver.get(report_url)
                url = driver.current_url
                report_name = dfx("//div[@class='md-content md-app-content md-flex md-theme-default']//h2").text
                report_name = report_name.split('\n')[0]
                judge_report(index,report_name,img_list,url)
                sleep(2)
                driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
                sleep(2)
                work_progress = round( (index+1) / len(new_url_list) * 100  )

            except StaleElementReferenceException as e:
                w = ser.find_JSerror(driver,report_name)
                print('=============================================================')
                print(ser._error_msg(e))
                print('=============================================================')
                sleep(2)
                if w == 'warning':
                    error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
                driver.assert_exist("//body", "xpath", '報表異常:第%s張報表 %s'%(index+1,report_name) )
                driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")

            except AssertionError as e:
                w = ser.find_JSerror(driver,report_name)
                print('=============================================================')
                print(ser._error_msg(e))
                print('=============================================================')
                if w == 'warning':
                    error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
                driver.assert_exist("//body", "xpath", '報表異常:第%s張報表 %s'%(index+1,report_name) )
                error_dict['error'].append( "<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name)  )
                driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
                
            except TimeoutException as e:
                w = ser.find_JSerror(driver,report_name)
                print('=============================================================')
                print(ser._error_msg(e))
                print('=============================================================')
                if w == 'warning':
                    error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
                driver.assert_exist("//body", "xpath", '報表異常:第%s張報表 %s'%(index+1,report_name) )
                error_dict['error'].append( "<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name)  )
                driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
                
            except Exception as e:
                w = ser.find_JSerror(driver,report_name)
                print('=============================================================')
                print(ser._error_msg(e))
                print('=============================================================')
                if w == 'warning':
                    error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
                driver.assert_exist("//body", "xpath", '報表異常:第%s張報表 %s'%(index+1,report_name) )
                error_dict['error'].append( "<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name)  )
                driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
        print(error_dict)
        try:
            if (len(error_dict['error']) >= 1) or (len(error_dict['jserror']) >= 1) :
                work_progress -= int(len(error_dict['error']) / len(new_url_list) * 100)
                assert_equal(False,True,'''錯誤報表彙總:<br>
                  報表異常: %s
                  jserror: %s
                  '''  %("，".join(error_dict['error']),"，".join(error_dict['jserror'])   ))
        except:
            pass


    except AssertionError as e:
        print('=============================================================')
        print(ser._error_msg(e))
        print('=============================================================')
    except NoSuchElementException as e:
        print('=============================================================')
        print(ser._error_msg(e))
        print('=============================================================')
    except Exception as e:
        print('=============================================================')
        print(ser._error_msg(e))
        print('=============================================================')
        
    return work_progress

if exe_owner == 'wt' and exe_time == '07':
    pass
elif exe_owner == 'dpr':
    pass
else:
    work_progress = report_main(work_progress)











        # url_list = ["/report/sales_conversion_analytics","/report/web_traffic_analytics","/report/product_traffic_analytics"]
        # new_url_list = []
        # for i in url_list:
        #     first_url =  'https://cdppj-sit.eagleeye.com.tw/'
        #     edition_url = first_url+ i
        #     new_url_list.append(edition_url)
        # for index, report_url in enumerate(new_url_list):
        #     for i in range(10):
        #         try:
        #             driver.get(report_url)
        #             url = driver.current_url
        #             report_name = dfx("//div[@class='md-content md-app-content md-flex md-theme-default']//h2").text
        #             report_name = report_name.split('\n')[0]
        #             judge_report(index,report_name,img_list,url)
        #             sleep(2)
        #             driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
        #             sleep(2)
        #             work_progress = round( (index+1) / len(new_url_list) * 100  )
            
        #         except StaleElementReferenceException as e:
        #             w = ser.find_JSerror(driver,report_name)
        #             print('=============================================================')
        #             print(ser._error_msg(e))
        #             print('=============================================================')
        #             sleep(2)
        #             if w == 'warning':
        #                 error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
        #             driver.assert_exist("//body", "xpath", '報表異常:第%s張報表 %s'%(index+1,report_name) )
        #             driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")

        #         except AssertionError as e:
        #             w = ser.find_JSerror(driver,report_name)
        #             print('=============================================================')
        #             print(ser._error_msg(e))
        #             print('=============================================================')
        #             if w == 'warning':
        #                 error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
        #             driver.assert_exist("//body", "xpath", '報表異常:第%s張報表 %s'%(index+1,report_name) )
        #             error_dict['error'].append( "<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name)  )
        #             driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
                    
        #         except TimeoutException as e:
        #             w = ser.find_JSerror(driver,report_name)
        #             print('=============================================================')
        #             print(ser._error_msg(e))
        #             print('=============================================================')
        #             if w == 'warning':
        #                 error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
        #             driver.assert_exist("//body", "xpath", '報表異常:第%s張報表 %s'%(index+1,report_name) )
        #             error_dict['error'].append( "<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name)  )
        #             driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
                    
        #         except Exception as e:
        #             w = ser.find_JSerror(driver,report_name)
        #             print('=============================================================')
        #             print(ser._error_msg(e))
        #             print('=============================================================')
        #             if w == 'warning':
        #                 error_dict['jserror'].append("<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name))
        #             driver.assert_exist("//body", "xpath", '報表異常:第%s張報表 %s'%(index+1,report_name) )
        #             error_dict['error'].append( "<a style='color: yellow' href= %s target='view_window'> 第%s張報表 %s  </a><br> "   %(url,index+1,report_name)  )
        #             driver.get("https://cdppj-sit.eagleeye.com.tw/report/rpt_list")
