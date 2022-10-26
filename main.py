import pandas as pd
import matplotlib.pyplot as plt

dataset_name = 'Data/london_weather.csv'

def main():
    print('Reading ' + dataset_name + '..')
    data = pd.read_csv(dataset_name)
    print('Dataset size: ' + str(data.shape))

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
    yearlymean_mintemp.plot()
    plt.show()
    yearlymean_meantemp.plot()
    plt.show()
    yearlymean_maxtemp.plot()
    plt.show()

    # CONCLUSION 1:
    # ANALYSIS ON TEMPERATURE DATA SHOWS AVERAGE TEMPERATURES RISING OVER TIME IN LONDON


if __name__ == '__main__':
    main()