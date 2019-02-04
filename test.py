import csv
from windrose import windrose

stations = []
with open('./all_stations_metdb.csv', encoding = 'latin1') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        stations.append(dict(row))


my_station = stations[2902]
print(my_station)

values = [int(my_station.get('n' + str(x).rjust(3,'0'))) for x in range(0, 360, 30)]

windrose(values, int(my_station.get('ntotal ')),
    my_station.get('id'), my_station.get('station'), my_station.get('net'),
    my_station.get('start'), my_station.get('end'), my_station.get('hasl'),
    my_station.get('hagr'),  float(my_station.get('avgff')), int(my_station.get('calm')))

