# CREATED BY CONNOR WHISMAN
# STARTED ON 10/25/22
# DEMONSTRATION OF BASIC DATA ANALYSIS AND USE OF MYSQL

import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector as sql

dataset_name = 'Data/london_weather.csv'

def main():
    print(f'Reading {dataset_name}..')
    dataset = pd.read_csv(dataset_name)
    print('Dataset size: ' + str(dataset.shape) + '\n')

    # CONVERT DATE COLUMN FROM STRING TO DATETIME FORMAT
    dataset['date'] = pd.to_datetime(dataset['date'], format='%Y%m%d')

    # ALL DATA CONTAINING MATCHING 'YEAR' INTO THEIR OWN GROUPS
    group_byyear = dataset.groupby(dataset['date'].dt.year)

    # FOR EVERY YEAR GROUP:
    # - FIND MEAN OF 'SUNSHINE'
    yearlymean_mintemp = group_byyear['min_temp'].mean()
    # - FIND MEAN OF 'MAX_TEMP'
    yearlymean_meantemp = group_byyear['mean_temp'].mean()
    # - FIND MAX OF 'MAX_TEMP'
    yearlymean_maxtemp = group_byyear['max_temp'].mean()

    #  PLOT ONTO LINE GRAPH
    # yearlymean_mintemp.plot()
    # plt.show()
    # yearlymean_meantemp.plot()
    # plt.show()
    # yearlymean_maxtemp.plot()
    # plt.show()

    # CONCLUSION 1:
    # ANALYSIS ON TEMPERATURE DATA SHOWS AVERAGE TEMPERATURES RISING OVER TIME IN LONDON

# ---------------------------------------------------------------------------------------------

    # ONTO ADDING MYSQL FUNCTIONALITY:
    db_name = 'test_database'
    table_name = 'london_weather'

    # # CONNECT TO CREATE DATABASE
    # db = sql.connect(
    #     host = 'localhost',
    #     user = 'root',
    #     password = 'CONnor0116'
    # )

    # # CURSOR DOES ALL OF THE CONTROLLING
    # cursor = db.cursor()

    # # CREATE DATABASE (ONLY IF IT HASN'T ALREADY BEEN CREATED)
    # cursor.execute('CREATE DATABASE IF NOT EXISTS ' + db_name)

    # RE-CONNECT TO CREATED DATABASE
    db = sql.connect(
        host = 'localhost',
        user = 'root',
        password = 'CONnor0116',
        database = db_name
    )
    cursor = db.cursor()

    # CREATE TABLE FOR LONDON WEATHER DATA IN ORDER TO MOVE DATASET TO THE DATABASE
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (date DATE, sunshine FLOAT(3,1), max_temp FLOAT(3,1), mean_temp FLOAT(3,1), min_temp FLOAT(3,1))')


# ------ ADD DATA TO DATABASE IF IT HASN'T BEEN SAVED YET ------
    # LOOP THROUGH PANDAS DATAFRAME AND INSERT INTO TABLE
        # DROP ROWS OF DATAFRAME THAT CONTAIN NAN BECAUSE THEY CURRENTLY CAUSE ERRORS
    dataset = dataset.dropna()
        # ONLY INSERT IF TABLE IS EMPTY
    cursor.execute(f'SELECT * FROM {table_name} LIMIT 1')
    result = cursor.fetchall()
    if len(result) == 0:
        for id, row in dataset.iterrows():
            values = (row.date, row.sunshine, row.max_temp, row.mean_temp, row.min_temp)
            cursor.execute(f'INSERT INTO {table_name} (date, sunshine, max_temp, mean_temp, min_temp) VALUES (%s, %s, %s, %s, %s)', values)
        db.commit()

    # QUERY DATABASE FOR ALL ENTRIES TO VERIFY DATA HAS BEEN SAVED
    # cursor.execute('SELECT * FROM ' + table_name)
    # result = cursor.fetchall()
    # print(cursor.rowcount)
    # print(result)
    
# ------ DATA IS NOW SAVED ------
# NEXT STEP, CREATE MORE SPECIFIC QUERIES TO FIND SPECIFIC DATA:

# 1. WHAT IS THE PERCENTAGE OF DAYS WHERE THE TEMPERATURE WAS 20 DEGREES CELCIUS OR ABOVE, FOR EACH YEAR?:
    cursor.execute(f'SELECT date, max_temp FROM {table_name} WHERE max_temp >= 20')
    query1 = cursor.fetchall()
    # DICT TO SAVE EACH YEAR WITH THE NUMBER OF DAYS
    count_results = {}
    # LOOP QUERY AND MANUALLY COUNT NUMBER OF DAYS IN EACH
    start = 1979
    while start < 2020:
        count = 0
        for i in query1:
            year = i[0].year
            if start == year:
                count += 1
        # ADD RESULT TO DICT AND INCREMENT TO RE-LOOP
        count_results[start] = count
        start += 1
    # FIND PERCENTAGES OF EACH RESULT (MAXIMUM OF 2 DECIMAL PLACES)
    percent_results = {}
    for key in count_results:
        value = count_results[key]
        percent = (value / 365) * 100
        percent_results[key] = float(str(percent)[0:3])
    # FINAL RESULT
    for key in percent_results:
        print(f'{key}: {percent_results[key]}%')

    # CREATE NEW TABLE TO STORE FINDINGS
    new_table = 'percent_warm_days_yearly'
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {new_table} (year INT, percent CHAR(6))')
    if not cursor.fetchall():
        for key in percent_results:
            values = (key, str(percent_results[key]))
            cursor.execute(f'INSERT INTO {new_table} (year, percent) VALUES (%s, %s)', values)
        db.commit()
    # QUERY NEW TABLE
    cursor.execute(f'SELECT * FROM {new_table}')
    print(cursor.fetchall())



    
if __name__ == '__main__':
    main()