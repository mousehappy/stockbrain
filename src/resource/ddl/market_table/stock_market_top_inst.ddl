CREATE TABLE stock_market_top_inst(
`trade_date` int(20) not null default 0 comment 'Y	交易日期',
`ts_code` varchar(20) not null default '' comment 'Y	TS代码',
`exalter` varchar(20) not null default '' comment 'Y	营业部名称',
`buy` float(24) comment 'Y	买入额（万）',
`buy_rate` float(24) comment 'Y	买入占总成交比例',
`sell` float(24) comment 'Y	卖出额（万）',
`sell_rate` float(24) comment 'Y	卖出占总成交比例',
`net_buy` float(24) comment 'Y	净成交额（万）',
key (trade_date, ts_code, exalter)) COMMENT '龙虎榜机构明细';
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