---
title: Skripte für Lehrende
---

Für Lehrende stehen neben dem Skript `scripts/deploy_to_grading.py` zur Ausführung der D2G-Pipeline in einem Aufgaben-Repository zwei weitere Skripte zum Einsammeln und Auswerten der Ergebnisse zur Verfügung. Dies sind das Skript `scripts/deploy_to_grading_teacher.py`, welches für ein Aufgabenblatt die Abgaben aller Studierende einsammelt und eine Zusammenfassung der Ergebnisse für dieses Aufgabenblatt ausgibt, und das Skript `scripts/teacher_summary.py`, welches aus den Ergebnissen aller Aufgabenblätter eine Übersicht über die Ergebnisse über z.B. ein gesamtes Semester erstellt.

### deploy_to_grading_teacher.py

Das Skript `scripts/deploy_to_grading_teacher.py` ermittelt für ein Aufgabenblatt die von den Studierenden erreichten Punkte und fasst diese in einer Excel-Datei zusammen. Über den folgenden Befehl kann das Skript gestartet werden. Dabei muss die `D2G_PATH`-Umgebungsvariable, wie in der [README](readme.md) beschrieben, gesetzt sein. Wenn der Plagiatscheck mit ausgeführt werden soll, dann muss zusätzlich die Umgebungsvariable `ASSIGNMENT_TEMPLATE_REPOSITORY` über den `export`-Befehl auf die URL des Vorgaberepositorys gesetzt sein.

```bash
scripts/deploy_to_grading_teacher.py [submissions.xlsx]
```

Die Datei `submissions.xlsx` muss zuvor aus dem LMS exportiert werden. Beim Einlesen der Datei wird aktuell nur das Format aus ILIAS unterstützt, welches sich aus den Spalte `Nachname`, `Vorname`, `Benutzername`, `Datum der letzten Abgabe` und `Textabgabe` zusammensetzt. Um diese Datei exportieren zu können, müssen Lehrende in einem ILIAS-Modul ein Übung-Objekt hinzufügen. In diesem muss eine Übungseinheit mit dem Abgabetyp `Text` erstellt werden. Dort tragen Studierende den Link zum Pull Request ihrer Abgabe ein.

Das Ergebnis des Skript ist eine Excel-Datei, in der für jeden Studierenden die erreichte Gesamtpunktzahl und die erreichten Punkt für die einzelnen Aufgaben aufgelistet sind. Für detaillierte Informationen zu einer Abgabe liegen im Order `repos` die von den Studierenden abgegebenen Dateien mitsamt `results`-Ordner, in dem die Ergebnisse für jede Aufgabe und jede Metrik zu finden sind.

### teacher_summary.py

Das Skript `scripts/teacher_summary.py` fasst die Ergebnisse der Studierenden über mehrere Aufgabenblätter hinweg zusammen und berechnet eine Gesamtpunktzahl. Dazu müssen dem Skript die vom oben beschriebenen Skript generierten Dateien wie im folgenden Befehl übergeben werden:

```bash
scripts/teacher_summary.py [file1] [file2] ...
```

Die aus der Ausführung resultierende Excel-Datei enthält für jeden Studierenden dessen LMS-Benutzernamen, vollständigen Namen, die erreichte Gesamtpunktzahl zusammen mit der maximal erreichbaren Gesamtpunktzahl sowie die erreichten Punkte und maximal erreichbaren Punkte für jedes Aufgabenblatt. Diese Ausgabe muss manuell zurück in das LMS überführt werden.
