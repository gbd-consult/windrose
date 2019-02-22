"""
    Skript zum Erstellen von Windrose Plots aus CSV Dateien.
    python3 fromcsv.py pfad/zur/datei.csv ordner/fuer/ausgabe

"""
import csv
import sys
import os.path
from windrose import windrose

csv_file = sys.argv[1]
out_path = sys.argv[2]

stations = []
with open(csv_file, encoding = 'latin1') as csvfile:
    reader = csv.DictReader(csvfile, delimiter = ',')
    for row in reader:
        stations.append(dict(row))

for s in stations:
    values = [int(s.get('n' + str(x).rjust(3,'0'))) for x in range(0, 360, 30)]
    
    print('generating plot: %s %s' % (s.get('net'), s.get('id')))
    windrose(values, int(s.get('ntotal')),
        s.get('id'), s.get('station'), s.get('net'),
        s.get('start'), s.get('enddate'), s.get('hasl'),
        s.get('hagr'),  float(s.get('avgff')),
        int(s.get('calm')), os.path.join(out_path, '%s_%s.png' % (s.get('net'), s.get('id'))))
