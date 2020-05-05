from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

from sqlalchemy_utils import database_exists

# 取得目前路徑
current_dir = os.path.dirname(__file__)

# 設定資料庫路徑
# db_path = 'sqlite:///{}/linebotClient.db'.format(current_dir)
db_path = os.environ['DATABASE_URL']

# 設定資料庫名稱以及路徑
engine = create_engine(db_path, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    engine.connect()

    if engine.dialect.has_table(engine, 'products'):
        return False
    else:
        Base.metadata.create_all(engine)
        return True
# 以下是離線的時候用的
# 如果資料庫不存在則建立資料庫以及回傳True
# if database_exists(db_path):
#     print("資料庫已存在")
#     return False
# else:
#     Base.metadata.create_all(bind=engine)
#     print("成功建立資料庫")
#     return True
