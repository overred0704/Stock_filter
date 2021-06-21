# Stock_filter

### <<社畜的財務自由計畫>>裡面的其中一項策略
[博客來連結](https://www.books.com.tw/products/0010879900)

## 爆漲的前兆:

**成交量暴增(比前一個交易日多500~1000%**

**隔天成交量急速下降(25%以下**


### 目前是根據這個去篩選可能可以研究的股票

後續搭配線型跟資訊去判斷

重要指標次序:成交量>>線型>>相關資訊

希望可以賺錢辣...

## 執行

```python
!git clone https://github.com/overred0704/Stock_filter
from Stock_filter.filter_v1 import filter
```

### 指定物件
```python
f = filter()
f.filter1( w1 = (1/4) , w2 = 3, day = 'today')
```

### 預設是今天日期 要修改的話把day裡面的str改成other
```python
f.filter1( w1 = (1/4) , w2 = 3, day = 'other')
```

### 之後會跳出輸入介面 輸入[年 月 日]就可以

![Imgur](https://imgur.com/UptCHHA.png)

### 若要修改權重的話改w1, w2那邊就可以
