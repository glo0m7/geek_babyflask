
from users import *


do = 0
if do:
    db.drop_all()
else:
    # Admin 信息
    name = 'LiUU'
    passwd='WoLiYouYouXueZhangTianXiaDiYi'
    token = hashlib.md5((name+passwd).encode("utf8")).hexdigest()
    flag="SYC{}"
    signature = 'LiUU senior is th3 most handsome!'
    #创建库
    db.create_all()

    LiUU = DB_Admin(name=name,passwd=passwd,token=token,flag=flag,signature=signature)

    db.session.add(LiUU)
    db.session.commit()

