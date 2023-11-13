#!/bin/bash

# Script for executing the JPlag plagiarism check. This script is meant to be
# executed in the teacher script of the Deploy-to-Grading pipeline. It is not
# meant to be used as a typical metric script. Therefore, don't include it in
# any task.yml file.
#
# Make sure that the ASSIGNMENT_TEMPLATE_REPOSITORY environment variable is
# set to the Git URL of the template repository.
#
# usage: jplag.sh
#

# Change this if you want to update the JPlag version.
JPLAG_VERSION="4.3.0"

JPLAG_URL=https://github.com/jplag/JPlag/releases/download/v${JPLAG_VERSION}/
JPLAG_PATH=jplag/
JPLAG_FILE=jplag-${JPLAG_VERSION}-jar-with-dependencies.jar

STUDENT_REPO_PATH=repos/
TEMPLATE_PATH=template_repo/
# We do not add file ending here as it is always appended by JPlag.
OUT_PATH=${JPLAG_PATH}jplag_results

# Clone template repository if known. Fail if not known.
if [ -z ${ASSIGNMENT_TEMPLATE_REPOSITORY} ]
then
    echo "No template repository is set. Aborting plagiarism check."
    exit -1
else
    git clone ${ASSIGNMENT_TEMPLATE_REPOSITORY} ${JPLAG_PATH}${TEMPLATE_PATH}
fi

# Download JPlag if it does not exist.
if [ ! -e ${JPLAG_PATH}${JPLAG_FILE} ]
then
    wget -P ${JPLAG_PATH} ${JPLAG_URL}${JPLAG_FILE}
fi

mkdir ${OUT_PATH}

# Execute JPlag
java -jar ${JPLAG_PATH}${JPLAG_FILE} -l java -r ${OUT_PATH} \
    -bc ${JPLAG_PATH}${TEMPLATE_PATH} -new ${STUDENT_REPO_PATH}

