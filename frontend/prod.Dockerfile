# ----------------- Stage 1: Build -------------------
FROM oven/bun:1-alpine AS builder

WORKDIR /app

COPY package.json bun.lock ./
RUN --mount=type=cache,target=/root/.bun/install/cache \
    bun install --frozen-lockfile

COPY . .
RUN bun run build

# ----------------- Stage 2: Run -------------------
FROM nginxinc/nginx-unprivileged:stable-alpine AS runner

# Replace the default server config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Add template config for forwarding backend traffic
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

# Copy only the build output
COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 8080

# Image already runs as the non-root `nginx` user (UID 101)
CMD ["nginx", "-g", "daemon off;"]
