---
title: Code FREAK
url: https://github.com/codefreak/codefreak
---

## Bibtex

```
@misc{codefreak,
  author        = {Henning Kasch and Erik Hofer and Hannes Olszewski},
  title         = {Code FREAK},
  year          = {2018},
  howpublished  = {https://github.com/codefreak/codefreak},
  note          = {[Letzter Zugriff: 16.06.2023]}
}

@article{woelk2021,
  author       = {Woelk, Felix and
                  Kasch, Henning},
  title        = {{Code FREAK: Automatisches Feedback für die
                   Programmierausbildung}},
  journal      = {Die neue Hochschule},
  year         = 2021,
  number       = {2021-5},
  pages        = {28-31},
  month        = oct,
  doi          = {10.5281/zenodo.5530450},
  url          = {https://doi.org/10.5281/zenodo.5530450}
}
```

*Anmerkung: Die angegebenen Autoren sind die drei Personen, die den Großteil der Commits im Repository haben.*

## Zusammenfassung

Code FREAK ist eine Online Plattform, auf der Studierenden Aufgaben gestellt werden können, die direkt auf der Online-Plattform bearbeitet und evaluiert werden. Die Plattform gibt KEINE finale Note aus.

Die Dokumentation bleibt sehr wage, womit Code FREAK alles verwendet werden kann, da es sehr offen gestaltet ist. Im Grunde stößt es Tools wie JUnit über Docker an und stellt dessen Ergebnisse schön formatiert dar. Als Beispiele, welche Tools genutzt werden können, werden JUnit, Checkstyle, pytest und pylint genannt. Verallgemeinert zählen sie Unit-Tests, Static Code Analysis und Linting auf.

Assignments werden in einer [codefreak.yml](https://docs.codefreak.org/codefreak/for-teachers/assignments.html#_add_code_freak_configuration) definiert. Die Definition erinnert stark an die Cmd GitHub Actions.

Ansonsten gibt es meiner Meinung nach nichts mehr, was für uns relevant sein könnte.
