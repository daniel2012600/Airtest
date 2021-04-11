# -*- coding:utf8 -*-
#原有import
import csv
import datetime
import os
import shutil
import sys
import time
from argparse import *
from pathlib import Path
from typing import List
import airtest.report.report as report
import jinja2
from airtest.cli.parser import runner_parser
from airtest.cli.runner import run_script
from airtest.core.settings import Settings as ST
from airtest.cli.runner import AirtestCase
#自己import
import logging
from pydash import py_
import click
from config import *
import re
# 紀錄Terminal內error的log
logger = logging.getLogger("airtest")
logger.setLevel(logging.ERROR)

# ==============================全域變數======================================
CHROME_PATH = "./chromedriver.exe" # 設定瀏覽器路徑
PROJECT_ROOT = os.getenv("suite",r'.')  # 設定腳本存放的根目錄
AIRTEST_EXPORT_DIR = os.getenv('report',r'C:/test')  # 測試報告相關資源打包後的匯出路徑，目錄不存在會自動建立
AUTOLINE_HOST = 'http://192.168.188.145:5297'
Exe_Cfg = Execute_Config()
Script_Cfg = Script_Config()
Error_Log_Path = 'C:/airtest_develop/suite/logs/'    # 設定 logs 目錄

if Path(AIRTEST_EXPORT_DIR).is_dir():
    pass
else:
    os.makedirs(AIRTEST_EXPORT_DIR)
class McCustomAirtestCase(AirtestCase):
    """
    Aietest Project自定義啟動器，參考文件：http://airtest.netease.com/docs/cn/7_settings/3_script_record_features.html
    """
    def setUp(self):
        print("----------Custom Setup [Hook method]----------")
        # 將自定義的公共變數加入到`self.scope`中，在腳本程式碼中就可以直接使用
        self.scope["exe_time"] = exe_time #執行時間
        self.scope["exe_script"] = exe_script  # 當前執行腳本
        self.scope["exe_owner"] = exe_owner #此次測試業主
        self.scope['work_progress'] = 0 #當前進度紀錄
        self.scope['script_cfg'] = Script_Cfg #設置檔案
        self.scope['chrome'] = CHROME_PATH # 啟動瀏覽器
        self.scope['upload_path'] = ACCOUNT_UPLOAD_FILE # 批次上傳帳號檔案
        # 設定`Airtest`全域性屬性值
        ST.THRESHOLD = 0.80  # 影象識別精確度閾值 [0,1]
        ST.THRESHOLD_STRICT = 0.85  # assert語句裡影象識別時使用的高要求閾值 [0,1]
        ST.OPDELAY = 2  # 每一步操作後等待多長時間進行下一步操作, 只針對Airtest語句有效, 預設0.1s
        ST.FIND_TIMEOUT = 30  # 影象查詢超時時間，預設為20s
        ST.CVSTRATEGY = ["tpl", "sift", "brisk"]  # 修改影象識別演算法順序，只要成功匹配任意一個符合設定闕值的結果，程式就會認為識別成功

        # 可以將一些通用的操作進行封裝，然後在其他指令碼中 import;
        # Airtest 提供了 using 介面，能夠將需要引用的指令碼加入 sys.path 裡，其中包含的圖片檔案也會被加入 Template 的搜尋路徑中
        # using("common.air")    # 相對於PROJECT_ROOT的路徑
        self.exec_other_script("setup.air")
        super(McCustomAirtestCase, self).setUp()

    def tearDown(self):
        print("----------Custom Teardown [Hook method]----------")

        self.exec_other_script("teardown.air")
        super(McCustomAirtestCase, self).tearDown()

def check_item(test_item : str ) -> list :
    if ('all' or 'ALL')  in test_item :
        if exe_owner == 'wt':
            all_scripts = Exe_Cfg.WT_SCRIPT_LIST
        elif exe_owner == 'cdppj':
            all_scripts = Exe_Cfg.CDPPJ_SCRIPT_LIST
        else:
            all_scripts = Exe_Cfg.SCRIPT_LIST
    else:
        all_scripts = []
        if re.search( r'\S+_check.air' ,test_item):
            all_scripts.append(test_item)
        elif re.search( r'\S+' ,test_item):
            all_scripts.append('%s_check.air' % test_item)

    return all_scripts

def run_airtest(script, log_root, device="",compress=75,):
    """
    執行單個指令碼，並生成測試報告，返回執行結果
    :param script:  *.air, 要執行的指令碼
    :param device:  裝置字串
    :param log_root:  指令碼日誌存放目錄
    """
    if os.path.isdir(log_root):
        print('once again on same time')
        # shutil.rmtree(log_root)
    else:
        os.makedirs(log_root)
        print(str(log_root) + '>>> is created')

    # 組裝執行引數
    args = Namespace(device=device,  # 裝置字串
                    log=log_root,  # log目錄
                    recording=None,  # 禁止錄屏
                    script=script,  # *.air
                    compress=compress,
                     )
    run_script(args, McCustomAirtestCase)

def generate_report(script, *, log_root, export_root,report_time):
    """
    生成測試報告
    :param script:  執行名稱
    :param log_root:  指令碼log目錄
    :return: export_root  測試報告輸出目錄
    """
    if not os.path.isdir(export_root):
        os.makedirs(export_root)
        print(str(export_root) + '>>> is created')
    # 生成測試報告
    rpt = report.LogToHtml(script_root=script,  # *.air
                           log_root=log_root,  # log目錄
                           export_dir=export_root,  # 設定此引數後，生成的報告內資源引用均使用相對路徑
                           lang='zh',  # 設定語言, 預設"en"
                           script_name=exe_script.replace(".air", ".py"),  # *.air/*.py
                           static_root=AUTOLINE_HOST + '/static',  # 設定此引數後，打包後的資源目錄中不會包含樣式資源 http://192.168.188.145:5297/static/
                           plugins=["airtest_selenium.report"] # 使報告支援poco語句
                           )
    rpt.report("log_template.html")
    # 提取指令碼執行結果
    # result = rpt.test_result  # True or False
    result = {}
    result['owner'] = exe_owner
    result["name"] = exe_script.replace('.air', '')
    script_dict = Exe_Cfg.SCRIPT_DICT
    desc_dict = Exe_Cfg.DESCRIPTION_DICT
    result["ch_name"] = script_dict[exe_script.split('_')[0].replace('.air', '')]
    result['desc'] = desc_dict[exe_script.split('_')[0].replace('.air', '')]
    result["time"] = report_time
    result["result"] = rpt.test_result

    return result

def summary_html(results, output_dir, template_dir ):
    """
    生成自定義的聚合報告
    :param results:  執行結果
    :param output_dir:  html輸出目錄
    :param template_parent:  jinja2模板所在目錄
    """
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(template_dir),
        extensions=(),
        autoescape=True,
    )
    owner_ch_name = Exe_Cfg.OWNERNAME_DICT
    template = env.get_template("summary_template.html", template_dir)
    script_count = len(results)
    True_count  = len(py_.filter_(results, {'result': True}))
    False_count = len(py_.filter_(results, {'result': False}))
    html = template.render({"results": results, 'project': owner_ch_name[exe_owner]})
    report_html = "%s_%s_%s_test%s_pass%s_fail%s.html" % (exe_owner,exe_time,exe_min,script_count,True_count,False_count)

    output_file = Path(output_dir, report_html)  # 聚合報告路徑
    with open(output_file, 'w', encoding="utf-8") as f:
        f.write(html)
    print(output_file)

def print_message(*message):
    print("*" * 50)
    mes = " ".join(map(str, message))
    print(mes)
    print("*" * 50)

def del_pyfile(log_path,today):
    py_path = os.path.join( log_path+'/'+exe_script.replace('.air', '.log'))
    for i in os.listdir(py_path):
        py_file = exe_script.replace('.air', '.py')
        if i.endswith(py_file):
            os.remove(os.path.join(py_path,py_file))

def create_logger(owner,date):
    # config
    filename = f'error_{owner}.log'    # 設定檔名
    logging.captureWarnings(True)   # 捕捉 py waring message
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    my_logger = logging.getLogger('py.warnings')    # 捕捉 py waring message
    my_logger.setLevel(logging.ERROR)
    
    # 若不存在目錄則新建
    if not os.path.exists(Error_Log_Path+date):
        os.makedirs(Error_Log_Path+date)
    
    # file handler
    fileHandler = logging.FileHandler(Error_Log_Path+date+'/'+filename, 'a+', 'utf-8')
    fileHandler.setFormatter(formatter)
    my_logger.addHandler(fileHandler)
    
    # console handler
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)
    consoleHandler.setFormatter(formatter)
    my_logger.addHandler(consoleHandler)
        
    return my_logger

@click.command()
@click.argument('test_item',default='all')
@click.argument('owner',default='cdppj')
def main(test_item,owner):
    global exe_owner,exe_time,exe_min
    exe_owner = owner
    exe_time = datetime.datetime.now().strftime('%H')
    exe_min = datetime.datetime.now().strftime('%M')
    # report_time = 'report_%s_%s' % (exe_time,exe_min)
    report_time = 'report_10_39'
    all_scripts = check_item(test_item) # 如果收到執行腳本名稱，則其他腳本則不執行
    print(all_scripts)
    results = []  # 指令碼執行結果彙總
    today = str(datetime.date.today())
    html_root = Path(AIRTEST_EXPORT_DIR,'report',today)  # html匯出目錄

    for script in all_scripts:
        global exe_script
        exe_script = script
        try:
            print_message("正在執行的案例名稱：" + script)
            if script == 'bi_list_check.air':
                print(my_fail)
            script = os.path.join('./case', script)
            log = os.path.join(AIRTEST_EXPORT_DIR, 'report' + '/' + today+'/'+ report_time + '/' + exe_owner + '/' + exe_script.replace('.air', ''))
            run_airtest(script, log)  # 執行指令碼
            result = generate_report(script,log_root=log, export_root=log,report_time=report_time)  # 生成測試報告
            results.append(result)
            results =  py_.sort_by(results,'owner')
            del_pyfile(log,today)
        except Exception as e:
            logger = create_logger(owner,today)
            logger.exception(e)
            logger.critical(f'留存已執行測試之結果 : {results}')

    print_message("執行結果彙總:", results)
    summary_html(results, output_dir=html_root, template_dir=PROJECT_ROOT)

if __name__ == '__main__':
    main()
    quit()
    




# def find_all_scripts(suite_dir: str = "") -> list:
#     """
#     遍歷suite目錄，取出所有的測試指令碼
#     """
#     suite = []
#     if not suite_dir:
#         suite_dir = PROJECT_ROOT
#     for fpath in Path(suite_dir).iterdir():
#         tmp = Path(Path.cwd(), fpath)
#         # print('forlder: %s  is dir? : %s ' % (tmp , tmp.is_dir()) )
#         if not tmp.is_dir():
#             pass
#         else:
#             if fpath.suffix == '.air' and fpath.stem not in ["setup", "teardown"]:  # 這裡會排除掉初始化指令碼
#                 suite.append(fpath.name)
#             else:
#                 deep_scripts = find_all_scripts(tmp)  # 遞迴遍歷
#                 suite += deep_scripts
#     return suite