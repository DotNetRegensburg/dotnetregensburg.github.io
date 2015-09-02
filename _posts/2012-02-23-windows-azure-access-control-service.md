---
layout: talk
date: 2012-02-23 18:30:00
thumbnail: azure.png
title: Der Windows Azure Access Control Service
speaker:
  name: Jörg Jooss
  description: Jörg Jooss unterstützt als Software-Architekt im Microsoft Technology Center (MTC) in München Microsoft-Kunden und -Partner beim Entwurf und der Erstellung .NET-basierter Lösungen.  Zu seinen Interessensschwerpunkten zählen die Entwicklung verteilter Anwendungen, Entwurfsmuster und Entwicklungsmethoden. Bevor er im Jahr 2005 zu Microsoft kam, war er über viele Jahre als Technologie-Berater für eine international führende Unternehmensberatung tätig.
  social:
    - title: xing
      url: https://www.xing.com/profile/Joerg_Jooss
---
Der Windows Azure Access Control Service (ACS) ist ein cloudbasierter Dienst, der es ermöglicht die Authentifizierung und Autorisierung von Benutzern vom Anwendungscode von Webanwendungen und -dienste zu trennen. Anstatt für eine Anwendung ein eigenes, anwendungsspezifisches Authentifizierungssystem mit Benutzerkonten zu implementieren, kann der ACS die Authentifizierung sowie einen Großteil der Autorisierung der Benutzer orchestrieren. 

ACS lässt sich mit auf offenen Standards basierenden Identitätsanbieter (z. B. in Unternehmensverzeichnisse wie etwa Active Directory) und Webidentitäten integrieren, z. B. in Windows Live ID, Google, Yahoo! und Facebook. Während der letztgenannte Aspekt auch für nicht auf Windows Azure laufende, öffentlich zugängliche Webanwendungen interessant ist, ist besonders die Integration mit einem Active Directory eine elementare Anforderung für Enterprise-Anwendungen, die auf Windows Azure laufen sollen. 