# from crawler.base.db_base.stock_db_base import StockDBBase
from common.db.db_base import DBBase
from common.tushare_client.ts_client import ts_client
import arrow


class StockCMDB(DBBase):
    def __init__(self):
        self.dt = arrow.now()
        self.ts_client = ts_client
        # super(StockCMDB, self).__init__()
        # super(StockCMDB, self).__init__("stock_db")

    def run(self):
        self.get_stock_list()

    def get_stock_list(self):
        #logger.info('Start to refresh stock list, current dt: %s' % self.dt)
        s_basic = self.ts_client.query('stock_basic', list_status='L')
        s_basic['dt'] = self.dt
        basic_dicts = s_basic.to_dict('records')
        # basic_dicts = {}
        # print json.dumps(basic_dicts[0:5])
        self.write_db('stock_list', basic_dicts)
        self.delete_outdated_rows('stock_list', self.dt)
        #logger.info('Success refresh stock list, stock count: %s' % len(basic_dicts))
        return basic_dicts


if __name__ == '__main__':
    basic = ts_client.query('stock_basic', list_status='L',
                                  fields='ts_code,symbol,name,area,industry,fullname,enname,market,'
                                         'exchange,curr_type,list_status,list_date,delist_date,is_hs')
