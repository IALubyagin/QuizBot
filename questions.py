# questions.py

# Структура квиза: { question, options, correct_option }

quiz_data = [
  {
    'question': 'Что такое Python?',
    'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
    'correct_option': 0
  },
  {
    'question': 'Какой тип данных используется для хранения целых чисел?',
    'options': ['int', 'float', 'str', 'natural'],
    'correct_option': 0
  },
  {
    'question': 'Каков порядок выполнения нескольких декораторов для одной функции?',
    'options': ['Рандомно', 'Снизу вверх', 'Сверху вниз', 'Зависит от реализации'],
    'correct_option': 1
  },
  {
    'question': 'Что такое поток?',
    'options': ['Коллекция в языке программирования', 'То же, что и процесс', 'Подзадача внутри процесса', 'Видео контент'],
    'correct_option': 2
  },
  {
    'question': 'Что выведет следующий код: s = \'Python\'; s.upper(); print(s) ?',
    'options': ['PYTHON', 'nohtyP', 'python', 'Python'],
    'correct_option': 3
  },
  {
    'question': 'Какие задачи хорошо параллелятся?',
    'options': ['всякие', 'CPU-bound', 'I/O-bound', 'Зависит от архитектуры'],
    'correct_option': 2
  },
  {
    'question': 'Что выведет следующий код: print(\'abcdef\'[None:3]) ?',
    'options': ['abcdef', 'abc', 'def', 'TypeError'],
    'correct_option': 1
  },
  {
    'question': 'Асинхронный фреймворк для Telegram Bot API - это...',
    'options': ['asyncio', 'asynctgbotapi', 'aiohttp', 'aiogram 3'],
    'correct_option': 3
  },
  {
    'question': 'Лучший язык программирования',
    'options': ['Python', 'C++', 'Java', 'JS'],
    'correct_option': 0
  },
  {
    'question': 'Когда же это кончится?!',
    'options': ['Не хочу Вас расстраивать', 'Уточните, пожалуйста, вопрос', 'Когда-нибудь это кончится', 'Марковна, никогда!'],
    'correct_option': 1
  },
]

def get_current_question(current_question):
  correct_index = current_question['correct_option']
  opts = current_question['options']
  right_answer = opts[correct_index]
  i = 0
  for option in opts:
    data = "1" if option == right_answer else "0"
    data += ':' + str(i)
    i += 1
