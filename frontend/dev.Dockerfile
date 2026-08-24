FROM oven/bun:1

# Set the working directory
WORKDIR /app

# Copy package.json and bun.lock files
COPY package.json bun.lock ./

# Install dependencies
RUN bun install --frozen-lockfile

# Copy the rest of the application code
COPY . .

# Run application in development mode
CMD ["bun", "dev", "--", "--host", "0.0.0.0"]
