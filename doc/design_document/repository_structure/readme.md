---
title: Aufbau der D2G-Repositorys
---

*Anmerkung: Basierend auf [Kommentar von @AMatutat](https://github.com/Programmiermethoden/Dungeon/issues/434#issuecomment-1532679532).*

![Repository Struktur](https://user-images.githubusercontent.com/32961997/236833681-507dac5b-7414-4c8c-a7f3-a4403e7c594e.png)

*Anmerkung: Die Namen der Repositories sind nicht final.*

*Notiz: Für Informationen zu git filter-repo siehe [hier](https://www.mankier.com/1/git-filter-repo).*

| Repository       | Erläuterung                                                                                                                                                                                         |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| D2A              | Enthält die GitHub Action, die über den Workflow ab dem Template-Repository in jedes darunter liegende Repository eingebunden wird.                                                                 |
| Template         | Enthält die Vorlagen für alle Aufgaben.                                                                                                                                                             |
| Tasks            | (Optional) Enthält die Vorlagen für ausschließlich die Aufgaben, die die Studierenden bearbeiten sollen.                                                                                            |
| StudiSolution    | Lösungen der Studierenden zu den Aufgaben.                                                                                                                                                          |
| HomeworkSolution | (Option 1): Die Lösungen werden wie bisher im gleichen Repository gesammelt wie die Vorlagen. Das Template-Repository ist ein über Subtree erstelltes Repository, welches nur die Vorlagen enthält. |
| SampleSolution   | (Option 2): Enthält wie Option 1 die Lösungen zu den Vorlagen. Verhält sich im Gegensatz dazu aber wie StudiSolution.                                                                               |

*Hinweis: Es soll Option 1 umgesetzt werden.*

**Gegenüberstellung HomeworkSolution vs SampleSolution**

| HomeworkSolution                                                                                                                                                  | SampleSolution                                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| - Neue Aufgaben können in ein und demselben Repository erstellt werden (Keine Arbeit in zwei Repositories gleichzeitig oder Rüberkopieren von Dateien notwendig). | - Entspricht dem Workflow der Studierenden.                                                                                                 |
| - Kein doppelter Vorlagen-Code in zwei unterschiedlichen Repositories.                                                                                            | - Erlaubt das Testen durch D2A, ohne eine Unterscheidung zu StudiSolution machen zu müssen.                                                 |
| - Bereits Pull-Request mit dieser Lösung vorhanden.                                                                                                               | - Ermöglicht das Arbeiten in den Vorgaben (größerer möglicher Aufgabenpool).                                                                |
|                                                                                                                                                                   | - Keine unterschiedlichen Build-Skripte und kein Ändern der Gradle-Konfiguration durch Source-Code, der an unterschiedlichen Stellen liegt. |

*Zusammenfassung:* Der Ansatz *SampleSolution* erscheint mir deutlich simpler und ermöglicht zusätzliche Aufgabentypen und Testmöglichkeiten. *HomeworkSolution* vereinfacht dagegen die Erstellung von neuen Aufgaben und wir haben bereits einen PR dazu.

**Erläuterung Task-Repository**

Studierenden wird pro Praktikumseinheit eine ausgewählte Liste an Aufgaben gestellt. Da im Template-Repository aber alle Vorlagen vorhanden sind, wird ein "Zwischenrepository" benötigt, welches Aufgaben zu Praktikumseinheiten zuordnet, die an Studierende verteilt werden. *Möglicher Aufbau des Repos: Zum Beispiel pro Praktikumseinheit ein Branch oder Aktualisieren bei jedem Aufgabenbeginn oder Praktikumseinheiten aufgeteilt in Unterordner.*

*Anmerkung: Die Erläuterung basiert darauf, dass ich nicht weiß, wie die Aufgaben vorher an Studierende gegeben wurden.*

*Anmerkung 2: @AMatutat hat mir mittlerweile gesagt, dass ihr im letzten Semester den Studis alle Aufgaben auf einmal zur Verfügung gestellt habt.*

## Inhaltsverzeichnis

1. [Dateistruktur von Aufgaben](file_structure.md)
2. [Definition von Konfigurationsdateien für Aufgabenblatt- und Aufgabendefinition](file_structure.md)
