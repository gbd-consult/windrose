**Wichtig:** Um die Datei `all_stations_metdb.csv` verwenden zu können, muss der Name des Attributs `end` angepasst werden, da dies ein Schlüsselwort in Python ist.
Wir ändern dies in diesem Beispiel auf `enddate`

Zunächst kopieren wir die Datei `windrose.py` in das QGIS Python Verzeichnis.
```
cp windrose.py ~/.local/share/QGIS/QGIS3/profiles/default/python
```
Anschließend erstellen wir in QGIS eine *Python Action* mit folgendem Inhalt:
```
from windrose import windrose
windrose([[%n000%],[%n030%],[%n060%],[%n090%],[%n120%],[%n150%],
    [%n180%],[%n210%],[%n240%],[%n270%],[%n300%],[%n330%]],
    [%ntotal%], '[%id%]', '[%station%]', '[%net%]', '[%start%]',
    '[%enddate%]', [%hasl%], [%hagr%], [%avgff%], [%calm%])
```
Für das *Balkendiagramm* wird eine eigene *Python Action* äquivalet dazu erzeugt:
```
from windrose import balken
balken([[%wgk1%],[%wgk2%],[%wgk3%],[%wgk4%],[%wgk5%],
    [%wgk6%],[%wgk7%],[%wgk8%],[%wgk9%]],
    '[%id%]', '[%station%]', '[%net%]', '[%start%]',
    '[%enddate%]', [%hasl%], [%hagr%], [%avgff%])
```
