---
layout: talk
date: 2017-01-30 18:00:00
thumbnail: kennyp.jpg
title: ".NET Threading im Detail"
doodle: 7h6i68cr9m7pit7h
speaker:
  name: Kenny Pflug
  description: Kenny Pflug studierte Informatik an der Ostbayerischen Technischen Hochschule Regensburg und ist aktuell Promovend und wissenschaftlicher Mitarbeiter am Universitätsklinikum Regensburg. Dort erforscht er User Interface Konzepte für mobile Medizinapplikationen. Er ist besonders interessiert an den Themengebieten User Experience und User Interface Design, OOP und OOD, Softwarearchitektur, Clean Code sowie Automatisiertes Testen.
  social:
    - title: rss
      url: http://www.feo2x.com
    - title: twitter
      url: https://twitter.com/feO2x
    - title: youtube
      url: https://www.youtube.com/c/kennypflug/
video:
  url: https://youtu.be/Le3w51xV3f8
  thumbnail: https://i.ytimg.com/vi/Le3w51xV3f8/mqdefault.jpg
downloads:
  - name: GitHub Repository mit Beispielcode und PowerPoint Präsentation
    url: https://github.com/feO2x/NetThreadingInDetail
---
Multithreading ist aus kaum einer Anwendung wegzudenken: sei es um langlebige Operationen vom UI-Thread auszulagern, oder um komplexe Berechnungen auf mehrere Threads zu verteilen. Dabei muss man sich vor allem um die korrekte Synchronisierung der Daten kümmern, die von mehreren Threads angesprochen werden. Doch was genau macht ein Lock eigentlich und welche Auswirkungen hat es auf den Thread Pool?

All das und noch viel mehr wird in diesem Talk besprochen. Neben Synchronization Primitives und Synchronization Contexts sowie async / await in Verbindung mit der Task Parallel Library (TPL) gehen wir auch auf die Details des Thread Pools ein und insbesondere auf die Möglichkeiten, Lock-freie Primitiven zur Synchronisation einzusetzen und die daraus resultierenden Algorithmen und Datenstrukturen anzuwenden.