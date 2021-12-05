from sqlalchemy import create_engine
from sqlmodel import SQLModel

sqlite_file_name = "whatif"
sqlite_url = f"mysql+pymysql://root:whatif@whatif_mysql:3306/{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
