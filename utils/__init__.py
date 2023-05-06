from utils import registration # регистация (ввод имени, фамилии, е-мэйл, ввод города) + изменение города из меню
from utils import menu # стартовая бота и главное меню всех состояний
from utils import time_slot # ввод ТаймСлота, Календарь выбора даты, Все часы выбора
from utils import statistics #  вывод статистики, выбор роли HR и Candidate
from utils import english_level # начало выбора уровня языка и уровни
from utils import instruction # пункт инструкции
from utils import sending_messages # отправка в моменте сообщений всем пользователям и всем пользователям кто не ввел уровень языка 
from utils import simple_calendar # описание клавиатуры каллендаря используемой при вводе ТаймСлота
from utils import restart_active_jobs # рестарт активных мэтчей пользователей
from utils import other_time_slots # предоставление списка чужих ТС, приминение чужого ТС как своего, начало ввода роли для статистики при удачной встрече, реакция на несостоявшуюся встречу, отмена встречи
from utils import connect # мэтчинг встречь
from utils import intention_meet  # подтверждение намерения встретиться за 1 час до мита (Да, Нет, не знаю(если не ответил на вопрос)), обработка результатов за 30 минут до мита и автоматическая отмена встречи при НЕТ в ответах пользователей