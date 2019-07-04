import tushare as ts
import pandas as pd
import pymysql
import datetime
import time
import sys
import os
from Caculate1 import CaculateClass
class StockinfoUpdate(object):
  def __init__(self,start_date):
      ts.set_token('27175de420b6c6c15c86b010dae94984541bd72d0ddffa6e8cf4da30')
      self.pro = ts.pro_api()
      self.rq = time.strftime('%Y%m%d', time.localtime(time.time()))
      self.rq1 = (datetime.datetime.now()+datetime.timedelta(days=1)).strftime('%Y%m%d')#明天
      self.file_subpath = 'd:/teststock/' + self.rq
      self.start_date = start_date
#获取票信息
#df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,market,list_status,is_hs')
#df.to_csv('d:\\663.csv',encoding='utf-8-sig')

  def get_company_info(self):
  #获取公司信息
    if  not os.path.exists(self.file_subpath+ '/companyinfo'):
        os.makedirs(self.file_subpath+ '/companyinfo')
    df = self.pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,main_business,business_scope')
    df.to_csv(self.file_subpath+ '/companyinfo/Company_SZ.csv',encoding='utf-8-sig')
    df = self.pro.stock_company(exchange='SSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,main_business,business_scope')   
    df.to_csv(self.file_subpath+ '/companyinfo/Company_SH.csv',encoding='utf-8-sig')


  def get_daily_info(self,cal_list):
  #获取每日行情
    if  not os.path.exists(self.file_subpath+ '/dairy'):
        os.mkdir(self.file_subpath+ '/dairy/')
    print(cal_list)
    for cal_date in cal_list:
        df = self.pro.daily(trade_date=cal_date)
        df.to_csv(self.file_subpath+ '/dairy/'+cal_date+'.csv',encoding='utf-8-sig')

  def get_now_info(self):
  #获取实时行情
    if  not os.path.exists(self.file_subpath+ '/nowinfo'):
        os.makedirs(self.file_subpath+ '/nowinfo')
    df = ts.get_today_all()
    sql = 'select ts_code from stockinfo'
    result=CaculateClass.con_sql("stockana",sql)
    df1 = pd.DataFrame(list(result)).drop_duplicates()
    df1[1]= df1[0].map(lambda x:x.strip()[0:6])
    df2 = pd.merge(df,df1,left_on="code",right_on=1)
    df2.to_csv(self.file_subpath + '/nowinfo/nowinfo.csv',encoding='utf-8-sig')
    return df2
   #1）.loc,.iloc,.ix,只加第一个参数如.loc([1,2]),.iloc([2:3]),.ix[2]…则进行的是行选择
   #2）.loc,.at，选列是只能是列名，不能是position
   #3）.iloc,.iat，选列是只能是position，不能是列名
   #4）df[]只能进行行选择，或列选择，不能同时进行列选择，列选择只能是列名。

  def get_yesterday_info(self,ts_codes):
  #获取昨日行情

    sql = 'select ts_code，close,change,vol,amount from dairy where trade_date=%s and ts_code=%s'%()
    result=CaculateClass.con_sql("stockana",sql)
    df1 = pd.DataFrame(list(result)).drop_duplicates()
    df1[1]= df1[0].map(lambda x:x.strip()[0:6])
    df2 = pd.merge(df,df1,left_on="code",right_on=1)
    df2.to_csv(self.file_subpath + '/nowinfo/nowinfo.csv',encoding='utf-8-sig')
    return df2
  def get_news(self):
  #获取新闻
    if  not os.path.exists(self.file_subpath+ '/news'):
        os.makedirs(self.file_subpath+ '/news')
    df = self.pro.news(src='sina', start_date=self.rq, end_date=self.rq1)
    df.to_csv(self.file_subpath + '/news/news.csv',encoding='utf-8-sig')

  def get_adj_factor(self,cal_list):
  #获取复权因子
    if  not os.path.exists(self.file_subpath+ '/factor'):
        os.makedirs(self.file_subpath+ '/factor/')
    for cal_date in cal_list:
        df = self.pro.adj_factor(ts_code='', trade_date=cal_date)
        df.to_csv(self.file_subpath + '/factor/'+cal_date+'.csv',encoding='utf-8-sig')



  def get_calendar(self):
  #获取交易日历
    if  not os.path.exists(self.file_subpath+ '/trade_cal'):
        os.makedirs(self.file_subpath+ '/trade_cal')
    df = self.pro.trade_cal(exchange='', start_date=self.start_date, end_date=self.rq ,is_open='1')
    df.to_csv(self.file_subpath + '/trade_cal/trade_cal.csv',encoding='utf-8-sig')
    return df




#提取000001全部复权因子
#df = pro.adj_factor(ts_code='000001.SZ', trade_date='')
#提取2018年7月18日复权因子
#df = pro.adj_factor(ts_code='', trade_date='20180718')
#获取资讯
#df = pro.news(src='sina', start_date='20190426', end_date='20190428')
#df.to_csv('d:\\news.csv',encoding='utf-8-sig')

#获取周线
#df = pro.index_weekly(ts_code='000001.SH', start_date='20000101', end_date='20190429', fields='ts_code,trade_date,open,high,low,close,vol,amount')
#df.to_csv('d:\\s3z.csv',encoding='utf-8-sig')

#获取日线
#df = pro.daily(ts_code='000001.SZ', start_date='20180701', end_date='20180718')

#engine = create_engine("mysql+pymysql://root:root@localhost:3306/stockana?charset=utf8")
#获取每日行情
#for aaa in result:
    #df = pro.daily(ts_code=aaa[0], start_date='19980101', end_date='20190430')
   # df.to_csv('f:\\python\\csv\\'+aaa[0]+'.csv',encoding='utf-8-sig')
   # time.sleep(0.3)
#写入数据库
#for aaa in result:
   # df=pd.read_csv('f:\\python\\csv\\'+aaa[0]+'.csv',encoding='gbk')
   # df.drop(df.columns[0],axis=1,inplace=True)
   # df.to_sql(name='dairy',con=engine,if_exists='append',index=False,index_label=False)

#for aaa in result:
    #df = pro.adj_factor(ts_code=aaa[0], trade_date='')
   #df.to_csv('f:\\python\\fqyz-csv\\'+aaa[0]+'.csv',encoding='utf-8-sig')



#for aaa in result:
    #df=pd.read_csv('f:\\python\\fqyz-csv\\'+aaa[0]+'.csv',encoding='gbk')
    #df.drop(df.columns[0],axis=1,inplace=True)
    #df.to_sql(name='factor',con=engine,if_exists='append',index=False,index_label=False)


    # for aaa in result[0]:
  #if cc>=1057:
    #df = pro.fina_mainbz(ts_code=aaa,type='P')
    #df.to_csv('f:\\python\\mainbz-csv\\'+aaa+'.csv',encoding='utf-8-sig ')
   # time.sleep(1)
  #cc=cc+1







