# bot.py
#@title Полный код бота для самоконтроля

# id=8260939020
# 8260939020:AAFPB8ELzijhICtGLCPd4Tt8Uv52vRCqK3w
# https://core.telegram.org/bots/apihttps://t.me/MDispatcherBot
# dtQuizBot/@DTQuizHammavetBot/t.me/DTQuizHammavetBot
# https://t.me/DTQuizHammavetBot


import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import F, html
from datetime import datetime
from quizstate import create_table, update_quiz, get_quiz_state
from questions import quiz_data

def bold(io):
  return html.bold(str(io))

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

default = DefaultBotProperties(
        parse_mode=ParseMode.HTML
        #
    )

# Замените "YOUR_BOT_TOKEN" на токен, который вы получили от BotFather
API_TOKEN = '8260939020:AAFPB8ELzijhICtGLCPd4Tt8Uv52vRCqK3w'

HELP = """
Вы можете выполнить следующие команды
/start - Начало работы
/help - Помощь
/quiz - Начать игру
/info - Получить дополнительную информацию
"""

# Объект бота
bot = Bot(token=API_TOKEN, default=default)
# Диспетчер
dp = Dispatcher()

dp["started_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")


def generate_options_keyboard(answer_options, right_answer):
  builder = InlineKeyboardBuilder()
  i = 0
  for option in answer_options:
    data = "1" if option == right_answer else "0"
    data += ':' + str(i)
    i += 1

    builder.add(types.InlineKeyboardButton(
        text=option,
        callback_data=data)
    )

  builder.adjust(1)
  return builder.as_markup()

async def get_question(message, user_id):
  # Получение текущего вопроса из словаря состояний пользователя
  current_question_index, _ = await get_quiz_state(user_id)
  current_question = quiz_data[current_question_index]
  correct_index = current_question['correct_option']
  opts = current_question['options']
  kb = generate_options_keyboard(opts, opts[correct_index])
  await message.answer(f"{bold(current_question_index + 1)}. {bold(current_question['question'])}",
                       reply_markup=kb)

async def new_quiz(message):
  user_id = message.from_user.id
  current_question_index = right_answers = 0
  await update_quiz(user_id, current_question_index, right_answers)
  await get_question(message, user_id)

@dp.callback_query()
async def answer(callback: types.CallbackQuery):
  chat_id = callback.from_user.id
  message = callback.message
  await callback.bot.edit_message_reply_markup(
      chat_id=chat_id,
      message_id=message.message_id,
      reply_markup=None
  )
  # Получение текущего вопроса из словаря состояний пользователя
  current_question_index, right_answers = await get_quiz_state(chat_id)

  current_question = quiz_data[current_question_index]
  correct_option = current_question['correct_option']
  options = current_question['options']

  right_answer = options[correct_option]
  data = callback.data.split(':')
  if data[0] == "1": # right answer
    right_answers += 1
  elif callback.data[0] == "0": # wrong answer
    ...

  await message.answer(f"Ваш ответ: {bold(options[int(data[1])])}\nПравильный ответ: {bold(right_answer)}")

  # Обновление номера текущего вопроса в базе данных
  current_question_index += 1
  await update_quiz(chat_id, current_question_index, right_answers)

  if current_question_index < len(quiz_data):
    await get_question(message, chat_id)
  else:
    await message.answer(f"Квиз завершен! Ваш результат: правильных ответов {bold(right_answers)}/{current_question_index}")


# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
  builder = ReplyKeyboardBuilder()
  builder.add(types.KeyboardButton(text="Начать игру"))
  await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

# Хэндлер на команду /info
@dp.message(Command("info", prefix='$/'))
async def cmd_info(message: types.Message, started_at: str):
  await message.answer(f"Бот запущен {started_at}")

# Хэндлер на команду /help
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
  await message.answer(HELP)

# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
  await message.answer(f"Давайте начнем квиз!")
  await new_quiz(message)


# Запуск процесса поллинга новых апдейтов
async def main():
  # Запускаем создание таблицы базы данных
  await create_table()
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())
