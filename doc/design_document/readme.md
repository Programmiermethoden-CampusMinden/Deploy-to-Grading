---
title: D2G-Designdokument
---

In diesem Designdokument wird ein Konzept vorgestellt, durch das wir den bisherigen Abgabeprozess im Modul Programmiermethoden des Studiengangs Informatik an der Hochschule Bielefeld mit einer automatischen Bewertung verknüpfen möchten. Studierende bearbeiten die Aufgaben lokal, laden ihre Lösungen in ihr Team-Repository auf einem Git-Server und erstellen zur Abgabe einen Pull Request. Commits zu diesem Pull Request sollen automatisch eine GitHub Action ausführen, die den Bewertungsprozess durchführt. Studierende können in der Ausgabe der GitHub Action ihre erreichte Punktzahl einsehen. Im Gegensatz zu anderen automatischen Bewertungssystemen nutzen wir keine eigene Serverstruktur und lehren gleichzeitig den Umgang mit Git und Free Open Source Software (FOSS). Daher ist unser automatisches Bewertungssystem eher für fortgeschrittenere Programmierkurse ab dem zweiten Semester geeignet.

## Inhaltsverzeichnis

1. [Ablauf des Deploy-to-Grading](d2g_procedure.md)
2. [Testmetriken](metrics.md)
3. [Repositorystrukturen](repository_structure/README.md)
4. [Ergebnispräsentation](result_presentation.md)


### Weitere outdated Issues

- [Deploy-to-Grading konzipieren #10](https://github.com/Programmiermethoden/Deploy-to-Grading/issues/10)
- [Deploy-to-Grading How to #11](https://github.com/Programmiermethoden/Deploy-to-Grading/issues/11)
- [Build Script für alle Task #15](https://github.com/Programmiermethoden/Deploy-to-Grading/issues/15)

*Anmerkung: Diese Issues sind hier verlinkt, da sie noch Relevanz haben könnten.*
