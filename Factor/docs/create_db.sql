-- 创建db文件

-- 全A股基本信息

-- 创建date日当天可获得最新财报日的dummy
-- 2010-01-01 -- 2010-04-31 取上年三季报 即 date_report = 2009-09-30
-- 2010-05-01 -- 2010-07-31 取上年年报   即 date_report = 2009-12-31
-- 2010-08-01 -- 2010-09-30 取本年一季报 即 date_report = 2010-03-31
-- 2010-10-01 -- 2010-10-31 取本年中报   即 date_report = 2010-06-30
-- 2010-11-01 -- 2010-12-31 取本年三季报 即 date_report = 2010-09-30
CREATE TABLE DUMMY
( 
  date                  DATE  NOT NULL ,
  sec_id            CHAR(20)  NOT NULL ,
  date_report_available  DATE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;


-- indicators
CREATE TABLE stocks_info
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  sec_name              CHAR(20)  NOT NULL ,
  industry_sw           CHAR(20) NOT NULL,
  traded_days_until_now           INT  NOT NULL,
  is_trade              INT  NOT NULL,
  is_st                 INT  NOT NULL,
  stock_total_shares    BIGINT  NOT NULL,
  stock_float_shares    BIGINT  NOT NULL,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- 前复权收盘价
CREATE TABLE close
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  close             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- 价值因子
CREATE TABLE pe_ttm
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  pe_ttm             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE ps_ttm
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  ps_ttm             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE pb
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  pb             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- 成长因子
CREATE TABLE growth_rate_of_opt_revenue
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  growth_rate_of_opt_revenue             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE growth_rate_of_net_income
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  growth_rate_of_net_income             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE growth_rate_of_total_asset
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  growth_rate_of_total_asset             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- CREATE TABLE growth_rate_of_roe
-- ( 
--   date                  DATE  NOT NULL ,
--   date_report_available                 DATE  NOT NULL ,
--   sec_id                CHAR(20)  NOT NULL ,
--   growth_rate_of_roe             DOUBLE  NOT NULL ,
--   PRIMARY KEY (date, sec_id)
-- ) ENGINE=MyISAM;

-- CREATE TABLE growth_rate_of_cash_flow
-- ( 
--   date                  DATE  NOT NULL ,
--   date_report_available                 DATE  NOT NULL ,
--   sec_id                CHAR(20)  NOT NULL ,
--   growth_rate_of_cash_flow             DOUBLE  NOT NULL ,
--   PRIMARY KEY (date, sec_id)
-- ) ENGINE=MyISAM;


-- 质量因子
CREATE TABLE debt_to_asset
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  debt_to_asset             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE current_ratio
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  current_ratio             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE quick_ratio
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  quick_ratio             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE cash_ratio
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  cash_ratio             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE interest_cover_ratio
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  interest_cover_ratio             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;


CREATE TABLE turnover_of_total_asset
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  turnover_of_total_asset             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;


CREATE TABLE turnover_of_total_inventory
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  turnover_of_total_inventory  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- 盈利因子
CREATE TABLE net_profit_margin
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  net_profit_margin  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE gross_profit_margin
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  gross_profit_margin  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE roe
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  roe  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE roa
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  roa  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- 波动率
CREATE TABLE vol_5days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_5days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE vol_30days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_30days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE vol_90days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_90days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE vol_180days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_180days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE vol_360days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_360days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- 动能

CREATE TABLE return_rate_5days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_5days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_30days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_30days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_90days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_90days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_180days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_180days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_360days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_360days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- 流动性因子
CREATE TABLE liq_5days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  liq_5days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE liq_30days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  liq_30days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE liq_90days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  liq_90days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE liq_180days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  liq_180days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE liq_360days
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  liq_180days             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;


-- 标准化后的表
CREATE TABLE vol_5days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_5days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE vol_30days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_30days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE vol_90days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_90days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE vol_180days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_180days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE vol_360days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  vol_360days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;


CREATE TABLE growth_rate_of_opt_revenue_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  growth_rate_of_opt_revenue_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE growth_rate_of_net_income_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  growth_rate_of_net_income_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE growth_rate_of_total_asset_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  growth_rate_of_total_asset_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- CREATE TABLE growth_rate_of_roe
-- ( 
--   date                  DATE  NOT NULL ,
--   date_report_available                 DATE  NOT NULL ,
--   sec_id                CHAR(20)  NOT NULL ,
--   growth_rate_of_roe             DOUBLE  NOT NULL ,
--   PRIMARY KEY (date, sec_id)
-- ) ENGINE=MyISAM;

-- CREATE TABLE growth_rate_of_cash_flow
-- ( 
--   date                  DATE  NOT NULL ,
--   date_report_available                 DATE  NOT NULL ,
--   sec_id                CHAR(20)  NOT NULL ,
--   growth_rate_of_cash_flow             DOUBLE  NOT NULL ,
--   PRIMARY KEY (date, sec_id)
-- ) ENGINE=MyISAM;


-- 质量因子
CREATE TABLE debt_to_asset_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  debt_to_asset_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE current_ratio_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  current_ratio_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE quick_ratio_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  quick_ratio_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE cash_ratio_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  cash_ratio_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE interest_cover_ratio_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  interest_cover_ratio_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;


CREATE TABLE turnover_of_total_asset_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  turnover_of_total_asset_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;


CREATE TABLE turnover_of_total_inventory_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  turnover_of_total_inventory_std  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

-- 盈利因子
CREATE TABLE net_profit_margin_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  net_profit_margin_std  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE gross_profit_margin_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  gross_profit_margin_std  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE roe_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  roe_std  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE roa_std
( 
  date                  DATE  NOT NULL ,
  date_report_available                 DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  roa_std  DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_5days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_5days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_30days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_30days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_90days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_90days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_180days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_180days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;

CREATE TABLE return_rate_360days_std
( 
  date                  DATE  NOT NULL ,
  sec_id                CHAR(20)  NOT NULL ,
  return_rate_360days_std             DOUBLE  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=MyISAM;
