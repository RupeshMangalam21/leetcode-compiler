#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "No source file provided"
    exit 1
fi

SOURCE_FILE="$1"
CLASS_NAME="${SOURCE_FILE%.*}"

# Compile the Java file
javac "$SOURCE_FILE"

# Run the compiled Java class with security manager and memory limits
java -Xmx512m -Djava.security.manager \
     -Djava.security.policy==/app/java.policy "$CLASS_NAME"
