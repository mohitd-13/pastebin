FROM node:24.14.0-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Set ownership of the app directory to the node user
RUN chown -R node:node /app

# Switch to the node user
USER node

# Expose the application port
EXPOSE 5173

# Run application in development mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
