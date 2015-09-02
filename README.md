# Webseite der .NET Usergroup Regensburg

## Aufbau

Die Seite verwendet Jekyll als Blogging Engine. Die gesamte Konfiguration ist in *_config.yml* gespeichert. Die Vorträge sind in *_posts* abgelegt. Das genaue Format der Metadaten ist:

```
layout: talk
date: (Datum im Format z.B. "2015-06-29 18:30:00 +2")
thumbnail: (Dateiname Vortragsbild)
title: (Vortragstitel)
speaker:
  name: (Sprechername)
  description: (Sprecherbeschreibung)
  social:
    - title: (z.B. twitter, github, rss, ...)
      url: (Url)
video:
  url: (Url zum Video)
  thumbnail: (Vorschaubild zum Video: 320x180 Pixel)
downloads:
  - name: (Name des Downloads)
    url: (Url zum Download, z.B. https://github.com/DotNetRegensburg/Downloads/tree/2015-06-29)
```

Der Videoeintrag ist optional. Wird er weggelassen, so wird kein Eintrag in der Videosektion generiert. Bei "social" können beliebig viele Einträge angegeben werden.

Analog "downloads". Diese Sektion auch optional, wobei beliebig viele Einträge verwendet werden können. Der Beispiellink würde zum entsprechenden Branch für die Downloads des Vortrags führen.

## Inhalte

Bei den Bildern gibt es folgendes zu beachten:

* Teambilder kommen in *img/team* und sollten **225x225* Pixel groß sein.
* Bilder für Logos sind in *img/logos*, hier gelten verschiedene Größen (immer einheitlich pro Zeile):

  - Die beste Größe ist **200x50** Pixel. Hier gehen 4 Bilder pro Zeile (lg).
  - Extragroße Sponsorenbilder haben **280x150** Pixel. Hier sind 3 Bilder pro Zeile möglich.
  - Daneben kommen noch **200x130** und **200x100** Pixel zum Einsatz. Jeweils auch 4 Bilder pro Zeile.

* Die Bilder für die Vorträge sind in *img/talks* gespeichert. Als Größe empfiehlt sich **200x200** Pixel.
* Die Bilder für die Videos und News werden automatisch aus den entsprechenden Feeds gezogen.

Der Graustufen-Effekt ist über CSS implementiert und benötigt daher keine weitere Bearbeitung. Die Bilder sollten immer mit Farbe abgespeichert werden.

## Lizenz

Die Seite verwendet die MIT Lizenz. Der ursprüngliche Theme (Agency) verwendet die Apache 2.0 Lizenz (Ersteller: Start Bootstrap). Die eingesetzten Komponenten (z.B. Bootstrap, jQuery) werden im Sinne der jeweiligen Lizenz verwendet.