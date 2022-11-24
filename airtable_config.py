from pyairtable import Table
from airtable import airtable
import requests
import os


api_key = os.getenv('AIRTABLE_API_KEY')
base_id = 'appq6pQqHPLUZGcPb'
table_name = 'test_table' 
table = Table(api_key, base_id, table_name, timeout=(5,5))
find_table = table.all()


at = airtable.Airtable(base_id="appq6pQqHPLUZGcPb", api_key="keypdxX6KYuSbLmWB")
# print(at.get('test_table'))
# at.update('test_table', 'recnJ5e6r3g2xhDeK', {'UserEngLevel': "B2"})



