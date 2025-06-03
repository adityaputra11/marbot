import os
import asyncpg
from datetime import datetime, timedelta, timezone
from config.db import get_db

class AuthRepository: 
    async def register(self, username: str, name:str):
      print(f"username: {username}")
      print(f"name: {name}")
      try:
          conn = await get_db()
          print(f"conn: {conn}")
          check_username = await conn.fetchrow(
              'SELECT * FROM users WHERE username = $1',
              username
          )
          
          if check_username:
              return {"status": False, "message": "Username sudah terdaftar"}
              
          # Insert user baru
          await conn.execute(
              'INSERT INTO users (username, name) VALUES ($1, $2)',
              username, name
          )
          
          await conn.close()
          return {"status": True, "message": "Registrasi berhasil"}
          
      except Exception as e:
          return {"status": False, "message": str(e)}

    async def login(self, username: str):
      try:
          conn = await get_db()  
          # Cek kredensial login
          user = await conn.fetchrow(
              'SELECT * FROM users WHERE username = $1',
              username
          )
          
          if not user:
              return {"status": False, "message": "Username tidak ditemukan"}
            
          await conn.close()
          return {
              "status": True,
              "message": "Login berhasil",
              "data": {
                  "id": user['id'],
                  "username": user['username']
              }
          }
          
      except Exception as e:
          return {"status": False, "message": str(e)}

    async def subscribe(self, username: str):
      try:
          conn = await get_db()
          user = await conn.fetchrow(
              'SELECT * FROM users WHERE username = $1',
              username
          )
          if not user:
              return {"status": False, "message": "Username tidak ditemukan"}
          conn = await get_db()
          await conn.execute(
              'INSERT INTO subscriptions (user_id, plan, status, start_date, end_date) VALUES ($1, $2, $3, $4, $5)',
              user['id'], 'premium', 'active', datetime.now(), datetime.now() + timedelta(days=30)
          )
          await conn.close() 
          return {"status": True, "message": "Berhasil berlangganan"} 
      except Exception as e:
          return {"status": False, "message": str(e)}