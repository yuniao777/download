
from aligo import Aligo
import os

ali = Aligo()
p = os.path.join(os.getcwd(), 'zh_cn.csv')
print(p)
up_file = ali.upload_file(p)
