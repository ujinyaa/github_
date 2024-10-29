

#compare  total literablity in india womean literablity in india
#we should see the longityde and latitiude of each paramater of dataset.

top150city_literatability['latitude'] = data.loc[top150city_literatability.index, 'latitude']
top150city_literatability[longitude]


top150female_literatability
top150female_literatability


plt.figure(figsize=(80, 15))

plt.subplot(1, 2, 1) 
map = Basemap(width=1200000, height=900000, projection='lcc', resolution='l',
              llcrnrlon=67, llcrnrlat=5, urcrnrlon=99, urcrnrlat=37, lat_0=28, lon_0=77)

map.drawmapboundary()
map.drawcountries()
map.drawcoastlines()

longitude = np.array(top150_populated_cities['longitude'])
latitude = np.array(top150_populated_cities['latitude'])
total_population = np.array(top150_populated_cities['population_total'])
city_name = np.array(top150_populated_cities['name_of_city'])

x, y = map(longitude, latitude)
population_sizes = top150_populated_cities["population_total"].head(50).apply(lambda x: int(x / 3000))
plt.scatter(x[:50], y[:50], s=population_sizes, marker="o", c=population_sizes, cmap=cm.Dark2, alpha=0.8)

for ncs, xpt, ypt in zip(city_name, x[:50], y[:50]):
    plt.text(xpt + 6000, ypt + 3000, ncs, fontsize=10, fontweight='bold')

plt.title('Top 150 Populated Cities in India', fontsize=20)


plt.subplot(1, 2, 2)
map = Basemap(width=1200000, height=900000, projection='lcc', resolution='l',
              llcrnrlon=67, llcrnrlat=5, urcrnrlon=99, urcrnrlat=37, lat_0=28, lon_0=77)

map.drawmapboundary()
map.drawcountries()
map.drawcoastlines()

longitude_female = np.array(top150_female['longitude'])
latitude_female = np.array(top150_female['latitude'])
female_population = np.array(top150_female['population_female'])
city_name_female = np.array(top150_female['name_of_city'])


x_female, y_female = map(longitude_female, latitude_female)
population_female_sizes = top150_female["population_female"].head(50).apply(lambda x: int(x / 3000))
plt.scatter(x_female[:50], y_female[:50], s=population_female_sizes, marker="o", c=population_female_sizes,  cmap=cm.Dark2,alpha=0.8)

for ncs, xpt, ypt in zip(city_name_female, x_female[:50],  y_female[:50]):
    plt.text(xpt + 6000, ypt + 3000, ncs, fontsize=10, fontweight='bold')

plt.title('Top 150 Female Dominated Cities in India', fontsize=20)

# 전체 그래프 출력
plt.tight_layout()
plt.show()
