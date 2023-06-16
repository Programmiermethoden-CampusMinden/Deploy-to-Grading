---
title: Ablauf des D2G
---

## Vergleich Docker vs Cmd-based

| Docker                                                                                  | Cmd-based                                                  |
| --------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| Kann mit wenigen Änderungen sowohl auf GitHub, GitLab als auch lokal ausgeführt werden. | Ablauf des Programms direkt in der Definition ersichtlich. |
|                                                                                         | Kein Docker-Overhead.                                      |

**Zusammenfassung:** Auch wenn in der Tabelle mehr Vorteile für eine Cmd-basierte Action genannt sind, ist der aktuelle Favorit von mir die Docker-basierte Action, da sie flexiber ist. Ein deutlicher Nachteil der Docker-basierten Action ist der Overhead und damit die längere Ausführungszeit. Ob es im Hinblick auf das verfügbare Zeitkontingent (2.000 min/Monat auf Linux für GitHub Free) Probleme geben könnte, muss während der Implementierung geprüft werden.

## Ablauf in der GH-Action

Im folgenden wird der Ablauf der GH-Action beschrieben:

| Schritt | Bezeichnung                                                          | Beschreibung                                                                                                                                                                                                                                                                              |
| ------- | -------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.      | Aufgabenblatt-yml laden                                              | Einlesen der Aufgabenblatt-yml (Definiert in [Definition von Konfigurationsdateien für Aufgabenblatt- und Aufgabendefinition](repository_structure/task_and_assignment_structure.md)). Relevant sind für die Bewertung das Abgabedatum (`due_date`) und die Liste der Aufgaben (`tasks`). |
| 2.      | Vorbereiten des Repositories                                         | Basierend auf dem Abgabedatum (`due_date`) wird das Repository passend ausgecheckt.                                                                                                                                                                                                       |
| 3.      | Aufgaben-yml laden (wiederholend bis 6. für jede Aufgabe in `tasks`) | Einlesen der Aufgaben-yml für die jeweilige Aufgabe. Relevant sind die Tests (`tests`) und die Liste an nicht zu überschreibenden Dateien (`no_override`).                                                                                                                                |
| 4.      | Überschreiben der Vorlagendateien                                    | Zur Vermeidung von veränderten Vorgabedateien werden alle in der Aufgabe vorhandenen Dateien mit den Dateien aus der Vorgabe überschrieben (Ausgenommen Lösungendateien, die nicht in der Vorlage vorhanden sind, und Dateien, die in `no_override` genannt sind.                         |
| 5.      | Ausführen des Tests (wiederholend bis 6. für jeden Test in `tests`)  | Führt den jeweiligen Test aus. Die Ausführung wird über Gradle angestoßen. Ergebnisse werden im Ordner `results/{task}/{test}/` gespeichert.                                                                                                                                              |
| 6.      | Auswerten der Ergebnisse der Tests                                   | Wertet die Ergebnisse der Tests aus und berechnet die erreichte Punktzahl für die jeweilige Aufgabe. Die Ergebnisse werden in der Datei `results/{task}/result.yml` gespeichert.                                                                                                          |
| 8.      | Präsentation der Ergebnisse                                          | Gibt die Ergebnisse auf der Konsole aus und stellt die Ergebnisse als Artefakt zur Verfügung (`results`-Ordner als `zip`-Datei).                                                                                                                                                          |

### Format der result.yml

```
task:                 # Name der Aufgabe für eine eindeutige Zuordnung
students:             # Liste mit Git-Namen der Studierenden, die an der Aufgabe beteiligt waren
tests:                # Metriken, die bei dieser Aufgabe ausgeführt wurden
  junit:
    mistakes:         # Auflistung aller Fehler innerhalb dieser Metrik
      - deduction:    # Anzahl Punkte, die für den Fehler abgezogen wurden
        description:  # Beschreibung des Fehlers
    points:           # Anzahl Punkte, die bei dieser Metrik erreicht wurden
    max_points:       # Maximal erreichbare Punktzahl (Hier notwendig für Vergabestrategie wie bei JUnit)
```

## Für Lehrende

### Übersicht

Das Deploy-to-Grading, welches Studierende über die GitHub Action ausführen, soll von Lehrenden auch lokal in einem Docker Container zur Sammlung der Ergebnisse ausgeführt werden können. Zur Zusammenführung von ILIAS- und GitHub-Daten geben Studierende im ILIAS die URL zu ihrem Pull Request ab.

Aus dem ILIAS kann von Lehrenden folgende Liste heruntergeladen werden:
```
student,pr
ILIAS_NAME,PR_URL
```
*Hinweis 1: Da ich gerade nicht weiß, wie bei ILIAS die Ergebnisse bei Textabgaben aussehen, habe ich jetzt vereinfacht eine csv-Datei angenommen.*

*Hinweis 2: In der csv-Datei fehlt aktuell noch die Zuordnung ILIAS-Name <-> GitHub-Username. Da müsste geprüft werden, was ILIAS für Möglichkeiten hierfür bietet. Alternativ wäre eine "Abgabe" des GitHub-Usernames zu Beginn des Semesters möglich.*

### Ablauf

Im Folgenden wird der D2G-Ablauf für Lehrende beschrieben:

| Schritt | Bezeichnung                                                     | Beschreibung                                                                                                                                                                                                                                                                                                                                                                          |
| ------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.      | *csv*-Datei einlesen                                            | Einlesen der Daten aus dem ILIAS.                                                                                                                                                                                                                                                                                                                                                     |
| 2.      | Auswerten der Ergebnisse (für jeden Eintrag in der *csv-Datei*) | Für jede(n) Studierenden werden die Ergebnisse der abgegebenen Aufgabe aus dem jeweiligen Repository geladen und überprüft. Alternativ ist es auch möglich, den Deploy-to-Grading-Prozess für jede Abgabe erneut auszuführen. Dies ist zum Beispiel notwendig, wenn das herunterzuladende Artefakt nicht mehr verfügbar ist oder Änderungen an der GitHub Action festgestellt wurden. |
| 3.      | Plagiatsprüfung                                                 | Da an dieser Stelle alle Abgaben der Studierenden an einem Ort gesammelt sind, kann eine Plagiatsprüfung durchgeführt werden.                                                                                                                                                                                                                                                         |
| 4.      | Export der Ergebnisse                                           | Die gesammelten Ergebnisse werden so aufbereitet, dass sie ins ILIAS übertragen werden können.                                                                                                                                                                                                                                                                                        |
