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
板块大盘: http://quote.eastmoney.com/center/boardlist.html#concept_board

url_example: http://37.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87&_=1569638458193
'''

base_url = 'http://{randint}.push2.eastmoney.com/api/qt/clist/get?pn=1&pz=1000&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:90+t:3&fields=f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f14,f15,f16,f17,f18,f20,f21,f62,f63,f64,f65,f66,f67,f68,f69,f70,f71,f72,f73,f74,f75,f76,f77,f78,f79,f80,f81,f82,f83,f84,f85,f86,f87&_={ts}'


class DfcfConceptInfoDailyTask(BaseTask):
    def __init__(self):
        super(DfcfConceptInfoDailyTask, self).__init__()
        self.stock_map = {}
        self.init_stock_map()
        self.token = '70f12f2f4f091e459a279469fe49eca5'
        self.db_table = ''
        self.order_column = ''
        self.date_columns = []
        self.base_url = ''
        self.pageSize = 30

    def close(self):
        super(DfcfConceptInfoDailyTask, self).close()

    def get_crawl_date(self):
        now_dt = arrow.now()
        hour = now_dt.hour
        if hour < 8:
            ts_date = now_dt.replace(days=-1).format('YYYYMMDD')
        elif hour > 15:
            ts_date = now_dt.format('YYYYMMDD')
        else:
            raise RuntimeError('Illegal crawl time: %s' % now_dt)
        self.ts_client.query('trade_cal', start_date=ts_date, end_date=ts_date)

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
            time.sleep(0.3)
        logger.info('Task [%s], total crawl records: %s' % (self.__class__.__name__, len(repoart_data)))
        # print json.dumps(repoart_data)
        self.write_db(self.db_table, repoart_data)

    def get_report_date(self):
        pass

    def get_season_end_date(self):
        month = self.dt.month
        year = self.dt.year
        season = int(math.ceil(month / 3))
        # next_season_dt = None
        if season <= 3:
            next_season_dt = arrow.get(year, season * 3 + 1, 1)
        else:
            next_season_dt = arrow.get(year + 1, 1, 1)
        season_end_dt = next_season_dt.replace(days=-1)
        return season_end_dt.date().strftime('%Y-%m-%d')

    def get_last_season_end_date(self):
        month = self.dt.month
        year = self.dt.year
        season_idx = math.ceil(month / 3.0)
        season = int(season_idx)
        # next_season_dt = None
        if season > 1:
            next_season_dt = arrow.get(year, (season-1) * 3 + 1, 1)
        else:
            next_season_dt = arrow.get(year, 1, 1)
        season_end_dt = next_season_dt.replace(days=-1)
        return season_end_dt.date().strftime('%Y-%m-%d')

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


if __name__ == '__main__':
    cit = DfcfConceptInfoDailyTask()
    cit.get_crawl_date()