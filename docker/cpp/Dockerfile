FROM gcc:latest

# Set the working directory
WORKDIR /leetcode_compiler

# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# Add a non-root user named "executor"
RUN useradd -ms /bin/bash executor

# Switch to the "executor" user
USER executor

# Add the script to compile and run code
COPY --chown=executor:executor docker/cpp/compile_and_run.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/compile_and_run.sh

# Set the default command to execute the script
CMD ["/usr/local/bin/compile_and_run.sh"]
