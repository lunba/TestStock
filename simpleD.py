from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication  ,QWidget  , QGridLayout, QPushButton
from Caculate1 import CaculateClass
from Ui_Dialog import Ui_Dialog
from StockinfoUpdate import StockinfoUpdate
from sqlalchemy import create_engine
import pandas as pd
#import sys
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

class SimpleDialogForm(Ui_Dialog, QtWidgets.QMainWindow):#从自动生成的界面类继承
    def __init__(self, parent = None):

        super(SimpleDialogForm, self).__init__()
        self.setupUi(self)#在此设置界面
        #self.dateEdit.setDate(currentDate())
        
        self.pushButton.clicked.connect(self.on_click)
        self.pushButton_2.clicked.connect(self.updateinfo)
        self.pushButton_3.clicked.connect(self.on_click3)
        #self.pushButton_2.clicked.connect(self.closeApp)
        self.gridlayout = QGridLayout(self.groupBox_3)  # 继承容器groupBox
        self.F = MyFigure()
        self.gridlayout.addWidget(self.F)
        CaculateClass.Zero_Stock(['fund','transaction'])
    def on_click3(self):
          sql = "SELECT a.ts_code,b.name,a.bz_item FROM mainbz as a,stockinfo as b where a.bz_item like '%s' and a.ts_code=b.ts_code"%('%'+str(self.lineEdit_3.displayText())+'%')
          
          result=CaculateClass.con_sql('stockana',sql)
          if(result == ()):
              self.textEdit_2.append("未找到")
          else:

          #执行结果转化为dataframe
              df = pd.DataFrame(list(result)).drop_duplicates()
          #df.columns=['代号','名称','主营']
              print(df)
              self.textEdit_2.setPlainText("")
              self.textEdit_2.append('代号          名称          主营')
              for row in df.values:
                  self.textEdit_2.append(row[0]+"  "+row[1]+"    "+row[2])
    def updateinfo(self):
          start1 = CaculateClass.get_lastest_time()
          print(start1)
          stupdate = StockinfoUpdate(start1)
          #comp_list = CaculateClass.con_sql('stockana','select ts_code from stockinfo') 
          #print(comp_list)
          cal_list = list(stupdate.get_calendar()['cal_date'])
          stupdate.get_daily_info(cal_list)
          stupdate.get_adj_factor(cal_list)
          CaculateClass.write_db(cal_list,stupdate.file_subpath,['factor'])  
          CaculateClass.write_db(cal_list,stupdate.file_subpath,['dairy'])
          #stupdate.get_now_info()

    def on_click(self):
        if (self.radioButton.isChecked()):
          self.gridlayout.removeWidget(self.F)
          start_time = self.dateEdit_2.date().toPyDate()
          end_time = self.dateEdit.date().toPyDate()
          code1 = self.lineEdit.text()
          print(end_time)
          db = 'stockana'
          sql1 = "select trade_date,adj_factor from factor where ts_code='%s'"%(code1)
          sql2 = "select trade_date,close from dairy where ts_code='%s'"%(code1)
          df=CaculateClass.Cac_ave_fiveday(db,sql1,sql2)
          df.sort_index(inplace=True)
          print(df)
          df2=pd.rolling_mean(df['price'],5)
          df['ave5']=df2
          df=df[df.index<=end_time]
          df=df[df.index>=start_time]
          #df=CaculateClass.con_sql(db,sql2)
          #df=df['price','ave5'].map(lambda x:('%.2f')%x)
          print(df)
          #第五步：定义MyFigure类的一个实例 
          self.F = MyFigure()
          self.F.axes.plot(df)
        #第六步：在GUI的groupBox中创建一个布局，用于添加MyFigure类的实例（即图形）后其他部件。
          
          #self.gridlayout = QGridLayout(self.groupBox_3)  # 继承容器groupBox
          #self.F.setLayout(self.gridlayout)
         
          self.gridlayout.addWidget(self.F)
          #策略1，突破5日均线即买，戳破5日线即卖
          status = 0
          money=[0]
          stock_num = 0
          total_fund = 200000
          for index, row in df.iterrows():
              if row['price']>row['ave5'] and status == 0:
                  stock_num = CaculateClass.Buy_Stock(total_fund+sum(money),row['price'],code1,index)
                  status = 1
                  money.append(-(stock_num * round(row['price'],2)))
              if  row['price']<row['ave5'] and status == 1:  
                  money.append(int(stock_num * round(row['price'],2) * 0.999))
                  stock_num = CaculateClass.Sell_Stock(total_fund+sum(money),row['price'],stock_num,code1,index)
                  status = 0
          if  status == 1:  
                 # money.append(-money[-1])
                  money.append(int(stock_num * round(row['price'],2) * 0.999))
                  CaculateClass.Sell_Stock(total_fund+sum(money),row['price'],stock_num,code1,index)
                  stock_num = 0
                  status = 0                 
          sql3="select fund_money from fund"
          result = CaculateClass.con_sql("stockana",sql3)
          self.lineEdit_7.setText(str(int(sum(money)+200000)))
          self.textEdit.setPlainText(str(list(result)))
          #CaculateClass.Buy_Stock(200000,3.568,code1,end_time)
         #print(self.textEdit.toPlainText())
        if (self.radioButton_2.isChecked()):
            print("ok")

#创建一个matplotlib图形绘制类
class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        #第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        #第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) #此句必不可少，否则不能显示图形
        #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)  
    #第四步：就是画图，【可以在此类中画，也可以在其它类中画】
        self.axes.plot()
