#Import bot stuff
from datetime import datetime
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext


#Import functionality
from function_implementation import ZhmihImage
from function_implementation import AddUpperCaption
from function_implementation import AddLowerCaption


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


#Zhmih feature
class ZhmihState(StatesGroup):
	active = State()


@dp.message_handler(commands=["zhmih"])
async def zhmih_function(message: types.Message):
	await ZhmihState.active.set()
	await message.answer("Кидай фотку, я жмыхну на ней все лица и немного фон")

@dp.message_handler(state=ZhmihState.active, content_types=types.ContentType.all())
async def ApplyZhmih(message: types.Message, state: FSMContext):
	if message.photo:
		name = message.from_user.username + str(message.photo[-1].file_id) + ".jpg"
		await message.photo[-1].download("files/inputs/" + name)
		print("Photo from " + message.from_user.username + " was downloaded at files/inputs folder, its name is " + name)
		ZhmihImage("files/inputs/" + name, "files/outputs/" + name, message.from_user.id)
		await bot.send_photo(message.chat.id, types.InputFile("files/outputs/" + name))
	else:
		await message.answer("Ой, у тебя фотка какая-то странная. Не могу обработать")
	await state.finish()


#Caption feature
class UpperCaptionState(StatesGroup):
	photo_name = State()
	text = State()


class LowerCaptionState(StatesGroup):
	photo_name = State()
	text = State()


@dp.message_handler(commands=["uppercaption"])
async def uppercaption_function(message: types.Message):
	await UpperCaptionState.photo_name.set()
	await message.answer("Кидай фотку, на которую надо добавить надпись")


@dp.message_handler(state=UpperCaptionState.photo_name, content_types=types.ContentType.all())
async def GetPhotoForUpperCaption(message: types.Message, state: FSMContext):
	if message.photo:
		name = message.from_user.username + str(message.photo[-1].file_id) + ".jpg"
		async with state.proxy() as data:
			data['photo_name'] = name
		await message.photo[-1].download("files/inputs/" + name)
		print("Photo from " + message.from_user.username + " was downloaded at files/inputs folder, its name is " + name)
		await UpperCaptionState.next()
		await message.answer("Теперь кидай текст")
	else:
		await message.answer("Ой, у тебя фотка какая-то странная. Не могу обработать")
		await state.finish()


@dp.message_handler(state=UpperCaptionState.text, content_types=types.ContentType.all())
async def GetTextForUpperCaption(message: types.Message, state: FSMContext):
	if message.text:
		name = "error"
		async with state.proxy() as data:
			name = data['photo_name']
		print(message.text)
		print(name)
		AddUpperCaption("files/inputs/" + name, "files/outputs/" + name, message.text)
		await bot.send_photo(message.chat.id, types.InputFile("files/outputs/" + name))
	else:
		await message.answer("Ой, у тебя текст какой-то странный. Не могу обработать")
	await state.finish()


@dp.message_handler(commands=["lowercaption"])
async def lowercaption_function(message: types.Message):
        await LowerCaptionState.photo_name.set()
        await message.answer("Кидай фотку, на которую надо добавить надпись")


@dp.message_handler(state=LowerCaptionState.photo_name, content_types=types.ContentType.all())
async def GetPhotoForLowerCaption(message: types.Message, state: FSMContext):
        if message.photo:
                name = message.from_user.username + str(message.photo[-1].file_id) + ".jpg"
                async with state.proxy() as data:
                        data['photo_name'] = name
                await message.photo[-1].download("files/inputs/" + name)
                print("Photo from " + message.from_user.username + " was downloaded at files/inputs folder, its name is " + name)
                await LowerCaptionState.next()
                await message.answer("Теперь кидай текст")
        else:
                await message.answer("Ой, у тебя фотка какая-то странная. Не могу обработать")
                await state.finish()


@dp.message_handler(state=LowerCaptionState.text, content_types=types.ContentType.all())
async def GetTextForLowerCaption(message: types.Message, state: FSMContext):
        if message.text:
                name = "error"
                async with state.proxy() as data:
                        name = data['photo_name']
                print(message.text)
                AddLowerCaption("files/inputs/" + name, "files/outputs/" + name, message.text)
                await bot.send_photo(message.chat.id, types.InputFile("files/outputs/" + name))
        else:
                await message.answer("Ой, у тебя текст какой-то странный. Не могу обработать")
        await state.finish()


async def startup(_):
	print("Bot was started at " + datetime.now().strftime("%d/%m/%y, %H:%M:%S"))


async def shutdown(_):
	print("\nBot was shutdown at " + datetime.now().strftime("%d/%m/%y, %H:%M:%S"))


if __name__ == '__main__':
	executor.start_polling(dp, on_startup=startup, on_shutdown=shutdown)
