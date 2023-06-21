# TSU_AI_M4

## About:
The work was performed as part of the machine learning course at the 3rd year of TSU of the HITS faculty. Author - Klassen Fedor

## Description
The work is presented in two parts - a telegram bot and a plug-in for summarizing the text by the Luhn method.
The model supports two languages - English and Russian. Automatic language detection is available.

## How to use
You can check the functionality of the application both from the command line and via Telegram.

### CLI
```
>python luhn.py process_text "your text"
```

### Telegram bot
 - Find TSU_AI_M4_2023 bot in Telegram
 - Choose the document and send it to the bot
 - Receive the document with summary
 - Download and work with this document

## Demo
![screen-gif](./gif.gif)

## Sources
https://courses.ischool.berkeley.edu/i256/f06/papers/luhn58.pdf

https://habr.com/ru/articles/595517/

https://pymorphy2.readthedocs.io/en/stable/index.html

https://www.nltk.org/
