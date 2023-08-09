---
title: Codeformat-Metrik
---

Über die Codeformat-Metrik kann geprüft werden, ob der Code korrekt formatiert ist. Dazu wird das Gradle `spotlessJavaCheck`-Target ausgeführt. Über den Rückgabewert wird ermittelt, ob der Code korrekt formatiert ist. Bei einer korrekten Formatierung wird eine über die Konfiguration definierte Punktzahl vergeben.

Mit dem folgenden YAML-Code kann die Codeformat-Metrik einer Aufgabenstellung
hinzugefügt werden:

```yml
metrics:
- codeformat:
    points: 2
```

- `points`: Gibt die Anzahl der zu vergebenden Punkte bei erfolgreicher
  Ausführung an.

Damit die Codeformat-Metrik ausgeführt werden kann, muss der
`spotlessJavaCheck`-Task in der `build.gradle`-Datei korrekt konfiguriert sein.
Im folgenden ist eine Beispielkonfiguration angegeben:

```gradle
plugins {
    id 'com.diffplug.spotless' version '6.+'
}

spotless {
    java {
        googleJavaFormat().aosp().reflowLongStrings()
    }
}
```
