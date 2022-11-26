from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage


TOKEN_API = "5607570842:AAFP4WjVh2MyLOV8QBdqr_KROfJH_GoOTXY"

bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())



