import pandas as pd

cost_df = pd.read_csv('./data/cost-of-living.csv', header=0)

cost_df.sort_values(by=['country', 'city'], ascending=True, inplace=True)

cost_df.set_index('No.', inplace=True)
cost_df = cost_df.rename(columns={'x33': 'Gasoline (1 liter) (USD)', 'x48': 'Apartment (1 bedroom) in City Centre (USD)', 'x49': 'Apartment (1 bedroom) Outside of Centre (USD)', 'x50': 'Apartment (3 bedrooms) in City Centre (USD)', 'x51': 'Apartment (3 bedrooms) Outside of Centre (USD)'})
cost_df['Gasoline (1 liter) (USD)']

#------------------------average price per liter of gas in each country---------------------------
import numpy as np
import pycountry
import geopandas as gpd
import matplotlib.pyplot as plt

with_lat_long_file = "./data/data_with_lat_long.csv"
lat_long_df = pd.read_csv(with_lat_long_file, header=0, 
                      usecols=["latitude", "longitude", 'Gasoline (1 liter) (USD)','country', 'gas_price_per_gallon'])
#creates a new column averaging the gas price per country
lat_long_df['avg_gas_price_per_country'] = np.round(lat_long_df.groupby(['country'])[['gas_price_per_gallon']].transform(np.mean), decimals = 1)
#drop the duplicates to only present one country and its average price of gas
lat_long_df.drop_duplicates(ignore_index=True, subset=['country','avg_gas_price_per_country'], inplace=True)

def alpha3code(column):
    CODE=[]
    for country in column:
        try:
            code=pycountry.countries.get(name=country).alpha_3
           # .alpha_3 means 3-letter country code 
           # .alpha_2 means 2-letter country code
            CODE.append(code)
        except:
            CODE.append('None')
    return CODE
#make a country code column in my lat_long_df
lat_long_df['CODE']=alpha3code(lat_long_df.country)
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
#rename the 'name' column to 'country to merge with my data set
world.columns=['pop_est', 'continent', 'country', 'CODE', 'gdp_md_est', 'geometry']
#rename United States of America to United States to be consistent with original data file. The DRC is also missing but there is no data on the DRC in our data set.
def rename_countries(value):
    if value == "United States of America":
        return 'United States'
    else:
        return value
world['country'] = world['country'].map(rename_countries)
merged_df=pd.merge(world,lat_long_df,on='country')

merged_df.plot(column='avg_gas_price_per_country', scheme="quantiles", edgecolor="black",
           figsize=(17, 13.3),
           legend=True,cmap='OrRd')
plt.title('Average Gas Price Per Gallon in USD',fontsize=50)
plt.show()

#bar chart showing the countriest with the lowest gas price
lat_long_df[['country','avg_gas_price_per_country']].sort_values(by='avg_gas_price_per_country').head(10)
max_gas_price_dict = {
    'Country': ['Libya', 'Algeria', 'Egypt', 'Angola', 'Brunei', 'Kuwait', 'Nigeria', 'Kazakhstan', 'Turkmenistan', 'Iran'],
    'avg_price_per_country': [0.1, 1.1, 1.2, 1.2, 1.4, 1.4, 1.4, 1.5, 1.6, 1.7]
 }
min_prices = pd.DataFrame(max_gas_price_dict)
# library
# give your chart some style
plt.style.use('dark_background')
# # 1st arg is column for x-axis, 2nd arg is column for y-axis
plt.bar(min_prices['Country'], max_gas_price_dict['avg_price_per_country'])
#give the chart a title
plt.title("Countries with the lowest gas price")  
# label the x and y axes
plt.xlabel('Country')
plt.ylabel('Average Gas Price (USD)')
# show the chart
plt.show()
