from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_URL = "postgresql://postgres.xnqjtwvmtlrkmnhugssp:Ahmed123@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres"

engine = create_engine(DB_URL)

LocalSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()