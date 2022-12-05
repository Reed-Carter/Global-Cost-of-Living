import pandas as pd

cost_df = pd.read_csv('./data/cost-of-living.csv', header=0)

cost_df.sort_values(by=['country', 'city'], ascending=True, inplace=True)

cost_df.set_index('No.', inplace=True)
