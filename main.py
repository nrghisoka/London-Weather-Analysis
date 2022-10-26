# CREATED BY CONNOR WHISMAN
# STARTED ON 10/25/22
# DEMONSTRATION OF BASIC DATA ANALYSIS AND USE OF MYSQL

import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector as sql

dataset_name = 'Data/london_weather.csv'

def main():
    print('Reading ' + dataset_name + '..')
    data = pd.read_csv(dataset_name)
    print('Dataset size: ' + str(data.shape) + '\n')

    # CONVERT DATE COLUMN FROM STRING TO DATETIME FORMAT
    data['date'] = pd.to_datetime(data['date'], format='%Y%m%d')

    # ALL DATA CONTAINING MATCHING 'YEAR' INTO THEIR OWN GROUPS
    group_byyear = data.groupby(data['date'].dt.year)

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
    cursor.execute('CREATE TABLE IF NOT EXISTS ' + table_name + ' (date DATE, sunshine FLOAT(3,1), max_temp FLOAT(3,1), mean_temp FLOAT(3,1), min_temp FLOAT(3,1))')


    # LOOP THROUGH PANDAS DATAFRAME AND INSERT INTO TABLE
        # DROP ROWS OF DATAFRAME THAT CONTAIN NAN BECAUSE THEY CURRENTLY CAUSE ERRORS
    data = data.dropna()
        # ONLY INSERT IF TABLE IS EMPTY
    cursor.execute('SELECT * FROM ' + table_name)
    result = cursor.fetchall()
    if len(result) == 0:
        for id, row in data.iterrows():
            cursor.execute('INSERT INTO ' + table_name + ' (date, sunshine, max_temp, mean_temp, min_temp) values(%s, %s, %s, %s, %s)', (row.date, row.sunshine, row.max_temp, row.mean_temp, row.min_temp))
    
    # QUERY DATABASE FOR ALL ENTRIES
    cursor.execute('SELECT * FROM ' + table_name)
    result = cursor.fetchall()
    print(result)
    
    
    
    # NEXT STEP, CREATE MORE SPECIFIC QUERIES TO FIND SPECIFIC DATA:

    
    
if __name__ == '__main__':
    main()