import json
from datetime import datetime, date
# import tushare as ts

from arrow import Arrow

from common.db.db_base import DBBase
import logging
from logging.handlers import TimedRotatingFileHandler

from common.tushare_client.ts_client import ts_client

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('[%(asctime)s] [%(processName)s] [%(process)d] [%(thread)d] [%(filename)s:%(lineno)d] [%(levelname)s] %(message)s')
file_handler = TimedRotatingFileHandler('/Users/wjq/work/stockbrain/src/resource/logs/stock_brain.log', when='H', backupCount=30)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class StockDBBase(DBBase):
    def __init__(self):
        super(StockDBBase, self).__init__('stock_db')
        self.dt = Arrow.now().date()
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


if __name__ == '__main__':
    s = StockDBBase()
    rows = s.query('select * from stock_task_scheduler limit 10')
    s.format_result(rows)
    print json.dumps(rows)