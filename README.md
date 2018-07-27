Stand:   20180728
Version: L.0.502


**hgm.py ist ein HAMGO Messenger Client für Linux.**

Das Programm ist in python geschrieben. Als GUI Framework wurde
PyGObject/Gtk3 verwendet.

Er basiert auf dem Windows .NET Client von OE1KBC
sowie dem HAMGO Protokoll von Alex OE1VQS und Kurt OE1KBC.

Die Linux Version wurde von 
Reinhold OE5RNL und Manfed OE5NVL erstellt.

Das Programm sollte auf allen gängigen Linuxplattformen laufen.

Konkret getestet wurden: 

* Ubuntu   16.04 LTS
* Ununtu   18.04 LTS
* Debian   9.4.0 
* Debian   8.7.1
* Raspbian 9 (stretch)


Weitere Infos im HAMNET: http://news.ampr.org

Im Internet: https://oevsv.at/

-----------------------------------------------------------------
Installation:

Es sind nur die Dateien des Repositories in ein beliebiges 
Verzeichnis zu kopieren und hgm.py zu starten.

git clone https://github.com/oe5rnl/hamgo-linux-client.git

cd hamgo-linux-client

./hgm.py

Dann im Menüpunkt Setup das Call, Name, Server-IP,
eigene IP  etc eingeben.

Als HAMGO Server können z.B. verwendet werden:

44.143.0.1 

44.143.25.1

44.143.104.135

-----------------------------------------------------------------
Folgened Abhängigkeiten sollten normalerweise bereits erfüllt sein:

* python 3
* PyGObject
* aplay



-----------------------------------------------------------------
Hinweise:

Zur Soundwidergabe wird /usr/bin/aplay verwendet.
Bitte im Setup ein Audiodevice wählen und mit "Audio Test"
überprüfen. 


* Warum wurde für die Oberfläche kein Glade verwendet ?

  Erstens wollte ich die API kennen lernen.  
  Zweitens gab es bei den Treeviews nicht nachvollziehbare Porobleme...


------------------------------------------------------------------
TODO:

* Filetransfer
* Group Call zu Rufzeichen
* Logfile
* main_header color stimmt nicht immer

Neu:
* Senden mit CR
* Begrezung der Message Textlänge 
* Gui Widgets in Objekte verpackt


73, OE5RNL Reinhold
