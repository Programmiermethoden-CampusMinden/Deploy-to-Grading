---
title: Definition von Konfigurationsdateien für Aufgabenblatt- und Aufgabendefinition
---

Aus dem alten Konzept existiert eine task.json, in der die zu bewertenden Aufgaben aufgelistet sind. Ich bin der Meinung, dass wir auch nicht um eine solche Konfigurationsdatei herumkommen. Daher im folgenden mein Vorschlag.

Im folgenden unterscheide ich zwischen einer Definition für das Aufgabenblatt und für die einzelnen Aufgaben. Während die Aufgabenblattdefinition die Auswahl an Aufgaben und das Abgabedatum angibt, befindet sich in der Aufgabendefinition die eigentliche Konfiguration zum Testen und Bewerten.

*Alternative: Könnten uns an [ProFormA](https://github.com/ProFormA/proformaxml/blob/master/Whitepaper.md), [CodeFreak](https://docs.codefreak.org/codefreak/for-teachers/assignments.html#task-codefreak-yml) oder [PEML](https://cssplice.github.io/peml/) orientieren oder das sogar einhalten. Im zweiten Fall tun wir das schon zum Teil.*

### Format Aufgabenblattdefinition (assignment.yml)

```
name:                  # Name des Aufgabenblatts
description:           # (optional) Pfad zu einer README, falls man daraus mal richtige Aufgabenblätter generieren möchte oder direkt hier
due_date:              # Abgabetermin (Commits danach zählen nicht mehr) (Muss jedes Semester aktualisiert werden)
tasks:                 # Liste mit allen zu dem Aufgabenblatt gehörenden Aufgaben (Würde entfallen bei Zwischen-Repository)
    - (List)
```

*Notiz: Könnte das Abgabedatum auch aus der [schedule.yaml](https://github.com/Programmiermethoden/PM-Lecture/blob/master/data/schedule.yaml) aus PM-Lecture gelesen werden?*

### Format Aufgabendefinition (task.yml)

```
name:                  # Name der Aufgabe (nötig?)
description:           # (optional) Sollte immer zur README.md zeigen
metrics:                 # Liste an Tests, die für die Benotung ausgeführt werden sollen
    compile:
        # Individuelle Konfiguration des Tests (Unvollständige Auflistung)
        points:        # siehe [Strategie der Punktevergabe](#strategie-der-punktevergabe)
    junit:
        # Individuelle Konfiguration des Tests (Unvollständige Auflistung)
        points_per_test: # siehe [Strategie der Punktevergabe](#strategie-der-punktevergabe)
        depends_on: compile
    checkstyle:
        # Individuelle Konfiguration des Tests (Unvollständige Auflistung)
        max_points:    # siehe [Strategie der Punktevergabe](#strategie-der-punktevergabe)
        depends_on:    # Wird nur ausgeführt und gibt nur Punkte, wenn das genannte target bestanden wurde
no_override:           # Liste an Dateien, die nicht mit der Vorlage überschrieben werden dürfen
```

#### Strategie der Punktevergabe

Im Gegensatz zum [task.json-Vorschlag](https://github.com/Programmiermethoden/Deploy-to-Grading/blob/master/.config/task.json) könnte man die Punktevergabe für jeden Test einzeln lösen, um das Verhältnis auch justieren zu können.

|Vergabestrategie|Erläuterung|Anwendungsbeispiel|
|--|--|--|
|Alles oder nichts|Es werden nur alle Punkte vergeben oder keine Punkte. Dies findet z.B. Anwendung bei compile, wo es kein klappt nur zur Hälfte gibt.|compile|
|Punktabzug pro Fehler|Es wird eine Maximalpunktzahl für diesen Testtyp vergeben. Das bedeutet auch, dass man mehr Fehler haben kann, für die keine Punkte mehr abgezogen werden, wenn bereits 0 Punkte erreicht werden.|checkstyle|
|Eindeutige Punktevorgabe|Es werden die möglichen Punkte genau vorgegeben. Im Falle von junit bedeutet das, dass die Anzahl der definierten Tests die Punkteanzahl angibt. (Erweiterung: Anwenden (der Idee) von [JGrade](https://github.com/espertus/jgrade), dass bei jedem Test genau definiert ist, wie viele Punkte man für diesen erhalten kann.)|junit|
