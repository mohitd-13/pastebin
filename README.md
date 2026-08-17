# PASTEBIN

This Pastebin is a full-stack project designed to store code snippets, errors logs, and other text-based content, convert them into shareable links. A developer debugging a production issue copies 200 lines of error logs and pastes them into the Pastebin. They click "Generate Link" receive a short URL "https://example.com/3cik8s5t" they can post this link on Github issue to ask for help from other developer.

## Demo

[View Demo](https://example.com)

## Getting Started

# Prerequisites (For Local Development)

You need to have the following installed on your machine:

- Docker & Docker Compose
- An AWS account & AWS CLI Configured
- A remote AWS S3 Bucket

# Installation

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

[!NOTE] Replace `mypassword` with password of your choice, try not to change any folder or file names.

4. Copy your AWS config and credentials for docker compose:

   ```bash
   mkdir -p .docker/aws
   cp ~/.aws/config .docker/aws/config
   cp ~/.aws/credentials .docker/aws/credentials
   ```

[!NOTE] The `~/.aws/config` and `~/.aws/credentials` files are typically located in your home directory.
[!WARNING] Do not commit the `.docker/aws` directory to version control.

5. Run the application:

   ```bash
   docker compose up --build --watch
   ```

## Contributing

We welcome contributions from developers who want to improve Pastebin
Follow these steps to contribute effectively:

1. **Fork the Repository**

    - Click the Fork button on Github to create your own copy of the project.

2. **Clone Your Fork**

    - Run

    ```bash
    git clone https://github.com/mohitd-13/pastebin.git
    ```

3. **Set Up Database password & AWS credentials**

    - Follow the setup instructions in the README to setup your credentials make sure not to change any folder or file names, if you do want to change any folder or file names, make sure they are updated in the compose.yaml and .gitignore so they don't end up in the repository.

4. **Create a Feature Branch**

    - Keep your changes organized:

    ```bash
    git checkout -b feature/your-feature-name
    ```

5. **Use Clear Commit Messages**

    - Make sure to always follow the conventional commit style without it, automated release process will not happen:
        - feat: - new feature
        - fix: - bug fix
        - BREAKING CHANGE: - new changes that are not backward-compatible
        - docs: - documentation update
        - refractor: - code restructuring

    - Document Your Changes
        - Update README.md or CONTRIBUTING.md if needed

6. **Submit a Pull Request (PR)**

    - Push your branch and open a PR with:

        - A short, clear description of your changes.
        - Any related issue numbers (for example, "Closes #12").
        - Screenshots or example outputs (if applicable).

7. **Participate in Code Review**

    - Respond to feedback, make improvements, and help maintain project quality.

## License

This project is licensed under the MIT License-see the LICENSE file for details.
