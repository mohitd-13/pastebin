# PASTEBIN

Pastebin is a full-stack application designed to store code snippets, errors logs, and other text-based content and convert them into shareable URLs. A developer debugging a production issue encounters errors, can use Pastebin to copy the error logs, and convert them into unique shareable URLs. They can then post or share this URL with others to get help from other developers who may have encountered the same issue.

## Demo

Click here to see live demo: [Live Demo](https://pastebin-ivory.vercel.app/)
> [!NOTE] 
> The demo may take a cold start of 15-20 seconds.

![Demo](./assets/pastebin-demo.gif)

## Tech Stack

- [FastAPI](https://fastapi.tiangolo.com/) for python backend API.
- [React](https://reactjs.org/) for frontend UI.
- [PostgreSQL](https://www.postgresql.org/) as a primary database for saving paste metadata.
- [AWS S3](https://aws.amazon.com/s3/) for storing paste content.
- [Docker Compose](https://docs.docker.com/compose/) for local development.

## Getting Started

### Prerequisites (For Local Development)

You need to have the following installed on your machine:

- Docker & Docker Compose
- An AWS account & AWS CLI Configured
- A remote AWS S3 Bucket

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/pastebin.git
   ```

2. Navigate to the project directory:

   ```bash
   cd pastebin
   ```

3. Create a secrets file for postgresql password:

   ```bash
   mkdir -p core/secrets/postgresql
   echo "mypassword" > core/secrets/postgresql/credential
   ```

> [!NOTE]
> Replace `mypassword` with password of your choice, try not to change any folder or file names.

4. Copy your AWS config and credentials for docker compose:

   ```bash
   mkdir -p .docker/aws
   cp ~/.aws/config .docker/aws/config
   cp ~/.aws/credentials .docker/aws/credentials
   ```

> [!NOTE]
> The `~/.aws/config` and `~/.aws/credentials` files are typically located in your home directory.
>
> [!WARNING]
> Do not commit the `.docker/aws` directory to version control.

5. Run the application:

   ```bash
   docker compose up --build --watch
   ```

## Architecture Overview

### High-Level Overview

![Alt Text](./assets/architecture.png)

The system separates concerns:
- **Frontend**: Handles user interactions and displays the UI.
- **Backend**: Manages the business logic and data persistence.
- **Database**: Stores paste metadata.
- **Object Storage**: Stores paste content.

### Creating a Paste

Users upload text content. The system generates a unique short URL and persists the text. The URL is returned immediately for sharing.

![Alt Text](./assets/writepath.png)

1. User pastes 50 lines of error logs and clicks "Generate Link".
2. Frontend renders UI and sends the data to the backend.
3. Backend receives the text data and generates a unique id for the paste.
4. Stores the text metadata into the database, if fails, returns an error.
5. Stores the text content into object storage, if fails, deletes the metadata, returns an error.
6. User receives back a unique URL and can share it with others.

### Retrieving a Paste

Users can retrieve pastes using the unique URL generated during creation.

![Alt Text](./assets/readpath.png)

1. User enters the unique URL into the browser and frontend receives the URL.
2. Frontend extracts the unique id from the URL and sends a request to the backend.
3. Backend obtains the text content from AWS s3 object storage and returns it to the frontend.
4. Frontend renders the UI and displays the text content to the user.

## API Documentation

The API documentation is available through FastAPI's Swagger UI at [Docs](https://pastebin-0axv.onrender.com/docs).

> [!NOTE]
> This may also take a few minutes to load.

## Contributing

We welcome contributions from developers who want to improve Pastebin
Follow these steps to contribute effectively:

1. **Set Up Database password & AWS credentials**

    - Follow the setup instructions in the README to setup your credentials make sure not to change any folder or file names.

2. **Create a Feature Branch**

    - Keep your changes organized:

    ```bash
    git checkout -b feature/your-feature-name
    ```

3. **Use Clear Commit Messages**

    - Make sure to always follow the conventional commit style without it, automated release process will not happen:
        - feat: - new feature
        - fix: - bug fix
        - BREAKING CHANGE: - new changes that are not backward-compatible
        - docs: - documentation update
        - refactor: - code restructuring

    - Document Your Changes
        - Update README.md or CONTRIBUTING.md if needed

4. **Submit your PR and participate in code review**

    - Push your branch and open a Pull Request with:

        - A short, clear description of your changes.
        - Any related issue numbers (for example, "Closes #12").
        - Screenshots or example outputs (if applicable)
        - Respond to feedback, make improvements, and help maintain project quality.

## License

This project is licensed under the MIT License.
