from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage





# TOKEN_API = "5607570842:AAFP4WjVh2MyLOV8QBdqr_KROfJH_GoOTXY" # токен Даниила
# TOKEN_API = "5988049870:AAF9JgMZQjX3jL55y9p8RVE2UDVMqIBBN5k" # токен Николая (Kliff_test_bot)
TOKEN_API = "5496793163:AAEKopXCilPK6D2Ue3tUtVlMTSolQ_fUgek" # токен Николая (EnRUChat_bot)


bot = Bot(TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())


week_dict = {'MO':'Monday', 'TU':'Tuesday', 'WE':'Wednesday', 'TH':'Thursday', 'FR':'Friday', 'SA':'Saturday', 'SU':'Sunday'}
WEEKDAYS = ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')

