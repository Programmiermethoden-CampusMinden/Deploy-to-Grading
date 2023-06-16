---
title: Programming Exercise Markup Language (PEML)
url: https://cssplice.github.io/peml/
---

## Bibtex

```
@inproceedings{peml,
    author    = {Divyansh S. Mishra and Stephen H. Edwards},
    title     = {The Programming Exercise Markup Language: Towards Reducing the Effort Needed to Use Automated Grading Tools},
    year      = {2023},
    doi       = {10.1145/3545945.3569734},
    pages     = {395–401},
    booktitle = {Proceedings of the 54th ACM Technical Symposium on Computer Science Education V. 1}
}
```

# Zusammenfassung

PEML ist eine eigens definierte Sprache zur Definition von Übungsaufgaben. Es wird ein Ruby-Parser angeboten sowie zwei API-Schnittstellen zur Umwandlung in JSON.

Eine Aufgabenstellung könnte beispielsweise folgendermaßen aussehen:

```
exercise_id: edu.vt.cs.cs1114.palindromes

# Single-line comments start with #
# Comments must be on lines by themselves

title: Palindromes (A Simple PEML Example)

license.id: cc-sa-4.0
license.owner.email: edwards@cs.vt.edu
license.owner.name: Stephen Edwards

topics: Strings, loops, conditions
prerequisites: variables, assignment, boolean operators

instructions:----------
Write a program that reads a single string (in the form of one line
of text) from its standard input, and determines whether the string is
a _palindrome_. A palindrome is a string that reads the same way
backward as it does forward, such as "racecar" or "madam". Your
program does not need to prompt for its input, and should only generate
one line of output, in the following
format:

#``` (hastags are here so that it is not considered markdown)
"racecar" is a palindrome.
#```

Or:

#```
"Flintstone" is not a palindrome.
#```
----------

assets.test_format: stdin-stdout

[systems]
language: java
version: >= 1.5
[]

# Test data/files/classes are probably located in separate files, but this
# is a simple example of how to do something directly inline
[suites]
[.cases]

stdin: racecar
stdout: "racecar" is a palindrome.


stdin: Flintstone
stdout: "Flintstone" is not a palindrome.


stdin: url(some/local/input.txt)
stdout: url(some/local/output.txt)


stdin: url(http://my.school.edu/some/local/generator/input)
stdout: url(http://my.school.edu/some/local/generator/output)

[]
[]
# The [] ends/closes a list of items, but they can be omitted at the
# end of the file, since EOF auto-closes any open lists. The first []
# closes the list of cases in one suite, while the second [] closes
# the list of suites, which here includes only one suite.
```

Quelle: https://cssplice.github.io/peml/examples/
