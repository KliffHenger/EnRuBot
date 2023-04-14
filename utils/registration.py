from aiogram import types, Dispatcher
from user_states import Reg
from aiogram.dispatcher import FSMContext
from airtable_config import table, table_view
from utils.menu import menu
from keyboards.inline_menu import START
from config import bot, dp
import re
import geopy
from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz


async def bot_register(message: types.Message):
    msg_id = (await bot.send_message(message.from_user.id,
        f"Please share your email to sign up:")).message_id
    print(msg_id)
    await Reg.user_email.set()

@dp.callback_query_handler(text='register')
async def bot_register(message: types.Message):
    msg_id = (await bot.send_message(message.from_user.id,
        f"Please share your email to sign up:")).message_id
    print(msg_id)
    await bot.delete_message(message.from_user.id, msg_id-1)
    await Reg.user_email.set()

async def set_user_email(message: types.Message, state=FSMContext):
    """
    Валидация почты работает. Если tg_id пользователя
    есть в базе - пропустит дальше. Если нет - попросит почту.
    Если почта есть в базе, то значение tg_id будет обновлено, а бот
    пустит пользователя дальше.
    """
    pattern = r'^([a-zA-Z0-9_-]+\.)*[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)*\.[a-zA-Z]{2,3}$'
    is_found = False
    if re.fullmatch(pattern, message.text):
        is_found = False
        await state.update_data(user_email=message.text)
        find_table = table.all()
        view_table = table_view.all()
        for index in range(len(view_table)):
            if view_table[index]['fields']['UserEmail'] == message.text:
                is_found = True
                # wrong_date = None
                wrong_status = False
                # element_id = find_table[index]['id']
                msg_id = (await bot.send_message(message.from_user.id,
                    f"Welcome, {view_table[index]['fields']['UserName']} {view_table[index]['fields']['UserSurname']}")).message_id
                print(msg_id)
                table.create({'UserName': str(view_table[index]['fields']['UserName']), 
                    'UserSurname': str(view_table[index]['fields']['UserSurname']),
                    'UserEmail': str(view_table[index]['fields']['UserEmail']),
                    'UserIDTG': str(message.from_user.id),
                    'UserEngLevel': 'None',
                    'UserHourGoal': '4',
                    'LeaveMeeting': '0',    # для отслеживания случаев слива с мита
                    'ServerTimeSlot': 'None',
                    'UserDateSlot': 'None',
                    'UserTimeSlot': 'None',
                    'UTC': 'None',
                    'IsPared': 'False',
                    'NoActive': 'False',
                    'LastFindPeer': 'None',
                    'IsParedID': 'None',
                    'JobName': 'None',
                    'msgIDforDEL': 'None',
                    'UserStatistics': str({"A0":{"HR":0,"Candidate":0,},"A0-A1":{"HR":0,"Candidate":0,},"A1":{"HR":0,"Candidate":0,},"A1-A2":{"HR":0,"Candidate":0,},"A2":{"HR":0,"Candidate":0,},"A2-B1":{"HR":0,"Candidate":0,},"B1":{"HR":0,"Candidate":0,},"B1-B2":{"HR":0,"Candidate":0,},"B2":{"HR":0,"Candidate":0,},"B2-C1":{"HR":0,"Candidate":0,},"C1":{"HR":0,"Candidate":0,},"C1-C2":{"HR":0,"Candidate":0,},"C2":{"HR":0,"Candidate":0,}})})
                # table.update(record_id=str(element_id), fields={"UserIDTG": str(message.from_user.id)})
                # table.update(record_id=str(element_id), fields={"UserEngLevel": str(wrong_date)})
                # table.update(record_id=str(element_id), fields={"UserTimeSlot": str(wrong_date)})
                # table.update(record_id=str(element_id), fields={"IsPared": str(wrong_status)})
                await bot.send_message(message.from_user.id, f"Введите ваш город:")
                await Reg.user_utc.set()

        if not is_found:
            msg_id = (await bot.send_message(message.from_user.id,
                "We didn't find you in the student database. Please contact the school to find out more.", reply_markup=START)).message_id
            print(msg_id)
            # await message.delete()
            await bot.delete_message(message.from_user.id, msg_id-2)
            await state.finish()
    else:
        msg_id = (await bot.send_message(message.from_user.id,
            text='Please enter the valid email address:')).message_id
        print(msg_id)
        # await message.delete()
        await bot.delete_message(message.from_user.id, msg_id-2)


@dp.callback_query_handler(text='set_city')
async def bot_register(message: types.Message):
    msg_id = (await bot.send_message(message.from_user.id,
        f"Введите ваш город:")).message_id
    print(msg_id)
    await Reg.user_utc.set()


async def set_user_utc(message: types.Message, state=FSMContext):
    await state.update_data(user_utc=message.text)
    user_city = message.text
    geo = geopy.geocoders.Nominatim(user_agent="SuperMon_Bot")
    location = geo.geocode(user_city) # преобразуе 
    # print(location.latitude,location.longitude)
    find_table = table.all()
    if location is None:
        await bot.send_message(message.from_user.id, 
                        f"Не удалось найти такой город. Попробуйте написать его название латиницей или указать более крупный город поблизости.")
    else:  
        tf = TimezoneFinder()
        tz_user = tf.timezone_at(lng=location.longitude, lat=location.latitude)
        print(tz_user)
        tzUser = pytz.timezone(tz_user)
        user_time = datetime.now(tzUser)
        user_utc = user_time.strftime("%z")
        utc_f_msg = str(user_utc[0]+user_utc[1]+user_utc[2]+':'+user_utc[3]+user_utc[4])
        await bot.send_message(message.from_user.id,f"Часовой пояс установлен в {user_city} ({tz_user} / UTC{utc_f_msg}).")
        for index in range(len(find_table)):
            if find_table[index]['fields']['UserIDTG'] == str(message.from_user.id):
                element_id = find_table[index]['id']
                table.update(record_id=str(element_id), fields={"UTC": str(user_utc)})
                await state.finish()
                await menu(message)
        
    

def register_handlers_registration(dp: Dispatcher):
    dp.register_message_handler(bot_register, commands=['register'])
    dp.register_message_handler(set_user_email, state=Reg.user_email)
    dp.register_message_handler(set_user_utc, state=Reg.user_utc)
