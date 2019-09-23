CREATE TABLE stock_daily_trade_info(
ts_code varchar(20) not null default '' comment '股票代码',
trade_date int(20) not null default 19700101 comment '交易日期',
open float(24) default 0.0 comment '开盘价',
high float(24) default 0.0 comment '最高价',
low float(24) default 0.0 comment '最低价',
close float(24) default 0.0 comment '收盘价',
pre_close float(24) default 0.0 comment '昨收价',
`change` float(24) default 0.0 comment '涨跌额',
pct_chg float(24) default 0.0 comment '涨跌幅',
vol float(24) default 0.0 comment '成交量',
amount float(24) default 0.0 comment '成交额',
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
