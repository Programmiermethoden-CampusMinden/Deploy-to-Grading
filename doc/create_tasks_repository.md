---
title: Aufgabenrepository erstellen
---

Ein Aufgabenrepository ist ein Git-Repository, welches den Studierenden von den Lehrenden zur Verfügung gestellt wird und welches die Aufgaben enthält, die die Studierenden innerhalb einer Abgabefrist bearbeiten sollen. Die Studierenden sollen ein Fork dieses Repositorys erstellen und ihre Lösungen auf einem separatem Branch hochladen. Anschließend sollen die Studierenden einen Pull-Request gegem ihren Fork stellen, dessen URL im LMS abgegeben werden soll. Die Deploy-to-Grading-Pipeline wird automatisch ausgeführt, wenn ein neuer Commit dem Pull Request hinzugefügt wird.

Um ein Aufgabenrepository mit Aufgaben zu befüllen und zu konfigurieren, müssen die folgenden Schritte ausgeführt werden:

1. Aufgaben hinzufügen
2. Aufgabenkonfiguration erstellen
3. Deploy-to-Grading-Pipeline als GH Workflow hinzufügen

### 1. Aufgaben hinzufügen

Als Basis für eine neue Java-Aufgabe kann das `empty`-Beispiel aus dem [Demo-Repository](https://github.com/Programmiermethoden/D2G-Aufgaben-Demo) übernommen werden. Das Beispiel enthält alle benötigten Dateien und muss nur noch auf eine konkrete Aufgabenstellung angepasst werden. Dazu müssen die folgenden Änderungen vorgenommen werden:

1. Hinzufügen von Vorgabe-Code im `src`-Ordner. Vorgabe-Dateien müssen dabei in `src/main/java` abgelegt werden, wohingegen Unittests im Ordner `src/test/java` hinzugefügt werden müssen.
2. Aktualisieren der `task.yml`, in der der Name der Aufgabenstellung und eine kurze Beschreibung der Aufgabe hinzugefügt werden müssen. Unter dem Punkte `no_override` können Dateien angegeben werden, die bei der Prüfung auf unerlaubte Änderungen ignoriert werden sollen. Dies ist insbesondere dann wichtig, wenn Studierende Änderungen in Vorgabedateien machen sollen. Für die Konfiguration der einzelnen Metriken sei auf dessen [Dokumentation](metrics/readme.md) verwiesen.
3. (Optional) Hinzufügen einer `readme.md`. Für eine detaillierte Beschreibung der Aufgabenstellung kann optional eine README-Datei hinzugefügt werden.

### 2. Aufgabenkonfiguration erstellen

Nachdem die einzelnen Aufgaben hinzugefügt wurden, müssen diese über eine Konfiguration zu einem "Aufgabenblatt" zusammengefügt werden. Dazu muss eine Datei `assignment.yml` mit dem folgenden Inhalt erstellt werden:

```yml
name: Demo Aufgabenblatt
description: Dies ist eine Beispielkonfiguration für ein Aufgabenblatt.
template_repository: https://github.com/Programmiermethoden/D2G-Aufgaben-Demo
due_date: 2025-01-01T00:00
tasks:
- empty
```

Die Konfiguration kann anschließend noch angepasst werden. Dabei stehen die Einstellungsmöglichkeiten für folgendes;

- `name`: Name des Aufgabenblatts
- `description`: Kurzbeschreibung des Aufgabenblatts. Optional kann auch hier dem Repository eine `README.md` hinzugefügt werden.
- `template_repository`: URL des aktuellen Repositorys.
- `due_date`: Abgabedatum des Aufgabenblatts.
- `tasks`: Liste an Aufgaben innerhalb des Repositorys, die evaluiert werden sollen. Die hier aufgezählten Namen müssen mit den Ordnernamen der einzelnen Aufgaben übereinstimmen.

### 3. Deploy-to-Grading-Pipeline als GH Workflow hinzufügen

Um abschließend die Deploy-to-Grading-Pipeline in das Repository einzubinden, muss die Datei `.github/workflows/d2g.yml` erstellt und mit dem folgenden Inhalt befüllt werden:

```yml
name: Deploy-to-Grading
on:
  pull_request:
  workflow_dispatch:
  
jobs:
  deploy-to-grading:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: akirsch1/deploy-to-grading@master
```

Damit wird die Deploy-to-Grading-Pipeline immer bei neuen Änderungen eines Pull Requests ausgeführt, sie kann aber auch manuell gestartet werden.
