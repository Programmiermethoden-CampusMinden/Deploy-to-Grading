---
title: Deploy-to-Grading Dokumentation
---

Deploy-to-Grading (D2G) ist eine Toolchain zur automatischen Analyse und Bewertung von Programmieraufgaben. Im Gegensatz zu anderen populären Lösungen nutzt es frei verfügbare Rechenkapazität (GitHub Runner) und basiert auf Git. Aktuell sind nur Tools zur Bewertung von Java-Programmieraufgaben implementiert.

## Lokale Ausführung

D2G kann lokal auf jedem Linux Betriebssystem ausgeführt werden, auf dem Bash und Python 3 zur Verfügung stehen. Um D2G auszuführen, muss sichergestellt werden, dass man sich in einem Ordner befindet, der eine `assignment.yml`-Datei enthält. Des Weiteren muss die `D2G_PATH`-Umgebungsvariable einen Pfad zum Hauptverzeichnis des geklonten D2G-Repositorys enthalten. Dazu muss der Befehl `export D2G_PATH=/home/{USER}/Deploy-to-Grading` ausgeführt werden. Sollte das D2G-Repository nicht im `Home`-Verzeichnis des Nutzers liegen, muss der Pfad entsprechend angepasst werden. Zum Ausführen des Deploy-to-Grading muss der folgende Befehl ausgeführt werden:

```bash
$D2G_PATH/scripts/deploy_to_grading.py
```

## Ausführung als CI/CD-Pipeline

D2G kann auch als GitHub Workflow in ein Repository eingebunden werden, damit sie automatisch ausgeführt wird. Dazu muss der [Anleitung zum Erstellen eines Aufgabenrepositorys](create_tasks_repository.md) gefolgt werden.

## Inhaltsverzeichnis

1. [Skripte für Lehrende](teacher_scripts.md)
2. [Aufgabenrepository erstellen](create_tasks_repository.md)
3. [Metriken](metrics/readme.md)
4. [Related Work](related_work/readme.md)
5. [Design Dokument](design_document/readme.md)
