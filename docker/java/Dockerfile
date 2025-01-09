FROM openjdk:17-jdk-slim

WORKDIR /app

RUN useradd -ms /bin/bash executor && \
    mkdir -p /app && \
    chown executor:executor /app

# Install additional tools if needed
RUN apt-get update && apt-get install -y \
    --no-install-recommends \
    bash && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy necessary files
COPY --chown=executor:executor compile_and_run.sh /bin/
COPY --chown=executor:executor java.policy /app/

RUN chmod +x /bin/compile_and_run.sh

# Debugging: Verify the presence of the files
RUN ls -l /bin/
RUN ls -l /app/

USER executor

# Set the default command to keep the container running
CMD ["tail", "-f", "/dev/null"]