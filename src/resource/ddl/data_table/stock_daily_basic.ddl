CREATE TABLE stock_daily_basic(
`ts_code` varchar(20) not null default '' comment 'TS股票代码',
`trade_date` int(20) not null default 0 comment '交易日期',
`close` float(24) comment '当日收盘价',
`turnover_rate` float(24) comment '换手率',
`turnover_rate_f` float(24) comment '换手率（自由流通股）',
`turnover_rate_s` float(24) comment '换手率（除大股东外流通股）',
`volume_ratio` float(24) comment '量比',
`pe` float(24) comment '市盈率（总市值/净利润）',
`pe_ttm` float(24) comment '市盈率（TTM）',
`pb` float(24) comment '市净率（总市值/净资产）',
`ps` float(24) comment '市销率',
`ps_ttm` float(24) comment '市销率（TTM）',
`total_share` float(24) comment '总股本 （万）',
`float_share` float(24) comment '流通股本 （万）',
`free_share` float(24) comment '自由流通股本 （万）',
`partner_share` float(24) comment '大股东流通股本 （万）',
`total_mv` float(24) comment '总市值 （万元）',
`circ_mv` float(24) comment '流通市值（万元）',
primary key (ts_code, trade_date))
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
