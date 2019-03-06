from sqlalchemy import create_engine, Float
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class UNLocode(Base):
    __tablename__ = "unlocode_list_with_gps"
    __columns__ = ["id", "country", "location", "name", "lat", "lng"]
    id = Column(String(10), primary_key=True)
    country = Column(String(100))
    location = Column(String(100))
    name = Column(String(100))
    lat = Column(Float())
    lng = Column(Float())

    def __init__(self, row):
        item = {"id": "%s%s" % (row["Country"], row["Location"])}
        for key in row:
            if key in self.__columns__:
                item[key] = row[key]
        super().__init__(**item)
        return


def start_mysql_session(config):
    uri = config["MYSQL_EP"]
    engine = create_engine(
        uri,
        encoding="utf8",
        echo=False,
        pool_size=30,
        pool_recycle=15)


    Session = sessionmaker(bind=engine)
    session = Session()
    return engine, session