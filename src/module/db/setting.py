from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

DATABASE = 'mysql://%s:%s@%s/%s?charset=utf8' % (
    "anigiri",      # user_name
    "password",  # password
    "mysql",    # host_ip
    "anigiri_db",   # db_name
)

ENGINE = create_engine(
    DATABASE,
    encoding = "utf-8",
    echo=False # Trueだと実行のたびにSQLが出力される
)

session = scoped_session(
  # ORM実行時の設定。自動コミットするか、自動反映するなど。
    sessionmaker(
        autocommit = False,
        autoflush = True,
        bind = ENGINE
    )
)

# modelで使用する
Base = declarative_base()
Base.query = session.query_property()
