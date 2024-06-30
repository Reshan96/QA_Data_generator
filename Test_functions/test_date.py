from faker import Faker
import datetime

fake = Faker()

def generate_timestamp(fake, start_date, end_date, time_zone):
    # Generate a random date within the range
    random_date = fake.date_time_between(start_date=start_date, end_date=end_date)

    # Extract date components
    year = random_date.year
    month = random_date.month
    day = random_date.day

    # Generate random time within the range of the generated date
    random_time = datetime.time(fake.random_int(min=start_date.hour, max=(end_date.hour-1)),
                                fake.random_int(min=0, max=59),
                                fake.random_int(min=0, max=59))

    # Combine date and time
    timestamp = datetime.datetime(year, month, day, random_time.hour, random_time.minute, random_time.second, random_time.microsecond).strftime('%d-%b-%y %I.%M.%S.%f %p')

    # Combine timestamp with timezone
    timestamp_with_timezone = f"{timestamp} {time_zone}"

    return timestamp_with_timezone

# Test the function
start_date = datetime.datetime(2022, 1, 1, 13, 0, 0)
end_date = datetime.datetime(2022, 1, 31, 15, 0, 0)
time_zone = '+02:00'

print(generate_timestamp(fake, start_date, end_date, time_zone))
