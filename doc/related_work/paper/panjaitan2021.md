---
title: Integration Model for Learning Management Systems, Source Control Management, and Autograders using Service-Oriented Architecture Principle
url: https://ieeexplore.ieee.org/document/9648450
---

## Bibtex

```
@inproceedings{panjaitan2021,
  author    = {Bram Musuko Panjaitan and Satrio Adi Rukmono and Riza Satria Perdana},
  booktitle = {International Conference on Data and Software Engineering (ICoDSE)},
  title     = {Integration Model for Learning Management Systems, Source Control Management, and Autograders using Service-Oriented Architecture Principle},
  year      = {2021}
}
```

## Abstract

Most learning management systems (LMS) use a file uploader that receives archived source code from a student for programming exercises and requires the teacher to grade it manually. In this approach, students do not learn to use standard professional tools to work on a source code, and the teachers also spend much time grading. There is an opportunity to use source control management (SCM), such as Git via GitHub or GitLab, as a submission method for students. This mechanism helps programming students practice a common process used in the professional world as early as possible. Rather than manual grading, autograders are widely used in Learning Management Systems to help instructors grade student works. Autograders work faster than humans and provide objective grading. This paper discusses an integration model for learning management systems, source control management, and autograders, each of these components is usually used separately. We write a reference implementation that uses Moodle as the LMS and GitLab as the SCM. We also build a minimally functional autograder in place for proof-of-concept in this implementation. Students can submit their work using the merge request feature provided by GitLab from the repository that they fork from the instructor’s original repository. The system captures the merge request event, and the autograder starts grading student works and updates student scores in the LMS. We also discuss how the system performs when dealing with many requests semi-simultaneously to simulate an exam situation. The system follows the Service-Oriented Architecture (SOA) principle to keep each component agnostic, and developers can use any LMS, SCM, and autograder they find suitable. In our experiment, the system can handle 200 submissions in a short period amount of time. The results are that the student learns SCM basic workflow using the system, and the teachers are helped by automated grading.

## Notizen

Proof-of-Concept eines Autograders, bei dem das Konzept sehr nah an unseres herankommt: Es wird über ein Merge-Request-Event auf GitLab ein Autograder angestoßen.
