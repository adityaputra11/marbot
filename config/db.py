import os
import asyncpg

async def get_db():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    database = os.getenv("DB_NAME")  # ubah sesuai nama variabel environment-mu
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    
    print(f"user: {user}")
    print(f"password: {password}")
    print(f"database: {database}")
    print(f"host: {host}")  
    print(f"port: {port}")

    if not all([user, password, database, host, port]):
        raise EnvironmentError("Database environment variables not set properly.")

    conn = await asyncpg.create_pool(
        user=user,
        password=password,
        database=database,
        host=host,
        port=port,
        statement_cache_size=0,  # matikan cache prepared statement
    )
    print(f"Connected to database: {conn}")
    return conn