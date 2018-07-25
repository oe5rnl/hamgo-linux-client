Stand:   20180724
Version: L.0.5


**hgm.py ist ein HAMGO Messenger Client für Linux.**

Er basiert auf dem Windows .net Client von OE1KBC
sowie dem HAMGO Protokoll von Alex OE1VQS und Kurt OE1KBC.

Die Linux Version wurde von 
Reinhold OE5RNL und Manfed OE5NVL erstellt.


Weitere Infos im HAMNET: http://news.ampr.org

Im Internet: https://oevsv.at/

Das Programm sollte auf allen gängigen Linuxplattformen laufen.

Konkret getestet wurden: 

* Ubuntu   16.04 LTS
* Ununtu   18.04 LTS
* Debian   9.4.0 
* Debian   8.7.1  
* Raspbian 9 (stretch)


-----------------------------------------------------------------
Installation:

Es sind nur die Dateien des Repositories in ein beliebiges 
Verzeichnis zu kopieren und hgm.py zu starten.

git clone https://github.com/oe5rnl/hamgo-linux-client.git

cd hamgo-linux-client

./hgm.py

Dann im Menüpunkt Setup das CALL etc eingeben.

Benötigt werden:
* python 3
* PyGObject
* aplay

Als HAMGO Server können z.B. verwendet werden:

44.143.0.1 

44.143.25.1

44.143.104.135


-----------------------------------------------------------------
Hinweise:

Zur Soundwidergabe wird /usr/bin/aplay verwendet.
Bitte im Setup ein Audiodevice wählen und mit "Audio Test"
überprüfen. 


* Warum wurde für die Oberfläche kein Glade verwendet ?

  Erstens wollte ich die API kennen lernen.  
  Zweitens gab es bei den Treeviews nicht nachvollziehbare Porobleme...

* Warum wurde in den Modulen für die GUI keine Klassen verwendet ?

  Diese Version hatte ich ...
  Allerdings gab es hier nicht nachvollziebare Probleme beim updaten 
  der GUI, auch mit GLib.idle_add().

------------------------------------------------------------------
TODO:

* Filetransfer
* Group Call zu Rufzeichen
* Senden mit CR
* Begrezung der Message Textlänge 
* Logfile
* Yourcall check
* main_header color stimmt nicht immer


73, OE5RNL Reinhold
