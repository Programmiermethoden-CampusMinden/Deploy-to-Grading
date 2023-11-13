# Documentation on Deploy-to-Grading

## Local usage

D2G can be run on any Linux operating system that comes with Bash and Python 3. To execute D2G, make sure that you are in an assignment folder, that contains an `assignment.yml` file. Furthermore, you need to set the `D2G_PATH` environment variable to the root directory of your cloned D2G repository. Execute the following command to run D2G:

```bash
$D2G_PATH/scripts/deploy_to_grading.py
```

## Execution as a CI/CD-Pipeline

You can use D2G as a CI/CD-Pipeline by adding a GitHub Workflow to your repository. The following listing shows an example configuration for such a pipeline:

```
name: Deploy-to-Grading
on:
  workflow_dispatch:
  
jobs:
  deploy-to-grading:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: programmiermethoden/deploy-to-grading@master
```

## Table of Contents

1. [Skripte für Lehrende](teacher_scripts.md)
2. [Aufgabenrepository erstellen](create_tasks_repository.md)
3. [Metriken](metrics/readme.md)
4. [Related Work](related_work/readme.md)
5. [Design Dokument](design_document/readme.md)
