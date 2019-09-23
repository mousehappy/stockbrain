import json

from common.tushare_client.ts_client import ts_client

head_datas = ts_client.query('daily', trade_date='20180906')
# head_datas = datas[0:2]
t_dt = head_datas.loc[:, 'trade_date'].copy()
head_datas.loc[:, 'trade_dt'] = t_dt
symbols = head_datas['ts_code'].str.split('.').str[0]
head_datas['symbol'] = symbols
print len(head_datas)
drop_datas = head_datas.dropna()
print len(drop_datas)
# print json.dumps(drop_datas.to_dict('records'))

# cols = head_datas.columns
# for col in cols:
#     print col
# print json.dumps(head_datas.to_dict('records'))
# head_datas1 = head_datas.drop(['symbol', 'trade_dt'], axis=1)
# print json.dumps(head_datas1.to_dict('records'))
# print json.dumps(head_datas.to_dict('records'))
