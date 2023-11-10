---
title: CoFee
url: https://ieeexplore.ieee.org/document/10216467
---

## Bibtex

```
@inproceedings{cofee,
    author    = {Schrötter, Max and Schnor, Bettina},
    title     = {Leveraging Continuous Feedback in Education to Increase C Code Quality},
    year      = {2022},
    booktitle = {2022 International Conference on Computational Science and Computational Intelligence (CSCI)},
    doi       = {10.1109/CSCI58124.2022.00351}
}
```

## Zusammenfassung

[CoFee (COntiuous FEEdback)](https://www.cs.uni-potsdam.de/bs/research/projectSecurity.html#cofee) ist ein Feedback-System, welches an der Universität Potsdam entwickelt und für die Feedback-Generierung für Abgaben in der Programmiersprache C eingesetzt wird. Es basiert auf der Idee, eine selbst-gehostete GitLab-Instanz als Ausführungseinheit zu verwenden. Sehr ähnlich zu unseren Ideen arbeiten Studierende in einem Repository und können Abgaben über Git pushen, wodurch eine Pipeline angestoßen wird, die Feedback generiert. 

Anschließend können die Studierenden sich die Ergebnisse über eine Web-UI anschauen. Die Web-UI wird über GitLab-Pages gehostet. Einen Link dazu finden Studierende in der Beschreibung eines Repositorys. Die Web-UI enthält eine Auflistung aller Fehler, die mit zusätzlichen Hinweisen angereichert ist. Die Hinweise können von Lehrenden in einer extra Datei definiert werden und werden automatisch den passenden Fehlertypen hinzugefügt. Des Weiteren enthält die Web-UI Verlinkungen zu den "Rohdaten" der Analyse-Tools, z.B. XML-Outputs, aber auch die Standard-HTML-Outputs.

Im Gegensatz zu unserem Ansatz sind alle Repositorys privat und werden innerhalb des Kurses verwaltet. Die Studierenden sortieren sich im LMS (in derem Fall Moodle) in kleinen Gruppen ein (i.d.R. Zweier-Gruppe). Diese Information kann aus dem LMS exportiert werden. Ein Skript erstellt anhand des Exports für jede Gruppe auf dem selbst gehosteten GitLab-Server in einer Obergruppe für das Semester kleinere Gruppen für die Moodle-Gruppen, in denen die jeweiligen Repositorys für die Studierenden automatisch erstellt werden. Sobald die Studierenden auf dem GitLab-Server einen Account haben, erhalten diese auch automatisch Zugriff auf ihre Aufgaben-Repositorys.

Ein weiterer Unterschied ist die Verwaltung der CI/CD-Pipeline und der Dateien zu den Aufgaben. Deren CI/CD-Pipeline wird in einem Einstellungsfenster in GitLab verlinkt anstatt dass eine YAML-Datei zur Konfiguration im Repository selbst liegt. Des Weiteren gibt es keine Datei zur Aufgabenkonfiguration und auch andere Dateien (z.B. Makefile) werden über die CI/CD-Pipeline zur Verfügung gestellt und liegen nicht im Studierenden-Repository.

Features, die denen fehlen, bei uns aber implementiert sind, sind die Benotung der Abgaben, das Auschecken des Abgabedatums und das System zum Verhinden von unerlaubtem Ändern von Dateien.

Deren System ist öffentlich verfügbar auf [GitLab](https://gitlab.com/schrc3b6/cofee_up). Das dazugehörige Studierenden-Repositry mit verlinkter Ergebnis-Webseite ist [hier](https://gitlab.com/cofee-demo/c-demo) zu finden.
