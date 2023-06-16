---
title: Dateistruktur von Aufgaben
---

Jede Aufgabe stellt ein eigenes vollständiges Java-Projekt mit folgendem Aufbau dar:

```
taskX/
|__.config/
|  |__task.yml            # Konfiguration der Aufgabe für D2A
|  |__checkstyle.xml
|  |__(Sonstige Konfigurationen)
|__.editorconfig
|__gradle/wrapper         # Wenn nicht anderweitig auslagerbar
|__src/
|____task/
|____test/
|__README.md              # Aufgabenstellung
|__build.gradle
|__(Restliche Gradle-Dateien)
```

Das Vorgaben-Repo enthält dann auf obersten Ebene die taskX-Ordner.

*Anmerkung: Zur genauen Definition der task.yml siehe [hier](task_and_assignment_structure.md).*
*Anmerkung: Es sollte noch geprüft werden, ob Gradle-Standardsachen aus den Aufgaben ausgelagert werden können.*

*Hinweis: Es sollte geprüft werden, ob es möglich ist, den `gradle/wrapper`-Teil auszulagern.*
