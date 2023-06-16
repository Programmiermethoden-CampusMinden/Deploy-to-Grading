---
title: Ergebnispräsentation
---

## Für Studierende

Bei der Ausgabe für Studierende wird unterschieden zwischen einer einfachen Ausgabe über die Konsole der GH-Action und einer webbasierten Ergebnispräsentation.

### Einfache Ergebnisausgabe für Studis

Als erste Präsentation der Ergebnisse soll eine einfache Ausgabe auf der Konsole des Workflows herhalten. Dazu gehört die Präsentation der Fehler, für die Punkte abgezogen wurden und am Ende eine Übersicht über die erreichte Punktzahl.

Die Ausgabe von Fehlern sieht folgendermaßen aus:

```
[TESTKLASSE (ABZUG)] KURZE_BESCHREIBUNG_DES_FEHLERS
```

Beispiel:

```
[JUnit (-1 Punkt)] Test `testSetVelocityNegative()` fehlgeschlagen.
```

*Anmerkung: Eine detailliertere Ausgabe der Fehler soll durch eine lokale Ausführung mit gradle möglich sein.*

Die Zusammenfassung sieht dann folgendermaßen aus:

```
Aufgabenblatt: NAME
Abgabedatum: DATUM
Beteiligte Studis: LIST_STUDIS
Erreichte Gesamtpunktzahl: P/ALL

|-----------|--------|
|  Aufgabe  | Punkte |
|-----------|--------|
| Aufgabe 1 |     19 |
| Aufgabe 2 |     10 |
|    ...    |      . |
|-----------|--------|
```

Erklärungen:
- NAME: Name des Aufgabenblattes
- DATUM: Abgabedatum
- LIST_STUDIS: Liste der Studierenden, die mindestens einmal für diese Abgabe committed haben
- P: Erreichte Punktzahl
- ALL: Maximal erreichbare Punktzahl

*Anmerkung: Die Formatierung der Tabelle kann in der finalen Implementierung anders ausehen.*

### Webbasierte Ergebnispräsentation für Studis (Optional)

Da bei der konsolenbasierten Ausgabe die Übersicht wahrscheinlich nicht wirklich gut sein wird, ist eine zweite Ausgabevariante sinnvoll, die insbesondere bei der Ausgabe der einzelnen Fehler hilfreicher sein soll. Im Allgemeinen ist die Idee vergleichbar zu der [Übersicht von JPlag](https://jplag.github.io/JPlag/). Auf einer über GitHub.io gehosteten Webseite können Studierende ihre Ergebnisse in Form eines `zip`-Archivs hochgeladen. Dieses Archiv wird in Frontend verarbeitet und die Informationen daraus dargestellt.

Das `zip`-Archiv wird von der GH-Action als [Artefakt](https://docs.github.com/de/actions/using-workflows/storing-workflow-data-as-artifacts) ([GH-Action](https://github.com/actions/upload-artifact)) zur Verfügung gestellt und kann von GitHub heruntergeladen und auf die Webseite hochgeladen werden. Es enthält eine Zusammenfassung der Ergebnisse sowie die Aufgaben- und Aufgabenblattdefinitionen und die Ausgaben der einzelnen Tests (JUnit, Checkstyle, ...).

## Für Lehrende

Die finale Rückmeldung an Lehrende sollte eine einfach weiterzuverarbeitende `results.csv`-Datei im folgenden Format sein:

```
name,mat_number,usernames,repository,no_commits,grade,overall_points,assignment1,assignment2,...
Max Mustermann,123456,mustermax;mmuster3000,https://github.com/mustermax/tasks,0,1.7,176,40,38,...
```

*Anmerkung: Je nachdem, was präferiert wird, können wir auch Semikolons statt Kommata nutzen.*

Erklärungen:
- name: Vollständiger Name des/der Studierenden
- mat_number: (optional?) Matrikelnummer des/der Studierenden
- usernames: Liste an GitHub-Benutzernamen, die von dem/der Studierenden verwendet werden
- repository: Repository, an dem mitgearbeitet wurde (Im Falle von Gruppenwechseln bräuchten wir hier eine Liste)
- no_commits: Anzahl an Aufgabenblättern, an denen nicht aktiv mitgearbeitet/mitcommitet wurde
  - *Notiz: Hier muss noch definiert werden, ob die Punktzahl trotzdem zu der Gesamtpunktzahl gerechnet wird oder nicht.*
- grade: (optional) Note für das Praktikum
- overall_points: Gesamtpunktzahl für alle Aufgabenblätter zusammen
- assignment1,assignment2,...: Punkte für die einzelnen Aufgabenblätter

*Anmerkung: Statt oder zusätzlich zu `name` könnte der ILIAS-Name oder die E-Mail-Adresse angegeben werden.*

Für eine detailliertere Übersicht über die Punktzahlen einzelner Studierenden existiert für jede Person noch eine eigene `{firstname_lastname_mat_number}.csv`-Datei (z.B. `max_mustermann_123456.csv`).

```
assignment,usernames,repository,has_commit,overall_points,task1,task2,...
Aufgabenblatt 1,mustermax,https://github.com/mustermax/tasks,true,40,10,10,...
```

Erklärungen:
- assignment: Name des Aufgabenblattes
- usernames: Liste an GitHub-Benutzernamen, die von dem/der Studierenden für dieses Aufgabenblatt verwendet wurden
- repository: Repository, in dem das Aufgabenblatt abgegeben wurde
- has_commit: true/false. Zeigt an, ob aktiv an der Aufgabe mitgearbeitet wurde
- overall_points: Gesamtpunktzahl für das Aufgabenblatt
- task1,task2,...: Punkte für die einzelnen Aufgaben

Je nachdem, ob die finale Bewertung als GH-Action oder lokal ausgeführt wird, wird entweder ein Ordner `results` mit den Dateien erstellt oder dieser wird in einer `results.zip` verpackt und als Artefakt in der GH-Action hochgeladen.

In einem Archiv `{firstname_lastname_mat_number}/` (z.B.  `max_mustermann_123456/`) werden die Ergebnisse einzelner Aufgabenblätter in `.zip`-Archiven gespeichert, sodass sie in der webbasierten Ergebnispräsentation für Studis angesehen werden können.
