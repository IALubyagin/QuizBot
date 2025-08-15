# quizstate.py

import aiosqlite
# import database

# Зададим имя базы данных
DB_NAME = 'quiz_bot.db'

async def create_table():
  # async with database.Database(DB_NAME) as db:
  async with aiosqlite.connect(DB_NAME) as db:
    await db.execute('CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER, right_answers INTEGER)')
    await db.commit()

async def update_quiz(user_id, index, right_answers):
  # Создаем соединение с базой данных (если она не существует, она будет создана)
  async with aiosqlite.connect(DB_NAME) as db:
    # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
    await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index, right_answers) VALUES (?, ?, ?)', (user_id, index, right_answers))
    # Сохраняем изменения
    await db.commit()

async def get_quiz_state(user_id):
  # Подключаемся к базе данных
  async with aiosqlite.connect(DB_NAME) as db:
    # Получаем запись для заданного пользователя
    async with db.execute('SELECT question_index, right_answers FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
      # Возвращаем результат
      results = await cursor.fetchone()
      if results:
        return results
      else:
        return (0, 0)

async def get_quiz_info():
  async with aiosqlite.connect(DB_NAME) as db:
    async with db.execute('SELECT * FROM quiz_state') as cursor:
      results = await cursor.fetchone()
      return results
