import requests
from io import StringIO
import pandas as pd
import numpy as np
import datetime
import time

class stock_filter():
  
  def crawler(self, date):
    url = requests.post('http://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date=' + str(date).split(' ')[0].replace('-','') + '&type=ALL')
    self.df = pd.read_csv(StringIO("\n".join([i.translate({ord(c): None for c in ' '}) 
                                        for i in url.text.split('\n') 
                                        if len(i.split('",')) == 17 and i[0] != '='])), header=0)
    self.df = self.df.set_index('證券代號')
    self.df['成交金額'] = self.df['成交金額'].str.replace(',','')
    self.df['成交股數'] = self.df['成交股數'].str.replace(',','')
    return self.df
  
  def running(self, n_days=3, max_fail_count = 4, date=datetime.datetime.now()): 
    #variable initial
    data = {}
    fail_count = 0
    n_days = n_days
    max_fail_count = max_fail_count
    date = date

    while n_days > 0 :

      print('loading', date)
      # crawler
      try:
          data[date.date()] = self.crawler(date)
          print('complete!')
          fail_count = 0
      except:
          print('沒開盤')
          fail_count += 1
      else:
        n_days -= 1
      if fail_count > max_fail_count:
        break
      
      #update day
      date -= datetime.timedelta(days=1)
      time.sleep(20)

      

    #取得股數
    df = pd.DataFrame({k:d['成交股數'] for k,d in data.items()}).transpose()
    df.index = pd.to_datetime(df.index)
    df = df.transpose()   

    #剔除空值
    df.dropna(axis=0, inplace=True)

    #convert data type and rename columns
    df = df.astype(str).astype(int)
    df.columns = ['今天', '昨天','前天']

    return df

  def get_time(self):
    y, m, d = map(int, input().split())
    d = datetime.datetime(y, m, d)
    return d
  
  def filter1(self,  w1 = (1/4) , w2 = 3, day = 'today'):
    da = day
    if da == 'today':
      d = datetime.datetime.now()
    else:
      d = get_time()

    df = self.running(date = d)
    w1 = w1
    w2 = w2

    #calculate threshold
    df['threshold1'] = df['今天'] - w1 * df['昨天']
    df['threshold2'] = df['前天'] * w2 - df['昨天']

    #set filter
    f1 = df['threshold1'] < 0
    f2 = df['threshold2'] < 0

    #write to new df
    df = df[(f1 & f2 )].sort_values('前天',ascending=False)

    df = df.drop(['threshold1', 'threshold2'], axis=1)

    df.index.name = None

    return df
