---
title: JUnit-Metrik
---

Über die JUnit-Metrik können Java-Unittests ausgeführt und bewertet werden.
Dabei wird das Gradle `test`-Target ausgeführt. Die JUnit-Metrik kann verwendet
werden, ohne dass Anpassungen an den Tests notwendig sind. Dazu kann eine
Standardpunktzahl für einzelne Tests als auch eine Gesamtpunktzahl angegeben
werden. Mit Anpassungen am Java-Code der Tests ist es auch möglich, einzelnen
Tests individuelle Punktzahlen zu geben. Des Weiteren können über diese Metrik
CLI-Tests umgesetzt werden.

Mit dem folgenden YAML-Code kann die JUnit-Metrik einer Aufgabenstellung
hinzugefügt werden:

```yml
metrics:
- junit:
    default_points: 1
    overall_points: 10
```

- `default_points`: (optional) Gibt die standardmäßige Punktzahl eines
  einzelnen Tests an. Der Standardwert für `default_points` ist "1", wenn
  kein anderer Wert angegeben wurde.
- `overall_points`: (optional): Gibt die Gesamtpunktzahl an, die die
  JUnit-Metrik bei null Fehlern gibt. Fehlt diese Angabe, dann wird die über
  die Anzahl der Tests definierte Gesamtpunktzahl verwendet. Wenn über
  `overall_points` eine Punktzahl angegeben ist, so wird diese Punktzahl auf
  die gegebene Konfiguration umgerechnet. Achtung: Bei Verwendung dieser Option
  kann es vorkommen, dass durch falsche Unittests eine "krumme" Punktzahl von
  der Gesamtpunktzahl abgezogen wird.

Damit die JUnit-Metrik ausgeführt werden kann, muss der `test`-Task in der
`build.gradle`-Datei korrekt konfiguriert sein. Der Pfad zum Speichern der
Ergebnisse im XML-Format muss dabei `build/results/junit/xml` sein. Im
folgenden ist eine Beispielkonfiguration angegeben:

```gradle
dependencies {
    testImplementation 'junit:junit:4.13.2'
}

test {
    useJUnit()
    reports.junitXml.outputLocation = file("build/results/junit/xml")
}
```

### Alternative Punktzahlen für einzelne Tests

Einzelne Tests können alternativ zu der Standardpunktzahl eine eigene Punktzahl
definieren. Dazu wird die zu vergebende Punktzahl am Ende des Namens der
Testmethode definiert. Die Zahl wird dabei mit einem Unterstrich vom
eigentlichen Namen. Am Ende der Punktzahl steht ein `P` oder `p`. Es ist nicht
möglich, Kommazahlen anzugeben.

```java
    @Test
    public void testDummyTest_2p() {
        assertEquals(5, 2+3);
    }
```

### Umsetzung von CLI-Tests

CLI-Tests zum Prüfen der Konsolenausgabe werden auch über JUnit umgesetzt. In
einer zusätzlichen Testklasse wird dafür vor jedem Test `System.out` auf einen
neuen OutputStream gesetzt, der leicht ausgelesen werden kann. In den
jeweiligen Testmethoden können wir dann die `main()`-Methode ausführen. Über
den OutputStream wird die Ausgabe des Programms ausgelesen.

```java
// Der Übersichtlichkeit halber wird für CLI-Tests eine eigene Testklasse
// genutzt.
public class CliTest {

    // In einem OutputStream werden die Konsolenausgaben gespeichert.
    private ByteArrayOutputStream outStream;

    @Before
    public void before() {
        // Vor jedem Test setzen wir einen neuen OutputStream für System.out.
        outStream = new ByteArrayOutputStream();
        System.setOut(new PrintStream(outStream));
    }

    @Test
    public void testMessagePrintCorrect() {
        // Im eigentlichen Test führen wir dann die main-Methode aus.
        // Hier können wir u.A. auch `args` setzen.
        Main.main(new String[]{});
        // Über outStream.toString() können wir die Ausgabe erhalten.
        assertEquals("Hello World!\n", outStream.toString());
    }

    @After
    public void after()  {
        // Und nach dem Test setzen wir auf den Default stdout Stream zurück.
        System.setOut(new PrintStream(
            new FileOutputStream(FileDescriptor.out)));
    }
}
```
