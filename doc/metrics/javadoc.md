---
title: JavaDoc-Metrik
---

Die JavaDoc-Metrik nutzt intern Checkstyle, um die korrekte Verwendung von JavaDoc zu prüfen. Dabei wird das Gradle `checkstyleMain`-Target ausgeführt. Über den Rückgabewert wird ermittelt, ob der Code korrekt formatiert ist. Bei einer korrekten Formatierung wird eine über die Konfiguration definierte Punktzahl vergeben. Dabei werden von einem vorgebenen Maximalwert für die Punkte je nach Anzahl der Fehler Punkte abgezogen. Bei der Konfiguration kann zwischen zwei verschiedenen Vergabevarianten gewählt werden. Zum einen kann für jeden Fehler ein Punkt abgezogen werden. Die zweite Variante erlaubt das Gruppieren der Fehlertypen und zieht nur beim ersten Auftauchen eines Fehlertypens einen Punkt ab.

Mit dem folgenden YAML-Code kann die Codeformat-Metrik einer Aufgabenstellung
hinzugefügt werden:

```yml
metrics:
- javadoc:
    max_points: 10
    deduction_per_error: 1
    group_errors: false
```

- `max_points`: Gibt die maximal erreichbare Punktzahl für diese Metrik an.
- `deduction_per_error`: Gibt die Anzahl an Punkten, die pro Fehler abgezogen werden, an.
- `group_errors`: Wählt zwischen den zwei Varianten für das Abziehen von Punkten bei Fehlern. Ist der Wert auf `true` gesetzt, dann werden pro Fehlertyp maximal ein mal Punkte abgezogen. Ansonsten werden für jeden Fehler die Punkte abgezogen.

Damit die JavaDoc-Metrik ausgeführt werden kann, muss der
`checkstyleMain`-Task in der `build.gradle`-Datei korrekt konfiguriert sein.
Im folgenden ist eine Beispielkonfiguration angegeben:

```gradle
plugins {
    id 'checkstyle'
}

checkstyle {
    toolVersion = "10.2"
    configFile = file(".config/checkstyle/javadoc.xml")
    reportsDir = file("build/results/javadoc")
}

tasks.withType(Checkstyle) {
    reports {
        xml.required = true
        html.required = false
    }
}
```

Des Weiteren muss im Projektpfad unter `.config/checkstyle/javadoc.xml` eine Konfiguration für Checkstyle vorhanden sein. Die folgende Beispielkonfiguration prüft alle für JavaDoc relevanten Angaben:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE module PUBLIC "-//Checkstyle//DTD Checkstyle Configuration 1.3//EN"
    "https://checkstyle.org/dtds/configuration_1_3.dtd">

<module name="Checker">
    <property name="severity" value="warning"/>

    <module name="TreeWalker">
        <module name="AtclauseOrder"/>
        <module name="InvalidJavadocPosition"/>
        <module name="JavadocBlockTagLocation"/>
        <module name="JavadocContentLocation"/>
        <module name="JavadocMethod"/>
        <module name="JavadocMissingLeadingAsterisk"/>
        <module name="JavadocMissingWhitespaceAfterAsterisk"/>
        <module name="JavadocParagraph"/>
        <module name="JavadocStyle"/>
        <module name="JavadocTagContinuationIndentation"/>
        <module name="JavadocType"/>
        <module name="JavadocVariable">
            <property name="scope" value="public"/>
        </module>
        <module name="MissingDeprecated"/>
        <module name="MissingJavadocMethod"/>
        <module name="MissingJavadocType"/>
        <module name="MissingOverride"/>
        <module name="RequireEmptyLineBeforeBlockTagGroup"/>
    </module>
</module>
```
