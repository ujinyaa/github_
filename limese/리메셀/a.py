import pandas as pd
import numpy as np
file_path = "C:\\Users\\LYJ\\Desktop\\CODE_HOME\\리메셀\\india geospatial\\cities_r2.csv"
data = pd.read_csv(file_path)
data.head()
data.describe()
data['lattitude'] = data['location'].apply(lambda x: x.split(',')[0])
data['longitude'] = data['location'].apply(lambda x: x.split(',')[1])
data.head(5)
top_pop_cities = data.sort_values(by='population_total',ascending=False)
top20_populated_cities=top_pop_cities.head(20)
top20_populated_cities


longitude = np.array(top20_populated_cities['longitude'])
lattitude = np.array(top20_populated_cities['lattitude'])
total_population = np.array(top20_populated_cities['population_total'])
city_name = np.array(top20_populated_cities['name_of_city'])

x, y = map(longitude, lattitude)
population_sizes = top20_populated_cities["population_total"].apply(lambda x: int(x / 5000))
plt.scatter(x, y, s=population_sizes, marker="o", c=population_sizes, cmap=cm.Dark2, alpha=0.8)

for ncs, xpt, ypt in zip(city_name, x, y):
    plt.text(xpt + 6000, ypt + 3000, ncs, fontsize=10, fontweight='bold')

plt.title('Top 20 Populated Cities in India', fontsize=20)





from IPython.display import display

top20_female = data.nlargest(20, 'sex_ratio')[['name_of_city','population_total', 'population_female','sex_ratio']]
display(top20_female)
data['longitude_female'] = data['location'].apply(lambda x: x.split(',')[0])
data['lattitude_female'] = data['location'].apply(lambda x: x.split(',')[1])
data.head(5)



longitude_female = np.array(top20_female['longitude'])
lattitude_female = np.array(top20_female['lattitude'])
female_population = np.array(top20_female['population_total'])
city_name_female = np.array(top20_female['name_of_city'])

x_female, y_female = map(longitude_female, lattitude_female)
population_female_sizes = top20_populated_cities["population_total"].apply(lambda x: int(x / 5000))
plt.scatter(x_female, y_female, s=100, marker="o", c=population_female_sizes,  cmap=cm.Dark2,alpha=0.8)

for ncs, xpt, ypt in zip(city_name_female, x_female, y_female):
    plt.text(xpt + 6000, ypt + 3000, ncs, fontsize=10, fontweight='bold')

plt.title('Top 20 Female Dominated Cities in India', fontsize=20)

# 전체 그래프 출력
plt.tight_layout()
plt.show()





top_pop_cities = data.sort_values(by='population_total',ascending=False)
top20_populated_cities=top_pop_cities.head(5)
top20_populated_cities
data['lattitude'] = data['location'].apply(lambda x: x.split(',')[0])
data['longitude'] = data['location'].apply(lambda x: x.split(',')[1])
top20_populated_cities.head(5)


from IPython.display import display
top20_female = data.nlargest(5, 'sex_ratio')[['name_of_city','population_total', 'population_female','sex_ratio']]
display(top20_female)
data['lattitude'] = data['location'].apply(lambda x: x.split(',')[0])
data['longitude'] = data['location'].apply(lambda x: x.split(',')[1])
top20_female.head(5)

