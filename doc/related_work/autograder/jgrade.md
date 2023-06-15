---
title: JGrade
url: https://github.com/espertus/jgrade
---

JGrade ist ein Plugin für Gradescope Autograders, kann aber auch unabhängig davon genutzt werden. Seit drei Jahren wird das Original-Repo nicht mehr fortgeführt.

Grundsätzlich ist JGrade zum Benoten von Java-Code gedacht und nutzt dafür primär JUnit-Tests, die alle eine unterschiedliche Anzahl an Punkten geben können. Zusätzlich wird noch Checkstyle genutzt und es bietet eine Schnittstelle für CLI-Tests. @cagix Gibt es/Stellt ihr Aufgaben, in denen Studierende CLI-Anwendungen programmieren müssen?

Die Ausgabe der Ergebnisse ist entweder im JSON-Format oder für Gradescope Autograders möglich.

Unabhängig von JGrade selbst gibt es in dem oben verlinkten Repo, in dem das Projekt fortgeführt wird, ein [YT-Video](https://www.youtube.com/watch?v=o1FHbHZwyUY), in dem deren Umsetzung der Bewertung und Aufbau der Ordnerstruktur beschrieben wird:

Erstmal vorweg, wirklich optimal finde ich die nicht. Folgendermaßen ist die Ordnerstruktur aufgebaut:
```
src/main/java
-- staff                        Sammelordner für irgendwie alles, was nicht von Studierenden kommt
-- -- hello                             
-- -- -- GradeHello.java        JGrade-spezifische Klasse, die die Tests anstößt
-- -- -- Greeting.java          Interface, das von beiden Hello-Klassen implementiert wird
-- -- -- Hello.java             Beispielimplementierung/Lösung
-- -- -- HelloTest.java         Klasse mit Tests im JGrade-Format (siehe Anmerkung 1)
-- student
-- -- hello
-- -- -- Hello.java             Lösung von Studis. Ist bei denen schon vorhanden (mit TODOS)
```
*Anmerkung 1: Nutzen hier einen bool, um zwischen Grading der Beispiellösung und der Studierendenlösung zu wechseln.*

Des Weiteren interessant ist in dem Video, wie "Log"-Tests durchgeführt werden. So wird über `System.setOut` ein anderer Out-Stream gesetzt. Damit könnte man zum Beispiel [dieses hier](https://github.com/Programmiermethoden/Homework-Solutions/blob/f683ed6d94c3d1a344c4f3bf8af9ae96b15425b5/type_object_pattern/loesung/src/MonsterTest.java) gut testen.
