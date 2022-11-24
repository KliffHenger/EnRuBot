from pyairtable import Table
from airtable import airtable


api_key = "keypdxX6KYuSbLmWB"
table = Table(api_key, 'appq6pQqHPLUZGcPb', 'test_table')
find_table = table.all()


at = airtable.Airtable(base_id="appq6pQqHPLUZGcPb", api_key="keypdxX6KYuSbLmWB")
# print(at.get('test_table'))
# at.update('test_table', 'recnJ5e6r3g2xhDeK', {'UserEngLevel': "B2"})



