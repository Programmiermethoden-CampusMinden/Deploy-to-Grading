---
title: Erstellen einer eigenen Metrik
---

Das Erstellen eigener Metriken teilt sich auf zwei Dateien auf, welche für die neue Metrik erstellt werden müssen. Die erste Datei ist ein Bash-Skript mit dem Namen `{metric}.sh`, wobei `{metric}` mit dem Namen der Metrik zu ersetzen ist. Dieser Name wird in der `task.yml` einer Aufgabenstellung dafür genutzt, um die Metrik zu benennen. Die Datei `{metric}.sh` wird dafür genutzt, die Metrik auszuführen. Im Falle der `compile`-Metrik wird in dem dazugehörigen Skript zum Beispiel das `compileJava`-Target der Gradle-Konfiguration ausgeführt und das Ergebnis in eine Datei gespeichert. Die zweite Datei ist ein Python-Skript mit dem Namen `{metric}_eval.py`. Dieses wertet das Ergebnis der Metrik aus und formatiert es für die Weiterverarbeitung in der Deploy-to-Grading-Pipeline. Beide Dateien müssen im Pfad `scripts/metrics/` liegen.

### Erstellen der `{metric}.sh`

Die Datei `{metric}.sh` ist in der Regel ein kurzes Skript, welches im Falle von Java ein Gradle-Target startet. Falls das Gradle-Target nicht automatisch die Ergebnisse in eine Datei exportiert, müssen diese von diesem Skript exportiert werden. Die Ergebnisse müssen dabei im Pfad `build/results/` gespeichert werden.

### Erstellen der `{metric}_eval.py`

Die Datei `{metric}_eval.py` ist verantwortlich für das Auswerten der Ergebnisse. Diese Evaluationsskripte werden ausgeführt, nachdem alle Metriken ausgeführt wurden. Die Hauptaufgabe besteht darin, die Ausgaben der Metriken in ein für die D2G-Pipeline verständliches und einheitliches Format zu bringen, welches bereits eine Bepunktung/Benotung enthält.

Der grundlegende Ablauf des Evaluationsskripts ist folgender:
1. Laden der Ergebnisse der Metrik aus `build/results/`
2. Auswerten der Ergebnisse und Umwandeln in das einheitliche Format
3. Ausgeben der Ergebnisse im einheitlichen Format

#### 1. Laden der Ergebnisse

Für das Laden von Ergebnissen werden in `scripts/metrics/metric_utils.py` Funktionen bereitgestellt. Mit diesen Funktionen können YAML- und XML-Dateien geladen werden. Für genauere Informationen, siehe die zur Datei gehörende Source-Code-Dokumentation.

#### 2. Auswerten der Ergebnisse

Zum Auswerten werden in `scripts/metrics/metric_utils.py` die Funktion `create_mistake` und Varianten der Funktion `generate_final_results*` zur Verfügung gestellt. Diese können genutzt werden, um die Ergebnisse in das korrekte Format umzuwandeln. Für die detaillierte Dokumentation der Funktionen, siehe die zur Datei gehörende Source-Code-Dokumentation.

#### 3. Ausgeben der Ergebnisse

Das von der aufgerufenen `generate_final_results*`-Funktion zurückgegebene `results`-Objekt muss zuletzt mit der `print_results(results)`-Funktion für die Weiterverarbeitung in der D2G-Pipeline ausgeben werden.

### Konfiguration der Metrik

Eine Metrik wird in der Datei `task.yml` einer Aufgabenstellung zur Evaluation der Aufgabe hinzugefügt und konfiguriert. Über `metric.utils.get_env_variable(key, taskname, USAGE_TEXT)` kann auf eine Konfigurationseinstellung zugegriffen werden. Der Schlüssel der Konfigurationseinstellung hat dabei immer das Muster `{taskname}_METRICS_{metric}_{setting}`, wobei `taskname` der Name der Aufgabe und `metric` der Name der Metrik ist. `setting` ist der Name der Einstellung in der `task.yml`-Datei. Der `key` muss dabei vollständig in Caps-lock geschrieben werden.
