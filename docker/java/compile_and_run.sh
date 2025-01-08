#!/bin/sh
set -e

# Debugging: List the current directory contents
echo "Current directory contents:"
ls -lah

if [ -z "$1" ]; then
    echo "Error: No source file provided."
    exit 1
fi

SOURCE_FILE="$1"
CLASS_NAME=$(basename "$SOURCE_FILE" .java)

# Debugging: Display source file and class name
echo "Source file: $SOURCE_FILE"
echo "Class name: $CLASS_NAME"

# Ensure the class file is removed before recompiling
echo "Removing existing class file if any..."
rm -f "$CLASS_NAME.class"

# Compile the Java source file
echo "Compiling $SOURCE_FILE..."
javac "$SOURCE_FILE"
if [ $? -ne 0 ]; then
    echo "Compilation failed."
    exit 1
fi

# Run the compiled Java class
echo "Running $CLASS_NAME..."
java "$CLASS_NAME"