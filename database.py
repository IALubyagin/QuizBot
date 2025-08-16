# database.py
# Объявление и определение класса Database, реализующего асинхронный доступ к базе aiosqlite
# В текущей версии не используется

import aiosqlite
import asyncio

#
class Database:
  """
  """
  def __init__(self, db_path):
    self.db_path = db_path
    self.connection = None
    self.lock = asyncio.Lock()

  async def connect(self):
    if not self.connection:
      self.connection = await aiosqlite.connect(self.db_path)

  async def close(self):
    if self.connection:
      await self.connection.close()
      self.connection = None

  async def __aenter__(self):
    await self.connect()
    return self

  async def __aexit__(self, exc_type, exc_val, exc_tb):
    await self.close()

  async def execute(self, query, params=None):
    if self.connection is None:
      raise RuntimeError("Database connection is not established.")
    async with self.connection.execute(query, params or ()) as cursor:
      await self.connection.commit()
      return cursor

  async def fetchall(self, query, params=None):
    async with self.lock:
      async with self.execute(query, params) as cursor:
        return await cursor.fetchall()


  async def fetchone(self, query, params=None):
    async with self.lock:
      async with self.execute(query, params) as cursor:
        return await cursor.fetchone()
