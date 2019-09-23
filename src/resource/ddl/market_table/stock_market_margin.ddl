CREATE TABLE stock_market_margin(
`trade_date` varchar(20) not null default '' comment '交易日期',
`exchange_id` varchar(20) not null default '' comment '交易所代码（SSE上交所SZSE深交所）',
`rzye` float(24) comment '融资余额(元)',
`rzmre` float(24) comment '融资买入额(元)',
`rzche` float(24) comment '融资偿还额(元)',
`rqye` float(24) comment '融券余额(元)',
`rqmcl` float(24) comment '融券卖出量(股,份,手)',
`rzrqye` float(24) comment '融资融券余额(元)',
key (trade_date, exchange_id)) COMMENT '融资融券交易汇总';
