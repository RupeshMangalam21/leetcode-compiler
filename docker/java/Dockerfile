FROM openjdk:latest

# Set the working directory
WORKDIR /app

# Add a non-root user named "executor"
RUN useradd -ms /bin/bash executor

# Ensure the /app directory is writable by the executor user
RUN mkdir -p /app && chown executor:executor /app

# Copy necessary files and assign correct ownership
COPY --chown=executor:executor docker/java/compile_and_run.sh /usr/local/bin/
COPY --chown=executor:executor docker/java/java.policy /app/

# Make the script executable
RUN chmod +x /usr/local/bin/compile_and_run.sh

# Switch to the non-root user
USER executor

# Set the default command to run the script
ENTRYPOINT ["/usr/local/bin/compile_and_run.sh"]
