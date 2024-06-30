import csv
import cx_Oracle

# Oracle connection details
username = "suystem"
password = "oracle"
dsn = "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=10.16.1.91)(PORT=1521))(CONNECT_DATA=(SERVER=DEDICATED)(SERVICE_NAME=dips)))"

# Open CSV file and connect to Oracle
with open('test_data_6_TEST.csv', newline='', encoding='utf-8') as csvfile, cx_Oracle.connect(username, password, dsn) as conn:
    reader = csv.reader(csvfile, delimiter=',')
    next(reader)  # Skip header row if present

    # Prepare the INSERT statement
    insert_sql = "INSERT INTO AUDIT_DATA.ADAUDITEVENT_V3 (DATE_INSERTED, SESSIONID, PARTITIONING_DATE, AUDITEVENT, SPECIFICATION) " \
                 "VALUES (TO_TIMESTAMP_TZ(:1, 'DD/MM/YYYY HH24:MI:SS'), :2, TO_DATE(:3, 'DD/MM/YYYY'), :4, :5)"

    # Execute the INSERT statement for each row in the CSV
    cursor = conn.cursor()
    for row in reader:
        cursor.execute(insert_sql, row)

    # Commit the changes
    conn.commit()

    # Close the cursor and connection
    cursor.close()

print("Data inserted successfully.")
