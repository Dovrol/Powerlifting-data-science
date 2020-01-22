import pandas as pd
import numpy as np

pd.set_option('max_columns', None)
types = {
    'Name': np.str,
    'Sex': np.str,
    'Event':np.str,
    'Equipment': np.str,
    'Age': np.float64,
    'Division': np.str,
    'BodyweightKg': np.float64,
    'WeightClassKg': np.str,
    'Best3SquatKg' : np.float64,
    'Best3BenchKg' : np.float64,
    'Best3DeadliftKg' : np.float64,
    'TotalKg': np.float64,
    'Wilks': np.float64,
    'Federation' : np.str,
    'Tested': np.str,
    'MeetName' :np.str,
    'MeetCountry': np.str
    
}
cols = ['Name', 'Sex', 'Event', 'Equipment', 'Age', 'Division', 'BodyweightKg', 'WeightClassKg', 'Squat1Kg', 'Squat2Kg', 
        'Squat3Kg', 'Best3SquatKg', 'Bench1Kg', 'Bench2Kg', 'Bench3Kg', 'Best3BenchKg', 'Deadlift1Kg', 'Deadlift2Kg', 'Deadlift3Kg',
        'Best3DeadliftKg', 'TotalKg', 'Wilks', 'Date', 'Federation', 'Tested', 'MeetName', 'MeetCountry']

# from sqlalchemy import create_engine
# engine = create_engine('postgresql://:@localhost:5432/open_powerlifting')

df = pd.read_csv('datasets/openpowerlifting.csv', usecols=cols, dtype=types)
# df = pd.read_sql('my_table_name', engine, index_col = 'index')
# print(df.head())

mean_weight = df.groupby(['WeightClassKg']).mean()['BodyweightKg']
def swap_body_weight(arg):
    try:
        if arg[-1] == '+':
            return mean_weight[arg]
        else:
            return arg
    except:
        return arg

def update_data(data):
    filtered_df = data.copy()

    # weight_categories = ['59', '66', '74', '83', '93', '105', '120']
    filtered_df['Tested'] = filtered_df['Tested'].map(lambda x: x if x == 'Yes' else 'No')
    filtered_df['WeightClassKg'] = filtered_df['WeightClassKg'].map(swap_body_weight)
    filtered_df['WeightClassKg'] = pd.to_numeric(filtered_df['WeightClassKg'])
    filtered_df['Date'] = pd.to_datetime(filtered_df['Date'], errors = 'coerce')
    filtered_df['Date'].dropna(inplace = True)
    return filtered_df

filtered_df = update_data(df)
years = filtered_df['Date'].dt.year.unique()
