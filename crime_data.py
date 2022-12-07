import pandas as pd
import numpy as np

df = pd.read_csv('crimedata.csv')[['racepctblack',
                                   'racePctWhite',
                                   'racePctAsian',
                                   'racePctHisp',

                                   'medIncome',
                                   'PctBornSameState',

                                   'murdPerPop',
                                   'rapesPerPop',
                                   'robbbPerPop',
                                   'assaultPerPop',
                                   'burglPerPop',
                                   'larcPerPop',
                                   'autoTheftPerPop',
                                   'arsonsPerPop']].dropna()

df = df.rename(columns={'murdPerPop': 'murders',
                        'rapesPerPop': 'rapes',
                        'robbbPerPop': 'robberies',
                        'assaultPerPop': 'assaults',
                        'burglPerPop': 'burglaries',
                        'larcPerPop': 'larcenies',
                        'autoTheftPerPop': 'autoThefts',
                        'arsonsPerPop': 'arsons'})

df_race = df[['racepctblack',
              'racePctWhite',
              'racePctAsian',
              'racePctHisp',

              'murders',
              'rapes',
              'robberies',
              'assaults',
              'burglaries',
              'larcenies',
              'autoThefts',
              'arsons']]

df['pctIncome'] = df['medIncome'] / df['medIncome'].max() * 100
df_social = df[['pctIncome',
                'PctBornSameState',

                'murders',
                'rapes',
                'robberies',
                'assaults',
                'burglaries',
                'larcenies',
                'autoThefts',
                'arsons']]

arr_social = np.ndarray([10, 5, 8])
for i in range(arr_social.shape[0]):
    for j in range(arr_social.shape[1]):
        df_filt = df_social

        df_filt = df_filt[i * 10 <= df_filt['PctBornSameState']]
        df_filt = df_filt[df_filt['PctBornSameState'] <= (i + 1) * 10]

        df_filt = df_filt[j * 10 <= df_filt['pctIncome']]
        df_filt = df_filt[df_filt['pctIncome'] <= (j + 1) * 10]

        df_filt = df_filt[['murders',
                           'rapes',
                           'robberies',
                           'assaults',
                           'burglaries',
                           'larcenies',
                           'autoThefts',
                           'arsons']]

        arr_social[i][j] = df_filt.sum(axis=0).array
