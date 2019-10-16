from crawler.base.db_base.stock_db_base import StockDBBase
import requests


class A(StockDBBase):
    def __init__(self):
        super(A, self).__init__()

    def __del__(self):
        print "A is destructed!"


class B(A):
    def __del__(self):
        super(B, self).__del__()
        print "B is destructed!"


def test_func():
    a = A()
    a.close()


if __name__ == '__main__':
    # test_func()
    params = {
        'fields': 'ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,list_status,list_date,delist_date,is_hs',
        'api_name': 'stock_basic', 'params': {'list_status': 'L'},
        'token': '8e7d8f41808064385f0e041d92ca95684767755f1134188a7fdfdd47'}
    resp = requests.post(url='http://api.waditu.com', json=params)
    print resp.json()
