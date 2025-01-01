#!/bin/bash
set -e

if [ -z "$1" ]; then
    echo "No source file provided"
    exit 1
fi

SOURCE_FILE="$1"
EXECUTABLE="${SOURCE_FILE%.*}"

# Compile with warnings and security flags
g++ -Wall -Wextra -O2 -fstack-protector-strong -D_FORTIFY_SOURCE=2 \
    -o "$EXECUTABLE" "$SOURCE_FILE"

# Execute
./"$EXECUTABLE"
