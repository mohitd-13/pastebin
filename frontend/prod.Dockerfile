# ----------------- Stage 1: Build -------------------
ARG NODE_VERSION=24.14.0-alpine
# Use a lightweight Node.js image
FROM node:${NODE_VERSION} AS builder

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install project dependencies using npm ci
RUN --mount=type=cache,target=/root/.npm npm ci

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build

# ----------------- Stage 2: Run -------------------
FROM node:${NODE_VERSION} AS runner

# Set the working directory
WORKDIR /app

# Set the environment variable
ENV NODE_ENV=production

# Copy only the production build output from the builder stage
COPY --link --from=builder /app/dist ./dist

# Install only the `serve` package
RUN --mount=type=cache,target=/root/.npm npm install serve@^14.2.6 --omit=dev

# Run the container as a non-root user
USER node

# Expose the port the app runs on
EXPOSE 3000

# Run `serve` directly to server the built app
CMD ["npx", "serve", "-s", "dist", "-l", "3000"]
