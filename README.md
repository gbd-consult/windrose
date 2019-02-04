# windrose
Skript zum Darstellen einer Windrose aus einem Punktlayer.

Dies ist ein Python-Programm, das aus einer Karte von Stationen, beim Anklicken 
aus einer Gesamtdatei aller Stationen im CSV Format (angehängt) den passenden 
Record herausfiltert und die dort abgelegten Werte zu einer Grafik verarbeitet, 
sie dann angezeigt wird. Man sollte diese Grafik auch als bspw. als PNG 
abspeichern können.

Hauptaufgabe des Skripts ist die Darstellung nach einer festen Vorgabe, die in 
der Datei vorschlag_stations-windrose.pdf zu sehen ist. Es kann als "Action" in 
QGIS eingebunden werden - siehe INSTALL.md und das QGIS 3 Projekt example.qgs.

Die Grafik ist absichtlich so aufgebaut, dass mann nicht die Skripte aus 
matplotlib o.ä. benötigt.

Zum Testen dienen ein paar Punkte der Datei meteo_ifu_allstations.csv. 
Das ist eine Stationsliste, in der die Parameternamen in der Kopfzeile stehen.
