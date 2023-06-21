import asyncio
import logging
import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters import Command
from plugins.luhn import LuhnSummarizer

logging.basicConfig(level=logging.INFO, filename='../data/log.log')
with open('../credentials/token.txt', 'r') as f:
    token = f.read()
bot = Bot(token=str(token))
dp = Dispatcher(bot)


@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer('Hello!')


@dp.message_handler(content_types=['document'])
async def luhn_summarization(message: types.Message):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    username = message.from_user.id
    destination = str(datetime.datetime.now()) + '_' + str(username) + '.txt'
    destination = destination.replace('-', '_').replace(' ', '_').replace(':', '_')
    await bot.download_file(file_path, './data/requests/' + destination)
    summarizer = LuhnSummarizer()
    with open('./data/requests/' + destination, 'r', encoding='utf-8') as f:
        text = f.read()
    summary = summarizer.process_text(text)
    with open('./data/answers/' + destination[:-4] + '_answer_' + '.txt', 'w') as f:
        f.write(summary)
    await message.answer_document(
        open('./data/answers/' + destination[:-4] + '_answer_' + '.txt', 'rb')
    )


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
