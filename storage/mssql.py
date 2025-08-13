# storage/mssql.py
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
import pandas as pd
import os

def mssql_engine_from_env(driver="ODBC Driver 17 for SQL Server") -> Engine:
    server = os.getenv("MSSQL_SERVER", "localhost")
    database = os.getenv("MSSQL_DB", "RSNA")
    user = os.getenv("MSSQL_USER", "sa")
    password = os.getenv("MSSQL_PASSWORD", "your_password")
    conn_str = f"mssql+pyodbc://{user}:{password}@{server}/{database}?driver={driver.replace(' ', '+')}"
    return create_engine(conn_str, fast_executemany=True)

def bulk_insert(df: pd.DataFrame, table: str, engine: Engine):
    # Lưu ý: if_exists='append' -> tránh ghi đè; đảm bảo PK/UK trong DB để chống trùng
    df.to_sql(table, engine, if_exists="append", index=False)
