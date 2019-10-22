import json
import os
from datetime import datetime, date
# import tushare as ts
from common.util.sls_log_service import get_logger

import arrow

from common.db.db_base import DBBase
import logging
from logging.handlers import TimedRotatingFileHandler

from common.tushare_client.ts_client import ts_client

# file_path = os.path.abspath(__file__)
# src_path = file_path.split('/')
# log_path = '/'.join(src_path[:-4]) + '/resource/logs/stock_brain.log'
#
# logger = logging.getLogger(__name__)
# logger.setLevel(level=logging.INFO)
# formatter = logging.Formatter('[%(asctime)s] [%(processName)s] [%(process)d] [%(thread)d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s')
# # file_handler = TimedRotatingFileHandler('/Users/wjq/work/stockbrain/src/resource/logs/stock_brain.log', when='H', backupCount=30)
# file_handler = TimedRotatingFileHandler(log_path, when='H', backupCount=30)
# file_handler.setLevel(logging.INFO)
# file_handler.setFormatter(formatter)
# console_handler = logging.StreamHandler()
# console_handler.setLevel(logging.INFO)
# console_handler.setFormatter(formatter)
# logger.addHandler(console_handler)
# logger.addHandler(file_handler)

logger = get_logger(uuid=arrow.now().date().strftime('%Y-%m-%d'))


class StockDBBase(DBBase):
    def __init__(self):
        super(StockDBBase, self).__init__('stock_db')
        self.dt = arrow.now().date()
        self.crawl_dt = self.get_crawl_date()
        # ts.set_token(ts_token)
        self.ts_client = ts_client

    # def info(self, message):
    #     logger.info(message)
    #
    # def error(self, message):
    #     logger.error(message)
    #
    # def warn(self, message):
    #     logger.warn(message)
    #
    # def debug(self, message):
    #     logger.debug(message)
    #
    # def critical(self, message):
    #     logger.critical(message)

    def format_result(self, result):
        if isinstance(result, list):
            for r in result:
                self.format_result(r)
        if isinstance(result, dict):
            for k, v in result.items():
                if isinstance(v, datetime):
                    result[k] = v.strftime('%Y-%m-%d %H:%M:%S')
                elif isinstance(v, date):
                    result[k] = v.strftime('%Y-%m-%d')

    def get_crawl_date(self):
        now_dt = arrow.now()
        hour = now_dt.hour
        if hour < 8:
            ts_date = now_dt.shift(days=-1).format('YYYY-MM-DD')
        elif hour > 15:
            ts_date = now_dt.format('YYYY-MM-DD')
        return ts_date


if __name__ == '__main__':
    s = StockDBBase()
    # rows = s.query('select * from stock_task_scheduler limit 10')
    # s.format_result(rows)
    logger.info("Test!")
    # print json.dumps(rows)