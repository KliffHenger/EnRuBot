from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



BTN_Monday = InlineKeyboardButton(text='Monday', callback_data='MO')
BTN_Tuesday = InlineKeyboardButton(text='Tuesday', callback_data='TU')
BTN_Wednesday = InlineKeyboardButton(text='Wednesday', callback_data='WE')
BTN_Thursday = InlineKeyboardButton(text='Thursday', callback_data='TH')
BTN_Friday = InlineKeyboardButton(text='Friday', callback_data='FR')
BTN_Saturday = InlineKeyboardButton(text='Saturday', callback_data='SA')
BTN_Sunday = InlineKeyboardButton(text='Sunday', callback_data='SU')


WEEK = InlineKeyboardMarkup().row(
    BTN_Monday, BTN_Tuesday, BTN_Wednesday).row(
    BTN_Thursday, BTN_Friday, BTN_Saturday).row(BTN_Sunday)


BTN_00 = InlineKeyboardButton(text='00', callback_data='00')
BTN_01 = InlineKeyboardButton(text='01', callback_data='01')
BTN_02 = InlineKeyboardButton(text='02', callback_data='02')
BTN_03 = InlineKeyboardButton(text='03', callback_data='03')
BTN_04 = InlineKeyboardButton(text='04', callback_data='04')
BTN_05 = InlineKeyboardButton(text='05', callback_data='05')
BTN_06 = InlineKeyboardButton(text='06', callback_data='06')
BTN_07 = InlineKeyboardButton(text='07', callback_data='07')
BTN_08 = InlineKeyboardButton(text='08', callback_data='08')
BTN_09 = InlineKeyboardButton(text='09', callback_data='09')
BTN_10 = InlineKeyboardButton(text='10', callback_data='10')
BTN_11 = InlineKeyboardButton(text='11', callback_data='11')
BTN_12 = InlineKeyboardButton(text='12', callback_data='12')
BTN_13 = InlineKeyboardButton(text='13', callback_data='13')
BTN_14 = InlineKeyboardButton(text='14', callback_data='14')
BTN_15 = InlineKeyboardButton(text='15', callback_data='15')
BTN_16 = InlineKeyboardButton(text='16', callback_data='16')
BTN_17 = InlineKeyboardButton(text='17', callback_data='17')
BTN_18 = InlineKeyboardButton(text='18', callback_data='18')
BTN_19 = InlineKeyboardButton(text='19', callback_data='19')
BTN_20 = InlineKeyboardButton(text='20', callback_data='20')
BTN_21 = InlineKeyboardButton(text='21', callback_data='21')
BTN_22 = InlineKeyboardButton(text='22', callback_data='22')
BTN_23 = InlineKeyboardButton(text='23', callback_data='23')
BTN_Back = InlineKeyboardButton(text='Back', callback_data='timeslot')


HOUR = InlineKeyboardMarkup().row(
    BTN_00, BTN_01, BTN_02, BTN_03
).row(
    BTN_04, BTN_05, BTN_06, BTN_07
).row(
    BTN_08, BTN_09, BTN_10, BTN_11
).row(
    BTN_12, BTN_13, BTN_14, BTN_15
).row(
    BTN_16, BTN_17, BTN_18, BTN_19
).row(
    BTN_20, BTN_21, BTN_22, BTN_23
).row(
    BTN_Back
)
