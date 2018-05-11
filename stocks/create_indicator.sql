########################################
# 创建金融金融数据库indicator
# 
# Example table creation scripts
########################################

CREATE TABLE close
(
  date         DATE  NOT NULL ,
  sec_id       CHAR(50)  NOT NULL ,
  close        DOUBLE NOT NULL   ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE open
(
  date         DATE  NOT NULL ,
  sec_id       CHAR(50)  NOT NULL ,
  open         DOUBLE NOT NULL   ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE traded_days_until_now
(
  date                        DATE  NOT NULL ,
  sec_id                      CHAR(50)  NOT NULL ,
  traded_days_until_now       INT NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;


CREATE TABLE is_trade
(
  date         DATE  NOT NULL ,
  sec_id       CHAR(50)  NOT NULL ,
  is_trade         INT  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE is_st
(
  date         DATE  NOT NULL ,
  sec_id       CHAR(50)  NOT NULL ,
  is_st       INT  NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;


CREATE TABLE stock_total_shares
(
  date         DATE  NOT NULL ,
  sec_id       CHAR(50)  NOT NULL ,
  stock_total_shares  BIGINT NOT NULL  ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE stock_float_shares
(
  date                     DATE  NOT NULL ,
  sec_id                   CHAR(50)  NOT NULL ,
  stock_float_shares       BIGINT NOT NULL ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE asset
(
  date         DATE  NOT NULL ,
  sec_id       CHAR(50)  NOT NULL ,
  asset       DOUBLE NOT NULL  ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE debt
(
  date            DATE  NOT NULL ,
  sec_id          CHAR(50)  NOT NULL ,
  debt            DOUBLE NOT NULL  ,
  PRIMARY KEY     (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE equity
(
  date         DATE  NOT NULL ,
  sec_id       CHAR(50)  NOT NULL ,
  equity       DOUBLE NOT NULL  ,
  PRIMARY KEY (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE current_asset
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  current_asset       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE current_liab
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  current_liab       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE revenue_operating
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  revenue_operating       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE cost_operating
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  cost_operating       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE profit_operating
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  profit_operating       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE tax_operating
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  tax_operating       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE profit_main_operating
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  profit_main_operating       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE net_income
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  net_income       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE cash_received_by_sale
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  cash_received_by_sale       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE cash_received_by_operating
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  cash_received_by_operating       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE cash_paid_by_buy
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  cash_paid_by_buy       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE cash_paid_by_operating
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  cash_paid_by_operating       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE net_cash_received_by_operating
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  net_cash_received_by_operating       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE net_cash_received_by_investment
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  net_cash_received_by_investment    DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;

CREATE TABLE net_cash_received_by_funding
(
  date                DATE  NOT NULL ,
  sec_id              CHAR(50)  NOT NULL ,
  net_cash_received_by_funding       DOUBLE NOT NULL  ,
  PRIMARY KEY         (date, sec_id)
) ENGINE=InnoDB;
