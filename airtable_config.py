from pyairtable import Table


api_key = "keypdxX6KYuSbLmWB"
table = Table(api_key, 'appq6pQqHPLUZGcPb', 'test_table')
find_table = table.all()
# print(find_table[2]['fields']['UserIDTG'])



