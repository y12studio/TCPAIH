FROM python:3.11-slim
WORKDIR /app

# Create a non-root user
RUN adduser --disabled-password --gecos "" myuser

# Install Node.js and npm
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_22.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Change ownership of /app to myuser
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

# Set up environment variables - Start
ENV PATH="/home/myuser/.local/bin:/home/myuser/.npm-global/bin:$PATH"
ENV NPM_CONFIG_PREFIX=/home/myuser/.npm-global
# Set up environment variables - End

# Create npm global directory for the non-root user
RUN mkdir -p /home/myuser/.npm-global
# Install global npm packages
RUN npm install -g @modelcontextprotocol/server-filesystem
# Install ADK
RUN pip install google-adk

# Copy agent - Start

COPY "tcpaih-assist-201/" "/app/agents/tcpaih-assist-201/"

# Copy agent - End

EXPOSE 8000

CMD ["adk", "web", "--port=8000", "/app/agents"]