import math

from common.db.db_base import DBBase
from common.tushare_client.ts_client import ts_token
import tushare as ts
import calendar
import arrow

from crawler.base.db_base.stock_db_base import StockDBBase

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
class BaseTask(StockDBBase):
    def __init__(self):
        super(BaseTask, self).__init__()
        ts.set_token(ts_token)
        self.ts_client = ts.pro_api()

    def close(self):
        super(BaseTask, self).close()

    def run(self, task_define):
        pass

    def get_day_span(self, start_dt, end_dt):
        span = end_dt - start_dt
        return span.days

    def is_last_day_of_month(self, dt):
        now_dt = arrow.now()
        year = dt.year
        month = dt.month
        day = dt.day
        hour = now_dt.hour
        last_day = calendar.monthrange(year, month)[1]
        if hour < 12 and day == 1:
            return True
        elif hour > 19 and day == last_day:
            return True
        return False

    def is_last_day_of_week(self, dt):
        now_dt = arrow.now()
        weekday = dt.weekday()
        hour = now_dt.hour
        if hour < 12 and weekday == 6:
            return True
        elif hour > 19 and weekday == 5:
            return True
        return False
        # calendar.monthrange(now_dt.)

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