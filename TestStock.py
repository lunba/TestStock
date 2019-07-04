#import tushare as ts
from sqlalchemy import create_engine
import pandas as pd
import pymysql
import time
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import QApplication , QMainWindow
from simpleD import SimpleDialogForm
#ts.set_token('27175de420b6c6c15c86b010dae94984541bd72d0ddffa6e8cf4da30')
#pro = ts.pro_api()
#获取票信息
#df = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date,market,list_status,is_hs')
#df.to_csv('d:\\663.csv',encoding='utf-8-sig')

#获取公司信息
#df = pro.stock_company(exchange='SZSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,main_business,business_scope')   
#df.to_csv('d:\\Company_info.csv',encoding='utf-8-sig')
#df = pro.stock_company(exchange='SSE', fields='ts_code,chairman,manager,secretary,reg_capital,setup_date,province,main_business,business_scope')   
#df.to_csv('d:\\Company_info_sh.csv',encoding='utf-8-sig')

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
  #获取实时行情
  #ts.get_today_all()

if __name__=='__main__':    
    app = QApplication(sys.argv)
    main = SimpleDialogForm()#创建一个主窗体（必须要有一个主窗体）
    main.show()#主窗体显示
    sys.exit(app.exec_())

