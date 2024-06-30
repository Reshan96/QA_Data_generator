import datetime
from test_data_generator import generate_test_data

# Example usage
column_names = ['DATE_INSERTED', 'SESSIONID', 'SPECIFICATION']
column_types = ['timestamp(6) with time zone',  'string', 'string']
num_rows = 100
num_files = 1
base_filename = 'test_data_new' 
json_dir_name = 'JSON_File_List_Extractable'
start_date = datetime.datetime(2022,1,10,23,0,0)
end_date = datetime.datetime(2022,1,11,0,0,0)
time_zone = '+05:30'

for i in range(num_files):
        output_file = f"{base_filename}_{i+1}.csv"
        generate_test_data(column_names=column_names,
                           column_types=column_types,
                           num_rows=num_rows,
                           start_date= start_date,
                           end_date=end_date,
                           time_zone= time_zone,
                           json_dir_name= json_dir_name,
                           output_file=output_file)
        print(f"Generated {num_rows} rows of test data and saved it to {output_file}")


