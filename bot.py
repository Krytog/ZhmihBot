#Import bot stuff
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


#Import functionality
from function_implementation import ZhmihImage


#Import config
from bot_config import key


#Bot setup
bot = Bot(key)
dp = Dispatcher(bot, storage=MemoryStorage())



#Bot code goes here
@dp.message_handler(commands=["start"])
async def start_function(message: types.Message):
	await message.answer("Привет! Жду команду. Если ты не знаешь, как я работаю, пиши /help")


@dp.message_handler(commands=["help"])
async def help_function(message: types.Message):
	await message.answer('''Ты можешь ввести следующие команды:
/start : выводит в чат приветствие
/help : выводит в чат это самое сообщение
/zhmih : ждёт от тебя фото, после чего применяет к нему эффект жмыха
/uppercaption : ждёт от тебя фото и текст, после чего добавляет в верхнюю часть картинки твой текст
/lowercaption : то же самое, что и предыдущая команда, только текст окажется внизу''')


class ZhmihState(StatesGroup):
	active = State()


@dp.message_handler(commands=["zhmih"])
async def zhmih_function(message: types.Message):
	await ZhmihState.active.set()
	await message.answer("Кидай фотку, я её жмыхну")

@dp.message_handler(state=ZhmihState.active, content_types=types.ContentType.all())
async def ApplyZhmih(message: types.Message, state: FSMContext):
	if message.photo:
		await message.photo[-1].download(str(message.photo[-1].file_id) + ".jpg")
		print("Photo was downloaded, its name is " + str(message.photo[-1].file_id) + ".jpg" )
	else:
		await message.answer("Ой, у тебя фотка какая-то странная. Не могу обработать")
	await state.finish()


async def startup(_):
	print("Bot was started at " + datetime.now().strftime("%d/%m/%y, %H:%M:%S"))


async def shutdown(_):
	print("\nBot was shutdown at " + datetime.now().strftime("%d/%m/%y, %H:%M:%S"))


if __name__ == '__main__':
	executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
