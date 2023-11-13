---
title: Verwandte Arbeiten
---

## Einordnung von D2G ins Forschungs-/Entwicklungsgebiet automatischer Bewertungstools

### Nach [Arnold Pears](https://researchonline.gcu.ac.uk/en/publications/a-survey-of-literature-on-the-teaching-of-introductory-programmin)

| System                                                                   | Einordnung                                                                                                                                                                                   |
| ------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Visualisierungstool                                                      | Da Studierende bereits vor der endgültigen Abgabe automatischen Feedback erhalten sollen, wird eine Darstellung der Testergebnisse benötigt. Minimum als Textausgabe in dem GitHub Workflow. |
| Automatisches Bewertungstool                                             | Primäre Einordnung in dieses System. D2G soll die auf GitHub erstellen Pull Requests bewerten und eine entsprechende Punktzahl generieren.                                                   |
| Programmierumgebung                                                      | Nicht passend. Studierende programmieren in ihrer gewählten IDE.                                                                                                                             |
| Andere Tools (z.B. Plagiatserkennung oder intelligente Tutoring-Systeme) | Plagiatserkennung: Sinnvoll einzusetzen erst bei der endgültigen Abgabe vom Lehrenden, da erst hier alle Abgaben in einem gemeinsamen geschützten Workspace vorliegen.                       |

### Nach [Petri Ihantola](https://www.researchgate.net/publication/216714976_Review_of_recent_systems_for_automatic_assessment_of_programming_assignments)

| Feature                                    | Einordnung                                                                                                                                                                                                                                          |
| ------------------------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unterstützte Programmiersprachen           | Es soll nur die Programmiersprache Java unterstützt werden.                                                                                                                                                                                         |
| Integration in Learning-Management-Systeme | Eine Anbindung an ILIAS ist bisher nicht geplant.                                                                                                                                                                                                   |
| Definition von Tests                       | Die genaue Auswahl an Testmetriken wird in Kapitel [Test Metriken](#test-metriken) beschrieben.                                                                                                                                                     |
| Erneute Einreichung von Lösungen           | Studierende erhalten die Möglichkeit, ihre Lösung bis zur finalen Abgabe abzuändern und neu prüfen zu können.                                                                                                                                       |
| Möglichkeiten einer manuellen Bewertung    | Die Prüfung, bei der Studierende eine erste Rückmeldung erhalten, soll vollständig automatisch passieren. Erst bei der endgültigen Prüfung wären nachträglich manuelle Änderungen möglichen. Dort ist die Frage der Rückmeldung aber nicht geklärt. |
| Sandboxing (Sicherheit)                    | Die Tests werden in von GitHub zur Verfügung gestellten Runnern durchgeführt.                                                                                                                                                                       |
| Verbreitung und Verfügbarkeit              | Bisher nicht diskutiert. Sollte aber problemlos möglich sein.                                                                                                                                                                                       |
| Spezielle/einmalige Funktionen             | Bisher keine speziellen Metriken zum Testen von z.B. grafischen Benutzeroberflächen, SQL-Abfragen, nebenläufiger Programmierung oder Webprogrammierung geplant.                                                                                     |

### Nach [Thomas Staubitz](https://ieeexplore.ieee.org/document/7386010)

| Scenario                                                                                                                                                                                                                                                    | Einordnung                                                                                                                                                                                                                             |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The user installs some sort of development software locally. The platform only provides the description of the exercise and, if necessary, required additional materials. The user in return uploads her solution to the platform for automated assessment. | Hier zutreffend: Studierende arbeiten in ihrer gewählten Entwicklungsumgebung. Der einzige Unterschied zu anderen Assessment Tools dieser Kategorie ist, dass keine eigene Online-Plattform benötigt wird, da alles über GitHub läuft. |
| Instead of using locally installed development software, third party online coding tools are employed. Apart from that, scenario 2 is identical to scenario 1.                                                                                              | Könnte auch zutreffen, wenn sich Studierende für ein Online Tool entscheiden, z.B. [GitHub Codespaces](https://github.com/features/codespaces).                                                                                        |
| The platform itself features a development environment. Exercises are provided and assessed in this environment. Code execution and assessment is handled on the server side.                                                                               | Nicht zutreffend.                                                                                                                                                                                                                      |
| Identical to scenario 3 except for client-side code execution.                                                                                                                                                                                              | Nicht zutreffend.                                                                                                                                                                                                                      |

### Abgrenzung von anderen AutoGradern

Durch die folgenden Punkte können wir uns von anderen AutoGradern abgrenzen:

* Integration von Git in den Arbeits-Workflow
* Serverseitige Evaluation der Abgaben ohne eigene Serverstruktur
* Gedacht für die fortgeschrittene Programmierausbildung
  * Erfordert Kenntnisse über Git und die Arbeit mit IDEs
* Vorteile von IDEs nutzbar machen gegenüber Texteingabefelder auf einer Webseite
* Wegen des Git-Workflows können wir kein ProFormA 2.0 verwenden
  * Das ist eher eine Einschränkung als Abgrenzung. Aber im Hinblick auf ABP 2023 relevant

## Inhaltsverzeichnis

1. [Konferenzliste](https://github.com/Programmiermethoden/Dungeon/blob/master/doc/related_work/conferences.md)
2. [Automatische Bewertungssysteme](autograder/readme.md)
3. [Nicht kategorisierte Paper](paper/readme.md)
4. [Bücher](book/readme.md)
5. [Aufgabendefinitionsdateien](task_definition_files/readme.md)
