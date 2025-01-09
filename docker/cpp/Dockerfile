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
COPY --chown=executor:executor compile_and_run.sh /bin/
RUN chmod +x /bin/compile_and_run.sh

# Set the default command to execute the script
CMD ["/bin/compile_and_run.sh"]