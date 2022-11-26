from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN_API = "5988049870:AAF9JgMZQjX3jL55y9p8RVE2UDVMqIBBN5k"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())



