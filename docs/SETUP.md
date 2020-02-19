# Setup

This codebase uses Python3.7.X and Python3.8.X (in the Lambda). These setup instructions are for macOS using [Homebrew](https://brew.sh). Installing these dependencies should be similar for other platforms with the appropriate package managers for that platform.

## Python3 Installation

1. Install python.

    ```shell
    brew install python
    ```

## Environment Setup

These steps are required for backend development.

1. Create a Python virtual environment.

    ```shell
    virtualenv -p python3 venv
    ```

2. Activate the environment.

    ```shell
    . venv/bin/activate
    ```

    **Note:** If you encounter an error at this stage, that says something like `command not found: virtualenv` you will need to re-install `virtualenv`.

    The easiest way to do so is as follows:

    ```shell
    pip3 uninstall virtualenv

    sudo pip3 install virtualenv
    ```

3. Install Python dependencies.

    ```shell
    pip3 install -r requirements.txt
    ```

4. Run the Flask application locally.

    Normal mode:

    ```shell
    python3 handler.py
    ```

    Development Mode (Auto reloads on code changes):

    ```shell
    export FLASK_ENV=development

    python3 handler.py
    ```

## Dependency Installation

These steps install the dependencies required for deploying to AWS.

1. Install Docker.

    ```shell
    brew cask install docker
    ```

2. Run `docker.app` and complete the installation instructions.

3. Install Node.

    ```shell
    brew install node
    ```

4. Install the serverless framework.

    ```shell
    sudo npm install -g serverless
    ```

5. Install serverless plugins.

    ```shell
    npm install
    ```

6. Deploy the new version of the app to AWS Lambda.

    **Note:** requires AWS credentials to be set.

    To update the dev backend instance:

    ```shell
    serverless deploy
    ```

    To update the prod backend instance:

    ```shell
    serverless deploy --stage prod
    ```

7. Destroy an existing CloudFormation stack.

    **Note:** requires AWS credentials to be set.

    ```shell
    serverless remove
    ```
