---
title: Teaching Clean Code
url: https://mediatum.ub.tum.de/doc/1428241/document.pdf
---

## Bibtex

```
@inproceedings{dietz2018,
  title = {Teaching Clean Code},
  author = {Dietz, Linus and Manner, Johannes and Harrer, Simon and Lenhard, Jörg},
  booktitle = {1st Workshop on Innovative Software Engineering Education},
  year = {2018}
}
```

## Abstract

Learning programming is hard – teaching it well is even more challenging. At university, the focus is often on functional correctness and neglects the topic of clean and maintainable code, despite the dire need for developers with this skill set within the software industry. We present a feedbackdriven teaching concept for college students in their second to third year that we have applied and refined successfully over a period of more than six years and for which received the faculty’s teaching award. Evaluating the learning process within a semester of student submissions (n=18) with static code analysis tools shows satisfying progress. Identifying the correction of the in-semester programming assignments as the bottleneck for scaling the number of students in the course, we propose using a knowledge base of code examples to decrease the time to feedback and increase feedback quality. From our experience in assessing student code, we have compiled such a knowledge base with the typical issues of Java learners’ code in the format of before/after comparisons. By simply referencing the problem to the student, the quality of feedback can be improved, since such comparisons let the student understand the problem and the rationale behind the solution. Further speed-up is achieved by using a curated list of static code analysis checks to help the corrector in identifying violations in the code swiftly. We see this work as a foundational step towards online courses with hundreds of students learning how to write clean code.

## Notizen

In dem Paper wird ein Konzept beschrieben, mit dem Studierenden beigebracht werden kann, sauberen Programmcode zu schreiben. Die Autoren stellen mit [QualityReview](https://github.com/LinusDietz/QualityReview) eine Gradle-Konfiguration auf GitHub zur Verfügung, um automatisiert den Programmcode von Studierenden basierend auf den Ergebnissen des Papers zu überprüfen.
