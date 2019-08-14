from django.test import TestCase
import datetime
import time
# Create your tests here.
# 'timestamp', '2019-08-14T10:13:43.893301'


d1 = datetime.datetime.strptime('2019-08-14T 10:13:43.893301', '%Y-%m-%d %H:%M:%S.%f')
d2 = datetime.datetime.strptime('2015-03-02 17:41:20', '%Y-%m-%d %H:%M:%S')
# timestamp = datetime.strptime(list(res)[0][2], '%Y-%m-%d %H:%M:%S')
print(d1)
print(d2)