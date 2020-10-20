
import json
from urllib.request import urlopen
import time
import datetime

from_date_str = "2020-10-16 09:00:00"
from_date = datetime.datetime.strptime(from_date_str, "%Y-%m-%d %H:%M:%S")
from_date_tst = int(datetime.datetime.timestamp(from_date))

to_date_str = "2020-10-16 15:00:00"
to_date = datetime.datetime.strptime(to_date_str, "%Y-%m-%d %H:%M:%S")
to_date_tst = int(datetime.datetime.timestamp(to_date))

url = "https://dchart-api.vndirect.com.vn/dchart/history?resolution=D&symbol=BID&from="+str(from_date_tst) +"&to="+str(to_date_tst)
#https://dchart-api.vndirect.com.vn/dchart/history?resolution=D&symbol=BID&from=1602649896&to=1602749896&fbclid=IwAR33kxjfH5Ww4hAu6xnXGJBoTUIg2r_wCecu1udtXh-ZnClJ-HfaFlKM22g
#1602649896
#1602813600
#--------
#1602749896
#1602835200
#1602835030522
print(url)
response = urlopen(url)

# data = json.loads(response.read())
#
# print(data)
# print(data['t'][0])