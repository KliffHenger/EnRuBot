from pyairtable import Table, Api


api_key = 'key64C9CvHlRvTZnd'
base_id = 'app5Z5KfDBdcGv3eg'
table_name = 'tblyHxtR3Se0M0hId'
table_name2 = 'tblHUyth3sBhAsQ8a'


table = Table(api_key, base_id, table_name)
table_view = Table(api_key, base_id, table_name2)

