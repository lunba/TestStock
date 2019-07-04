from sqlalchemy import create_engine
import pandas as pd
import pymysql
import time
import datetime
import matplotlib.pyplot as plt
import sys
class CaculateClass():
  def __init__(self):
      pass
  def con_sql(db,sql):
# 创建连接
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db=db, charset='utf8')
# 创建游标
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
# 关闭连接
    db.close()
#返回dataframe
    print(result)
    return result

  def insert_sql(db,sql):
# 创建连接
    db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='root', db=db, charset='utf8')
    db.autocommit(True)
# 创建游标
    cursor = db.cursor()
#value1为元组
    cursor.execute(sql)
#执行结果转化为dataframe
# 关闭连接
    cursor.close()
    db.close()
    return "ok"

#写入整张csv文件到数据库
  def write_db(cal_list,subpath,tablename):
      engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/stockana?charset=utf8")
      #写入数据库
      print(cal_list)
      print(subpath)
      for bbb in tablename:
          for aaa in cal_list:
             print(aaa)
             df=pd.read_csv(subpath+"/"+bbb+"/"+aaa+'.csv',encoding='gbk')
             df.drop(df.columns[0],axis=1,inplace=True)
             df.to_sql(name=bbb,con=engine,if_exists='append',index=False,index_label=False)

  def Cac_ave_fiveday(db,sql1,sql2):
    #db='stockana'
    #sql1 = "select trade_date,adj_factor from factor where ts_code='600166.SH'"
    result=CaculateClass.con_sql(db,sql1)
    #执行结果转化为dataframe,计算复权因子
    df = pd.DataFrame(list(result))
    df.columns=['trade_date','price']
    df.set_index('trade_date',inplace=True)
    df=df/max(df.values)
    #df.to_csv('f:\\python\\11'+'.csv',encoding='utf-8-sig')
    #sql2 = "select trade_date,close from dairy where ts_code='600166.SH'"
    result2=CaculateClass.con_sql(db,sql2)
    #执行结果转化为dataframe
    df1 = pd.DataFrame(list(result2))
    df1.columns=['trade_date','price']
    df1.set_index('trade_date',inplace=True)
    df2=df*df1
    df2.dropna(how='all',inplace=True)
    return df2

  def get_lastest_time():
  #获取最近一次更新时间
    sql = 'select trade_date from dairy order by trade_date desc limit 1'
    result  = CaculateClass.con_sql('stockana',sql)
    return (result[0][0]+datetime.timedelta(days=1)).strftime('%Y%m%d')
  def get_yesterday_time():
  #获取上个交易日时间，执行前需先更新
    sql = 'select trade_date from dairy order by trade_date desc limit 1'
    result  = CaculateClass.con_sql('stockana',sql)
    return (result[0][0].strftime('%Y-%m-%d'))

  def Zero_Stock(tablelist):
    #tablelist 需清空的数据库表的列表
    for dlist in tablelist:
       sql="delete from %s"%dlist       
       CaculateClass.insert_sql('stockana',sql)    
    return "ok"

  def Buy_Stock(total_fund,price,ts_code,trade_date):
    #获取价格，计算可买数量，写入Transaction表，同时写入fund 表，记录所花款项
    type1='buy'
    price = round(price,2)
    number = (int(total_fund / price /100))*100
    sql="INSERT INTO transaction(ts_code,trade_date,deal_number,deal_type,deal_price) VALUES ('%s','%s',%s,'%s',%s)" %(ts_code,trade_date,number,type1,price)
    sql1="INSERT INTO fund(trade_date,fund_money,deal_type) VALUES ('%s',%s,'%s')" %(trade_date,total_fund-(number * price),type1)   
    CaculateClass.insert_sql('stockana',sql)
    CaculateClass.insert_sql('stockana',sql1)
    return number

  def Sell_Stock(total_fund,price,number,ts_code,trade_date):
     #获取价格，获取可卖数量，写入Transaction表，同时写入fund 表，记录所得款项，再记录1/千的交易费用
    type1='sell'
    type2='interest'
    price = round(price,2)
    sql="INSERT INTO transaction(ts_code,trade_date,deal_number,deal_type,deal_price) VALUES ('%s','%s',%s,'%s',%s)" %(ts_code,trade_date,number,type1,price)
    sql1="INSERT INTO fund(trade_date,fund_money,deal_type) VALUES ('%s',%s,'%s')" %(trade_date,total_fund,type1)

    CaculateClass.insert_sql('stockana',sql)
    CaculateClass.insert_sql('stockana',sql1)
    #db.close()
    return 0