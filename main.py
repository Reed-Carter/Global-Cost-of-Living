import pandas as pd

cost_df = pd.read_csv('./data/cost-of-living.csv', header=0)

cost_df.sort_values(by=['country', 'city'], ascending=True, inplace=True)

cost_df.set_index('No.', inplace=True)
cost_df = cost_df.rename(columns={'x33': 'Gasoline (1 liter) (USD)', 'x48': 'Apartment (1 bedroom) in City Centre (USD)', 'x49': 'Apartment (1 bedroom) Outside of Centre (USD)', 'x50': 'Apartment (3 bedrooms) in City Centre (USD)', 'x51': 'Apartment (3 bedrooms) Outside of Centre (USD)'})
cost_df['Gasoline (1 liter) (USD)']
