from pyairtable import Table, Api


api_key = 'key64C9CvHlRvTZnd'
base_id = 'app5Z5KfDBdcGv3eg'
table_name = 'tblyHxtR3Se0M0hId' # Test
# table_name = 'tblTjjGzhD8UAMjNP' # Prod
table_name2 = 'tblHUyth3sBhAsQ8a' # Это таблица Формы регистрации с сайта
table_msg = 'tblWOK5v6wvnzHHoN' # Это таблица с Текстами для рассылки


table = Table(api_key, base_id, table_name)
table_view = Table(api_key, base_id, table_name2)
msg_table = Table(api_key, base_id, table_msg)

