# coding=utf-8
from common.db.db_base import DBBase
from crawler.base.db_base.stock_db_base import logger
from crawler.task.BaseTask import BaseTask
from arrow import Arrow
import arrow

'''
{
    "symbol": "000001",
    "ts_code": "000001.SZ",
    "last_crawl_day": "2018-01-15",
    "crawl_type": "BasicTradeInfo",
    "cur_dt": "2019-09-08"
}
'''
API_NAME = 'hk_hold'

'''
沪深港股通持股明细: https://tushare.pro/document/2?doc_id=188
'''


class DailyHkHoldTask(BaseTask):
    def __init__(self):
        super(DailyHkHoldTask, self).__init__()

    def close(self):
        super(DailyHkHoldTask, self).close()

    def run(self, task_define):
        Arrow.now().date()
        start_dt = arrow.get(task_define['last_crawl_day'])  # .strftime('%Y%m%d')
        end_dt = arrow.get(task_define['cur_dt']).replace(days=-1)
        for r_dt in Arrow.range('day', start_dt, end_dt):
            logger.info('Start to crawl data of task: %s, dt: %s' % (API_NAME, r_dt))
            t_dt = r_dt.strftime('%Y%m%d')
            daily_records = self.ts_client.query(API_NAME, trade_date=t_dt)
            self.write_db_with_df('stock_hk_hold_info', daily_records)

        # self.ts_client.query('daily')
