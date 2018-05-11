# 将含有@的财报比率数据转换成结构数据
all = {}
for ind in ['liab', 'growth', 'operating', 'investment', 'cash_flow', 'profit', 'capital_structure']:
    df = pd.read_csv(
        r"E:\02_work\data\finance_analysis\{}.CSV".format(ind), encoding='gbk')
    a = {}
    for i in df.columns.tolist()[2:]:
        key = str(i[:8])
        if key in a:
            a[key].append(i)
        else:
            a[key] = [i]
    dfs = {}

    for date in a:
        dfs[date] = df[['代码', '名称'] + a[date]]

    new = pd.DataFrame()
    for date in dfs:
        df = dfs[date]
        df = df.rename(columns={ins: ins.split(
            '@')[1] for ins in df.columns.tolist()[2:]})
        df['date'] = date[:4] + '-' + date[4:6] + '-' + date[6:]
        new = new.append(df)
    all[ind] = new

output = pd.DataFrame(all['liab'][['代码', '名称', 'date']])
for ind in all:
    output=output.merge(all[ind],how='outer',left_on=['代码','名称','date'],right_on=['代码','名称','date'])

ratios = output
ratios=ratios.replace({0:np.NaN})
ratios1=ratios.iloc[ratios.iloc[:,3:].dropna(how='all').index,:]
def date_transform(date):
    return datetime.datetime.strftime(datetime.datetime.strptime(date,'%Y/%m/%d'),'%Y-%m-%d')
ratios1['date']=ratios1['date'].apply(lambda x: date_transform(x))
del ratios1['名称']
ratios1=ratios1.reset_index()
ratios1 =ratios1.rename(columns={'date':'date_report'})
ratios1 = ratios1.sort_values(by=['date','sec_id'])
a=ratios1.isnull().sum() / ratios1.shape[0]
cols_to_retain=a[a<0.3].index.tolist()
ratios1 = ratios1[cols_to_retain]

# 整理财报数据
a = pd.read_csv(r"E:\02_work\data\fr\fr.CSV", encoding='gbk')
a['date_published'] = a['date_published'].apply(lambda x: datetime.datetime.strftime(
    datetime.datetime.strptime(str(x), '%Y%m%d'), '%Y-%m-%d'))
names = {
    '流动资产合计': 'current_asset',
    '固定资产合计': 'fixed_asset',
    '无形资产': 'intangible_asset',
    '商誉': 'goodwill',
    '开发支出': 'devlopment_expense',
    '资产总计': 'asset',
    '流动负债合计': 'current_liab',
    '长期负债合计': 'long_term_liab',
    '股东权益合计': 'equity',
    '负债与股东权益总计': 'sum_of_equity_and_liab',
    '营业总收入': 'revenue_from_total_operating',
    '营业收入': 'revenue_from_operating',
    '主营业务收入净额': 'net_main_operating_revenue',
    '营业总成本': 'cost_from_total_operating',
    '营业成本': 'cost_from_operating',
    '营业税金及附加': 'business_tariff_and_annex',
    '主营业务利润': 'income_from_main_operating',
    '其他业务利润': 'income_from_other_operating',
    '营业费用': 'operating_expense',
    '管理费用': 'administrative_cost',
    '财务费用': 'financial_cost',
    '资产减值损失': 'loss_from_asset_devaluation',
    '其他业务成本': 'cost_from_other_business',
    '投资收益 ': 'income_from_investment',
    '营业利润': 'income_from_operating',
    '利润总额': 'income_before_tax',
    '净利润': 'net_income',
    '归属于母公司所有者净利润': 'net_income_to_owners',
    '基本每股收益': 'basic_eps',
    '稀释每股收益': 'diluted_eps',
    '应付普通股股利': 'divdends_payable',
    '转作股本的普通股股利': 'divdends_to_capital_stock',
    '未分配利润': 'undistributed_profits',
    '销售商品、提供劳务收到的现金': 'inflow_cash_from_sales',
    '经营活动现金流入小计': 'inflow_cash_from_operating',
    '购买商品、接受劳务支付的现金': 'outflow_cash_from_buy',
    '经营活动现金流出小计': 'outflow_cash_from_operating',
    '经营活动产生的现金流量净额': 'net_cash_inflow_from_operating',
    '投资活动现金流入小计': 'inflow_cash_from_investment',
    '投资活动现金流出小计': 'outflow_cash_from_investment',
    '投资活动产生的现金流量净额': 'net_cash_inflow_from_investment',
    '筹资活动现金流入小计': 'inflow_cash_from_funding',
    '筹资活动现金流出小计': 'outflow_cash_from_funding',
    '筹资活动产生的现金流量净额': 'net_cash_inflow_from_funding',
    '现金': 'cash',
    '现金等价物': 'cash_equivalent',
}

report_variables = a.rename(columns=names)

report_variables1=report_variables.replace({0.00:np.nan})
report_variables2=report_variables1.iloc[report_variables1.iloc[:,3:].dropna(how='all').index,:]
a=report_variables2.isnull().sum() / report_variables2.shape[0]
cols_to_retain=a[a<0.3].index.tolist()
report_variables3 =report_variables2.loc[:,cols_to_retain]

# 合并财报数据和比略数据
df2 = report_variables3.merge(ratios1,how='left',left_on=['sec_id','date_report'],right_on=['sec_id','date_report'])

# 获取2006-2015年沪深按市值排150的股票的财务指标及年收益率
# 获取close
conn = dk.MySQLProxy()
conn.connect("root", "123888", "indicator")
close_info = conn.query_as_dataframe("SELECT Year(date) as year, date, sec_id, close FROM time_series_variables WHERE Year(date) BETWEEN 2005 AND 2015")
close_begin=close_info.groupby(['sec_id','year'], as_index=False).apply(lambda x: x[x.date == x.date.min()])
close_begin = close_begin.rename(columns={'close': 'close_begin'})
close_ending=close_info.groupby(['sec_id','year'], as_index=False).apply(lambda x: x[x.date == x.date.max()])
close_ending = close_ending.rename(columns={'close': 'close_ending'})
close = close_begin.merge(close_ending,how='inner',left_on=['year','sec_id'], right_on=['year','sec_id'])[['year','sec_id','close_begin','close_ending']]
close=close.replace({0:np.nan})
close = close.dropna()
close['return_rate_annual'] = close['close_ending'] / close['close_begin'] -1

# 获得财报数据
## 市值指标
flag = conn.query_as_dataframe("SELECT Year(date) as year, sec_id, AVG(stock_total_shares) as stock_float_shares_avg,FROM time_series_variables GROUP BY Year(date), sec_id;")

fr = conn.query_as_dataframe("SELECT *, YEAR(date_report) as year FROM report_variables1 WHERE (Year(date_report) BETWEEN '2005' and '2015') and  MONTH(date_report) = 12;")

df = fr.merge(flag, how='inner',right_on=['sec_id','year'],left_on=['sec_id','year'])
df['market'] = df['sec_id'].apply(lambda x: "上交所" if x[:2]=='SH' else "深交所")
df=df.sort_values(by=['year','market','stock_float_shares_avg'], ascending=[True, True,False])
df1=df.groupby(by=['year','market']).apply(lambda x: x.head(150)) #  筛选沪深市值排名前150的股票
df2=df1.copy()
ana_vars=df2.columns.drop(['sec_id','date_report','date_published','year','stock_float_shares_avg','market'])
# 归一化处理
df2[ana_vars] = (df2[ana_vars] - df2[ana_vars].min())/ (df2[ana_vars].max() - df2[ana_vars].min())

# 合并财报数据和年收益率
df3 = df2.merge(close[['year', 'sec_id', 'return_rate_annual']], how='inner', left_on=['year','sec_id'], right_on=['year','sec_id'])
missing_flag = df1.isnull().sum()/df1.shape[0] <= 0  # 删除缺失值
cols_to_retain=missing_flag[missing_flag].index.tolist()
df4 = df3[cols_to_retain]
