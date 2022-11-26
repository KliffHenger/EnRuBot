from pyairtable import Table
from airtable import airtable
import os


# api_key = os.getenv('AIRTABLE_API_KEY')
api_key = 'keypdxX6KYuSbLmWB'
base_id = 'appq6pQqHPLUZGcPb'
table_name = 'test_table' 
table = Table(api_key, base_id, table_name)


at = airtable.Airtable(base_id="appq6pQqHPLUZGcPb", api_key="keypdxX6KYuSbLmWB")
# print(at.get('test_table'))
# at.update('test_table', 'recnJ5e6r3g2xhDeK', {'UserEngLevel': "B2"})



