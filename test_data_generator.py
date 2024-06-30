import csv
import random
from faker import Faker
import datetime
import uuid
import glob
import sys
import string

from Test_functions.Json_reader import get_json_value

def generate_test_data(column_names, column_types, num_rows, start_date, end_date, time_zone, json_dir_name, output_file):
    # Create an instance of the Faker generator
    fake = Faker('no_NO')  # Set locale to Norwegian
    
    # Open the output CSV file in write mode
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Write the column names as the first row
        writer.writerow(column_names)
        
        # Generate data for each row
        for row_num in range(num_rows):
            row = []
            json_file = ''
            # Generate random data for each column
            for column_name, data_type in zip(column_names, column_types):
                if data_type == 'integer':
                    value = random.randint(1, 100)
                elif data_type == 'float':
                    value = random.uniform(1.0, 100.0)
                elif data_type == 'string':
                    # Generate meaningful data based on column name
                    if 'name' in column_name.lower():
                        value = fake.name()
                    elif 'address' in column_name.lower():
                        value = fake.address().replace('\n', ', ')
                    elif 'specification' in column_name.lower():
                        value = 'DSTU2'
                    elif 'auditevent' in column_name.lower():
                        value, file_name = select_random_json(json_dir_name)
                        json_file = file_name
                    elif 'source_identifier_value' in column_name.lower():
                        value =  get_json_value(json_dir_name, json_file)
                    elif 'id' in column_name.lower():
                        value = str(uuid.uuid4().hex)
                    else:
                        value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=10))
                elif data_type == 'boolean':
                    value = random.choice([True, False])
                elif data_type == 'date':
                    #value = fake.date_between(start_date=datetime.date(2022,1,1), end_date='today').strftime('%m/%d/%Y')
                    value = fake.date_between(start_date=start_date, end_date=end_date).strftime('%d/%m/%Y %H:%M:%S')
                elif data_type == 'datetime_with_timezone':
                    date_inserted = fake.date_between(start_date=start_date, end_date=end_date)
                    value = date_inserted.strftime('%m/%d/%Y %H:%M:%S %z')
                elif data_type == 'raw':
                    value = generate_raw_data()
                elif data_type == 'timestamp(6) with time zone':
                    value = generate_timestamp(fake, start_date, end_date, time_zone)
                else:
                    # Add more data type checks if needed
                    value = None
                row.append(value)
            
            # Write the generated row to the CSV file
            writer.writerow(row)
            
            # Calculate progress percentage
            progress = (row_num + 1) / num_rows * 100
            sys.stdout.write(f"\rGenerating data: {row_num+1}/{num_rows} ({progress:.2f}%)")
            sys.stdout.flush()
    
    #print(f"\nGenerated {num_rows} rows of test data and saved it to {output_file}.")

def select_random_json(json_dir_name):
    # Define the directory path where the JSON files are located
    json_directory = json_dir_name
    
    # Get the list of JSON files in the directory
    json_files = glob.glob(f"{json_directory}/*.json")
    
    # Randomly select a JSON file from the list
    random_json_file = random.choice(json_files)
    
    # Read the content of the selected JSON file
    with open(random_json_file, 'r') as file:
        json_content = file.read()
    
    return json_content, random_json_file

def generate_raw_data():
    # Generate a GUID with only literal and numeric characters
    guid = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
    return guid.upper()

def generate_timestamp(fake, start_date, end_date, time_zone):

    # Generate a random date within the range
    random_date = fake.date_time_between(start_date=start_date, end_date=end_date)
    
    # Extract date components
    random_year = random_date.year
    random_month = random_date.month
    random_day = random_date.day
    
    min_hour = start_date.hour
    max_hour = end_date.hour

    if (random_day == start_date.day) & (start_date.date() == end_date.date()):
        max_hour = end_date.hour
    elif (random_day == start_date.day) & (end_date.date() > start_date.date()):
        max_hour = 23
    elif (random_date.date() < end_date.date()):
        min_hour = 0
        max_hour = 23
    else:
        min_hour = 0
        max_hour = end_date.hour-1

    # Generate random time within the range of the generated date
    random_time = datetime.time(fake.random_int(min=min_hour, max=(max_hour)),
                                fake.random_int(min=0, max=59),
                                fake.random_int(min=0, max=59),
                                fake.random_int(min=0, max=999999))
    #print(random_time)

    # Combine date and time
    timestamp = datetime.datetime(random_year, random_month, random_day, random_time.hour, random_time.minute, random_time.second, random_time.microsecond).strftime('%d-%b-%y %I.%M.%S.%f %p')

    # Combine timestamp with timezone
    timestamp_with_timezone = f"{timestamp} {time_zone}"

    return timestamp_with_timezone

