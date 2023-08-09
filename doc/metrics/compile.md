---
title: Compile-Metrik
---

Die Compile-Metrik überprüft, ob der Programmcode fehlerfrei kompiliert werden
kann und vergibt bei korrekter Ausführung eine eindeutig vorgegebene Punktzahl.
Die Kompilierung wird über Gradle die Kompilierung durchgeführt. Dazu muss im
Gradle-Projekt die `compileJava`-Task definiert sein. Über den Rückgabewert
wird ermittelt, ob das Kompilieren erfolgreich war.

Mit dem folgenden YAML-Code kann die Compile-Metrik einer Aufgabenstellung
hinzugefügt werden:

```yml
metrics:
- compile:
    points: 1
```

- `points`: Gibt die Anzahl der zu vergebenden Punkte bei erfolgreicher
  Ausführung an.
