import pandas as pd
import numpy as np

# Data Preprocessing
clubstats = pd.read_csv('clubstats.csv')
tables = pd.read_csv('tables.csv')

# Change to proper data types
clubstats['cross_accuracy'] = clubstats['cross_accuracy'].map(lambda x: x.rstrip('%')).astype('int')
clubstats['pass_accuracy'] = clubstats['pass_accuracy'].map(lambda x: x.rstrip('%')).astype('int')
clubstats['shooting_accuracy'] = clubstats['shooting_accuracy'].map(lambda x: x.rstrip('%')).astype('int')
clubstats['tackle_success'] = clubstats['tackle_success'].map(lambda x: x.rstrip('%')).astype('int')
clubstats['aerial_battles'] = clubstats['aerial_battles'].str.replace(',','').astype('int')
clubstats['clearance'] = clubstats['clearance'].str.replace(',','').astype('int')
clubstats['cross'] = clubstats['cross'].str.replace(',','').astype('int')

# In 'clubstats' AFC Bournemouth is named as it is, but in 'tables' it is named as 'Bournemouth'.
# So in order to join the two data frames, the club_name for AFC Bournmouth has to be changed.
clubstats['club_name'].iloc[53] = 'Bournemouth'
clubstats['club_name'].iloc[54] = 'Bournemouth'
clubstats['club_name'].iloc[55] = 'Bournemouth'
clubstats['club_name'].iloc[56] = 'Bournemouth'
clubstats['club_name'].iloc[57] = 'Bournemouth'

season_info = clubstats[clubstats['club_name'] == "Arsenal"].loc[:,'season']
seasons = []

for i in range(len(season_info)):
    if i < 25:
        seasons.append([season_info[i],] * 20)
    else:
        seasons.append([season_info[i],] * 22)

seasons_flat = [season for sub_season in seasons for season in sub_season]
tables['season'] = seasons_flat

# Join two data frames
data = pd.merge(tables, clubstats, on=['club_name', 'season'])

# To get total number of games
data['total_games'] = data['won'] + data['drawn'] + data['lost']
# Add top4 indicator 
data['is_top4'] = data['position'].apply(lambda x: 1 if (x <= 4) else 0)
# Change to Datetime
data['season'] = pd.to_datetime(data['season'],format='%Y/%y')

# numpy datetime and pandas datetime conflict each other
# create a new dataframe for displaying table
df = data.copy()

for i in range(len(df)):
    df['season'].iloc[i] = df['season'].iloc[i].year

# Seperate into two groups
top4 = data[data['is_top4'] == 1]
below4  = data[data['is_top4'] == 0]

# Save preprocessed dataset
clubstats.to_csv('p_clubstats.csv')
tables.to_csv('p_tables.csv')
top4.to_csv('top4.csv')
below4.to_csv('below4.csv')
df.to_csv('df.csv')