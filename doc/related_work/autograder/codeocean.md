---
title: CodeOcean
url: https://github.com/openHPI/codeocean
---

## Bibtex

```
@inproceedings{codeocean,
  author    = {Thomas Staubitz and Hauke Klement and Ralf Teusner and Jan Renz and Christoph Meinel},
  booktitle = {IEEE Global Engineering Education Conference},
  title     = {CodeOcean - A versatile platform for practical programming excercises in online environments},
  year      = {2016},
  pages     = {314-323},
  doi       = {10.1109/EDUCON.2016.7474573}
}
```

## Zusammenfassung

CodeOcean ist eine pädagogische, webbasierte Ausführungs- und Entwicklungsumgebung für praktische Programmierübungen, die für den Einsatz in Massive Open Online Courses (MOOCs) konzipiert wurde.

Die auf openHPI angebotenen Programmierkurse beinhalten praktische Programmierübungen, die auf einer webbasierten Code-Ausführungsplattform namens CodeOcean bereitgestellt werden. Die Plattform hat viele Vorteile für Lernende und Lehrende gleichermaßen:

1. CodeOcean bietet eine vordefinierte Ansicht auf die Übungen mit gerüsteten Quelltexten inklusive Syntax-Highlighting und ermöglicht die Bearbeitung dieser Dateien direkt im Browser.
2. Die Plattform ermöglicht die Ausführung des Codes auf dem Server und streamt die Ausgabe zurück in den Webbrowser des Lernenden. Zusammen mit der benutzerdefinierten Ansicht werden die Lernenden dabei unterstützt, in kürzester Zeit mit der Programmierung zu beginnen, ohne sich um die Entwicklungsumgebung kümmern zu müssen. Die Lernenden müssen weder einen Compiler noch eine Laufzeitumgebung herunterladen und installieren. So minimieren MOOC-Dozenten technische Hilfeanfragen zur korrekten Einrichtung des Rechners und können sich in Forenbeiträgen auf die im Kurs vermittelten Inhalte konzentrieren.
3.CodeOcean beinhaltet Unit-Tests, um den Lernenden Feedback zu geben und ihren Code zu bewerten. Ein Unit-Test ist definiert als ein Programm, das entweder den Code des Lernenden auf eine vordefinierte Art und Weise ausführt und das Ergebnis mit einer Erwartung vergleicht, oder der Unit-Test analysiert den Quellcode des Lernenden und vergleicht ihn mit einer als Übung definierten Zeichenfolge. Während der Code der Unit-Tests verborgen ist, können die Lernenden die Unit-Tests jederzeit ausführen und erhalten sofort eine Rückmeldung, ob sie bestanden haben oder nicht. Wenn die Unit-Tests fehlschlagen, wird das Ergebnis zusammen mit einer von den MOOC-Dozenten definierten Fehlermeldung angezeigt. Einerseits hilft dieses Feedback den Lernenden, sich selbst zu helfen und gibt ihnen einen Hinweis auf ihren Fehler. Andererseits ist die automatisierte Bewertung durch Unit-Tests notwendig, um den Lernenden den Fortschritt anzuzeigen. Im Rahmen eines MOOCs mit Tausenden von aktiven Lernenden ist eine manuelle Überprüfung durch die Dozenten nicht möglich und ein Peer-Review des Quellcodes wurde in CodeOcean bisher nicht implementiert.
4. In CodeOcean können die Lernenden Fragen zu ihrem Programm direkt auf der Plattform und im Zusammenhang mit ihrem aktuellen Programm stellen. Normalerweise bieten MOOC-Plattformen ein Forum, um Fragen zu diskutieren. Während dieses Konzept auch für Quellcode im Allgemeinen außerhalb eines MOOCs gut funktioniert (vgl. StackOverflow), stellt es für Anfänger eine zusätzliche Barriere dar, ihr Problem extern zusammenzufassen. Um das Problem zu verstehen, sind kontextuelle Informationen in der Regel hilfreich für andere, um die aktuelle Lösung zu liefern. Bei der Nutzung eines speziellen Forums müssen die Lernenden so viele Informationen wie nötig angeben, um das Problem zu reproduzieren, was Anfängern unter Umständen schwerfällt. Infolgedessen könnten sie zu wenige oder zu viele Informationen kopieren. Darüber hinaus zeigte sich in den ersten Iterationen der Java-Kurse, dass die Lernenden ihren Quellcode in den Forenbeiträgen nicht angemessen formatierten (sondern als reinen Text), was das Lesen erschwerte. Mit Request for Comments bietet CodeOcean eine eingebaute Funktion, um im Rahmen einer Übung eine Frage zu stellen und so die Hürde zu senken, Hilfe zu erhalten. CodeOcean präsentiert den Quellcode und die Fehlermeldung des Lernenden zusammen mit der Frage den Kommilitonen und erlaubt ihnen, einen Kommentar speziell zu einer Codezeile hinzuzufügen. So wird das zuvor beschriebene Problem mit einem eigenen Forum gelöst.

CodeOcean wird vor allem im Rahmen von MOOCs (wie z.B. bei openHPI und mooc.house) eingesetzt und wurde bis Juni 2020 von mehr als 60.000 Nutzern verwendet. CodeOcean ist ein eigenständiges Tool, das den Standard Learning Tools Interoperability (LTI) implementiert und in verschiedenen Lernszenarien eingesetzt werden kann. Durch das Angebot einer LTI-Schnittstelle ist es sowohl von MOOC-Anbietern als auch von anderen Anbietern wie der HPI Schul-Cloud zugänglich. CodeOcean selbst kann nicht direkt von Lernenden oder anderen Nutzern als den MOOC-Dozenten oder Administratoren verwendet werden.

*Quelle: https://github.com/openHPI/codeocean, 16.06.23 (Übersetzt mit DeepL)*
