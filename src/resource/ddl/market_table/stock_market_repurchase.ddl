CREATE TABLE stock_market_repurchase(
`ts_code` varchar(20) not null default '' comment 'Y	TS代码',
`ann_date` varchar(20) not null default '' comment 'Y	公告日期',
`end_date` varchar(20) not null default '' comment 'Y	截止日期',
`proc` varchar(20) not null default '' comment 'Y	进度',
`exp_date` varchar(20) not null default '' comment 'Y	过期日期',
`vol` float(24) comment 'Y	回购数量',
`amount` float(24) comment 'Y	回购金额',
`high_limit` float(24) comment 'Y	回购最高价',
`low_limit` float(24) comment 'Y	回购最低价',
key (ts_code, ann_date)) COMMENT '股票回购';
