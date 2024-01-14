from sqlalchemy import create_engine
from sqlalchemy.engine import URL

url = URL.create(
    drivername="postgresql",
    username="coderpad",
    host="/tmp/postgresql/socket",
    database="coderpad"
)

engine = create_engine(url)