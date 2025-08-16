# Игровой Telegram бот Quiz Bot для проведения квиза

Список команд:

- /start - начало работы

- /quiz - команда начать игру

- /info - вывод дополнительной информации

- /help - отображение списка команд

Вопросы организованы в виде списка словарей с тремя ключами:

- question - вопрос

- options - варианты ответов

- correct_option - индекс правильного ответа

Состояние процесса игры хранится в базе данных SQLite. Структура таблицы:

```js
CREATE TABLE quiz_state

(

    user_id INTEGER PRIMARY KEY, --

    question_index INTEGER, --

    right_answers INTEGER --

)
```

Ссылки:

- @DTQuizHammavetBot

- https://t.me/DTQuizHammavetBot

Установка:

git clone git@github.com:IALubyagin/QuizBot.git
