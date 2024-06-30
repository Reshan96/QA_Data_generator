import cx_Oracle
import csv

def import_data_into_table(csv_file, table_name, connection_string):
    # Establish a connection to the Oracle database
    connection = cx_Oracle.connect(connection_string)

    # Create a cursor object to execute SQL statements
    cursor = connection.cursor()

    try:
        # Truncate the table to remove existing data
        cursor.execute(f"TRUNCATE TABLE {table_name}")

        # Open the CSV file for reading
        with open(csv_file, 'r') as file:
            # Create a CSV reader object
            csv_reader = csv.reader(file)

            # Iterate over each row in the CSV file
            for row in csv_reader:
                # Construct the SQL INSERT statement
                insert_statement = f"INSERT INTO {table_name} VALUES ({','.join([':{}'.format(i+1) for i in range(len(row))])})"

                # Execute the SQL INSERT statement with the current row values
                cursor.execute(insert_statement, row)

        # Commit the transaction to persist the changes
        connection.commit()
        print("Data imported successfully.")

    except cx_Oracle.DatabaseError as e:
        # Rollback the transaction in case of any error
        connection.rollback()
        print("Error occurred during data import:", e)

    finally:
        # Close the cursor and connection
        cursor.close()
        connection.close()

# Example usage
csv_file = 'test_data_JAN.csv'
table_name = 'AUDIT_DATA.adauditevent_v3'
connection_string = 'system/oracle@10.16.1.91/dips'

import_data_into_table(csv_file, table_name, connection_string)
