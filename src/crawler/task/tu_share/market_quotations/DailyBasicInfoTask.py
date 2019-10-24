# coding=utf-8
from common.db.db_base import DBBase
from crawler.base.db_base.stock_db_base import logger
from crawler.task.BaseTask import BaseTask
import arrow

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
API_NAME = 'daily_basic'

'''
每日指标: https://tushare.pro/document/2?doc_id=32
'''


class DailyBasicInfoTask(BaseTask):
    def __init__(self):
        super(DailyBasicInfoTask, self).__init__()

    def close(self):
        super(DailyBasicInfoTask, self).close()

    def run(self, task_define):
        start_dt = arrow.get(task_define['last_crawl_day'])  # .strftime('%Y%m%d')
        end_dt = arrow.get(task_define['cur_dt'])
        for r_dt in arrow.Arrow.range('day', start_dt, end_dt):
            logger.info('Start to crawl data of task: %s, dt: %s' % (self.__class__.__name__, r_dt))
            t_dt = r_dt.strftime('%Y%m%d')
            daily_records = self.ts_client.query(API_NAME, trade_date=t_dt)
            self.write_db_with_df('stock_daily_basic', daily_records)

        # self.ts_client.query('daily')
