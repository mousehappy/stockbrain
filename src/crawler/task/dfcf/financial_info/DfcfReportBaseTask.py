# coding=utf-8
import json
import math
import time

import arrow
import requests

from common.db.db_base import DBBase
from common.util.StringUtils import genRandomString
from crawler.base.db_base.stock_db_base import logger
from crawler.task.BaseTask import BaseTask
from arrow import Arrow
import listcompare

'''
{
    "data_start_day": "2019-09-01",
    "status": 1,
    "crawl_end": "2019-09-01",
    "data_end_day": "2019-09-01",
    "gmt_create": "2019-09-07 13:54:35",
    "symbol": "000001",
    "ts_code": "000001.SZ",
    "gmt_modify": "2019-09-07 14:01:51",
    "last_crawl_day": "2018-01-15",
    "crawl_type": "BasicTradeInfo",
    "dt": "2019-09-07",
    "crawl_start": "2019-09-01 12:00:00",
    "crawl_status": "waiting",
    "cur_dt": "2019-09-08"
}
'''
API_NAME = 'dfcf_season_forecast'

'''
业绩预告: http://data.eastmoney.com/bbsj/201906/yjyg.html

url_example: http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token=70f12f2f4f091e459a279469fe49eca5&st=ndate&sr=-1&p=2&ps=30&js=var%20xsFnzmed={pages:(tp),data:%20(x),font:(font)}&filter=(IsLatest=%27T%27)(securitytypecode%20in%20(%27058001001%27,%27058001002%27))(enddate=^2019-09-30^)&rt=52288381
'''

base_url = 'http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=YJBB21_YJYG&token=70f12f2f4f091e459a279469fe49eca5&st=ndate&sr=-1&p={pageNo}&ps={pageSize}&js=var%20{varName}={pages:(tp),data:%20(x),font:(font)}&filter=(IsLatest=%27T%27)(securitytypecode%20in%20(%27058001001%27,%27058001002%27))(enddate=^{enddate}^)&rt={rt}'


class DfcfReportBaseTask(BaseTask):
    def __init__(self):
        super(DfcfReportBaseTask, self).__init__()
        self.stock_map = {}
        self.init_stock_map()
        self.token = '70f12f2f4f091e459a279469fe49eca5'
        self.db_table = ''
        self.order_column = ''
        self.date_columns = []
        self.base_url = ''
        self.pageSize = 30

    def close(self):
        super(DfcfReportBaseTask, self).close()
        
    def init_stock_map(self):
        sql = 'select ts_code, symbol as scode from stock_list'
        stock_list = self.query(sql)
        for stock in stock_list:
            self.stock_map[stock['scode']] = stock['ts_code']

    def get_latest_record(self, table, order_column):
        sql = 'select * from %s order by %s desc limit 1' % (table, order_column)
        latest_record = self.query(sql)
        return latest_record

    def run(self, task_define):
        # Arrow.now().date()
        # start_dt = Arrow.fromdate(task_define['last_crawl_day'])  # .strftime('%Y%m%d')
        # end_dt = Arrow.fromdate(task_define['cur_dt'])
        # for r_dt in Arrow.range('day', start_dt, end_dt):
        logger.info('Start to crawl data of task: %s, dt: %s' % (self.__class__.__name__, self.dt))
        self.dt = arrow.get(task_define['cur_dt'])
        report_dt = self.get_report_date()
        logger.info('Crawl task: %s, dt: %s, report date: %s' % (self.__class__.__name__, self.dt, report_dt))
        pageNo = 1
        total_pages = -1
        repoart_data = []
        latest_record = self.get_latest_record(self.db_table, self.order_column)
        while True:
            data = self.get_report_data(pageNo, report_dt)
            tmp_data = data['data']
            if total_pages < 0:
                total_pages = data['pages']
            logger.info('Crawl task [%s] with page [%s] success, total pages: [%s], current batch size: [%s]' % (
                self.__class__.__name__, pageNo, total_pages, len(tmp_data)))
            for record in tmp_data:
                record['ts_code'] = self.stock_map.get(record['scode'], '')
                for k,v in record.items():
                    if v == '-':
                        record[k] = None
                # if record['yearearlier'] == '-':
                #     record['yearearlier'] = None
            repoart_data.extend(tmp_data)
            # break
            if pageNo >= total_pages:
                break
            if not self.continue_crawl(tmp_data, latest_record, self.date_columns):
                break
            pageNo += 1
            # time.sleep(0.3)
        logger.info('Task [%s], total crawl records: %s' % (self.__class__.__name__, len(repoart_data)))
        # print json.dumps(repoart_data)
        self.write_db(self.db_table, repoart_data)

    def get_report_date(self):
        pass



    def get_report_data(self, pageNo, enddate):
        pageSize = self.pageSize
        rt = int(arrow.now().timestamp / 30)
        varName = genRandomString()
        cur_url = self.base_url.replace('{token}', self.token).replace('{pageNo}', str(pageNo)).replace('{pageSize}', str(pageSize)).replace(
            '{rt}', str(rt)).replace('{enddate}', enddate).replace('{varName}', varName)
        # print cur_url
        resp = requests.request('GET', cur_url)
        data = resp.content
        data = data.split(varName + '=')[1]
        data = data.replace('data:', '"data":').replace('pages:', '"pages":').replace('font:', '"font":')
        formatted_data = json.loads(data)
        font_map = formatted_data.get('font').get("FontMapping", [])
        for no_map in font_map:
            code = no_map.get('code').encode('utf-8')
            value = str(no_map.get('value'))
            data = data.replace(code, value)
        return json.loads(data)

    def continue_crawl(self, batch_record, latest_record, date_columns=[]):
        if not latest_record:
            return True
        latest_record = latest_record[0]
        latest_scode = str(latest_record.get('scode'))
        latest_data = [latest_record.get(col).strftime('%Y-%m-%dT%H:%M:%S') for col in date_columns]
        latest_data.append(latest_scode)
        # latest_enddate = latest_record.get('enddate').strftime('%Y-%m-%dT%H:%M:%S')
        # latest_ndate = latest_record.get('ndate').strftime('%Y-%m-%dT%H:%M:%S')
        for record in batch_record:
            scode = str(record.get('scode'))
            # enddate = str(record.get('enddate'))
            # ndate = str(record.get('ndate'))
            # if latest_scode == scode and latest_enddate == enddate and latest_ndate == ndate:
            #     return False
            current_data = [record.get(col) for col in date_columns]
            current_data.append(scode)
            if listcompare.compare_list(latest_data, current_data):
                return False
        return True
        # self.ts_client.query('daily')
