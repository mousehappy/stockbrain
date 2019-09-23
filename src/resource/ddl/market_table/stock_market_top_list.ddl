CREATE TABLE stock_market_top_list(
`trade_date` int(20) not null default 0 comment 'Y	交易日期',
`ts_code` varchar(20) not null default '' comment 'Y	TS代码',
`name` varchar(20) not null default '' comment 'Y	名称',
`close` float(24) comment 'Y	收盘价',
`pct_change` float(24) comment 'Y	涨跌幅',
`turnover_rate` float(24) comment 'Y	换手率',
`amount` float(24) comment 'Y	总成交额',
`l_sell` float(24) comment 'Y	龙虎榜卖出额',
`l_buy` float(24) comment 'Y	龙虎榜买入额',
`l_amount` float(24) comment 'Y	龙虎榜成交额',
`net_amount` float(24) comment 'Y	龙虎榜净买入额',
`net_rate` float(24) comment 'Y	龙虎榜净买额占比',
`amount_rate` float(24) comment 'Y	龙虎榜成交额占比',
`float_values` float(24) comment 'Y	当日流通市值',
`reason` varchar(20) not null default '' comment 'Y	上榜理由',
key (trade_date, ts_code)) COMMENT '龙虎榜每日明细';
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