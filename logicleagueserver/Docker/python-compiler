# Base image with Python, Java, and Node.js
FROM ubuntu:20.04

# Set non-interactive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install Python, Java, Node.js, and other utilities
RUN apt-get update && apt-get install -y \
    python3 python3-pip \
    openjdk-17-jdk-headless \
    nodejs npm \
    && apt-get clean

# Create a directory for user code
WORKDIR /sandbox

# Default command to keep the container running, will be overridden by user code execution
CMD ["tail", "-f", "/dev/null"]
