import pandas as pd
import numpy as np


def replace_pct_to_num_column(df, pct_column_name, num_column_name, scale_factor_column_name):
    df[num_column_name] = (df[pct_column_name] / 100) * \
        df[scale_factor_column_name]
    df.drop([pct_column_name], axis=1, inplace=True)


def replace_num_to_pct_column(df, num_column_name, pct_column_name, scale_factor_column_name):
    df[pct_column_name] = df[num_column_name] / \
        df[scale_factor_column_name] * 100
    df.drop([num_column_name], axis=1, inplace=True)


df = pd.read_csv('crimedata.csv')[['state',
                                   'communityName',
                                   'population',

                                   'racepctblack',
                                   'racePctWhite',
                                   'racePctAsian',
                                   'racePctHisp',

                                   'medIncome',
                                   'NumUnderPov',
                                   'PctUnemployed',
                                   'PctNotHSGrad',

                                   'murders',
                                   'rapes',
                                   'robberies',
                                   'assaults',
                                   'burglaries',
                                   'larcenies',
                                   'autoTheft',
                                   'arsons']].dropna()

replace_pct_to_num_column(df, 'racepctblack', 'num_black', 'population')
replace_pct_to_num_column(df, 'racePctWhite', 'num_white', 'population')
replace_pct_to_num_column(df, 'racePctAsian', 'num_asian', 'population')
replace_pct_to_num_column(df, 'racePctHisp', 'num_hisp', 'population')

replace_pct_to_num_column(df, 'PctUnemployed', 'num_unemployed', 'population')
replace_pct_to_num_column(df, 'PctNotHSGrad', 'num_uneducated', 'population')

df.rename(columns={'communityName': 'community',
                   'medIncome': 'med_income',
                   'NumUnderPov': 'num_underpov',
                   'autoTheft': 'auto_thefts'}, inplace=True)


df = df.groupby(['state', 'community']).agg({'population': 'sum',

                                             'num_black': 'sum',
                                             'num_white': 'sum',
                                             'num_asian': 'sum',
                                             'num_hisp': 'sum',

                                             'num_underpov': 'sum',
                                             'num_unemployed': 'sum',
                                             'num_uneducated': 'sum',
                                             'med_income': 'mean',

                                             'murders': 'sum',
                                             'rapes': 'sum',
                                             'robberies': 'sum',
                                             'assaults': 'sum',
                                             'burglaries': 'sum',
                                             'larcenies': 'sum',
                                             'auto_thefts': 'sum',
                                             'arsons': 'sum'}).reset_index()

replace_num_to_pct_column(df, 'num_black', 'pct_black', 'population')
replace_num_to_pct_column(df, 'num_white', 'pct_white', 'population')
replace_num_to_pct_column(df, 'num_asian', 'pct_asian', 'population')
replace_num_to_pct_column(df, 'num_hisp', 'pct_hisp', 'population')

replace_num_to_pct_column(df, 'num_unemployed', 'pct_unemployed', 'population')
replace_num_to_pct_column(df, 'num_uneducated', 'pct_uneducated', 'population')
replace_num_to_pct_column(df, 'num_underpov', 'pct_underpov', 'population')
df['pct_income'] = df['med_income'] / df['med_income'].max() * 100


df_social_status_crimes_relation = df[['pct_uneducated',
                                       'pct_underpov',
                                       'pct_income',

                                       'murders',
                                       'rapes',
                                       'robberies',
                                       'assaults',
                                       'burglaries',
                                       'larcenies',
                                       'auto_thefts',
                                       'arsons']]

array_sscr = np.ndarray([10, 10, 8])
for i in range(array_sscr.shape[0]):
    for j in range(array_sscr.shape[1]):
        df_sscr = df_social_status_crimes_relation
        df_sscr = df_sscr[df_sscr['pct_uneducated'] <= (i + 1) * 5]
        df_sscr = df_sscr[df_sscr['pct_uneducated'] >= i * 5]
        df_sscr = df_sscr[df_sscr['pct_income'] <= (j + 1) * 5]
        df_sscr = df_sscr[df_sscr['pct_income'] >= j * 5]
        df_sscr = df_sscr[['murders',
                           'rapes',
                           'robberies',
                           'assaults',
                           'burglaries',
                           'larcenies',
                           'auto_thefts',
                           'arsons']]
        df_sscr = df_sscr.sum(axis=0)
        array_sscr[i][j] = df_sscr.array
