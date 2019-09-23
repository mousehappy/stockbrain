CREATE TABLE stock_market_margin_detail(
`trade_date` int(20) not null default 0 comment '交易日期',
`ts_code` varchar(20) not null default '' comment 'TS股票代码',
`rzye` float(24) comment '融资余额(元)',
`rqye` float(24) comment '融券余额(元)',
`rzmre` float(24) comment '融资买入额(元)',
`rqyl` float(24) comment '融券余量（手）',
`rzche` float(24) comment '融资偿还额(元)',
`rqchl` float(24) comment '融券偿还量(手)',
`rqmcl` float(24) comment '融券卖出量(股,份,手)',
`rzrqye` float(24) comment '融资融券余额(元)',
key (trade_date, ts_code)) COMMENT '融资融券交易明细'
PARTITION BY RANGE(trade_date)
(
PARTITION p2016 VALUES LESS THAN (20170101),
PARTITION p2017 VALUES LESS THAN (20180101),
PARTITION p2018 VALUES LESS THAN (20190101),
PARTITION p2019 VALUES LESS THAN (20200101),
PARTITION p2020 VALUES LESS THAN (20210101),
PARTITION p2021 VALUES LESS THAN (20220101),
PARTITION p2022 VALUES LESS THAN (20230101)
);
