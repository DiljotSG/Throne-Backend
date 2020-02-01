# Throne Backend
This repository contains the backend for the Throne application.

Throne is a web and mobile application which allows users to find nearby washrooms tailored to their preferences and requirements. Throne presents up-to-date information by enabling users to provide feedback and information on the washrooms they visit.

# Setup

## Installing Python3
```shell
brew install python
```

## Installing Dependencies Required for Deploying to AWS
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

6. Deploy the new version of the app to AWS Lambda (requires AWS credentials to be set).

To update the dev backend instance.
```shell
serverless deploy
```

To update the prod backend instance.
```shell
serverless deploy --stage prod
```

7. Destroy an existing CloudFormation stack (requires AWS credentials to be set).
```shell
serverless remove
```

## Environment Setup for Backend Development
1. Create a Python virtual environment and activate the environment.
```shell
virtualenv -p python3 venv
. venv/bin/activate
```

2. Install Python dependencies.
```shell
pip3 install -r requirements.txt
```

3. Run the Flask application locally.
```shell
python3 handler.py
```

4. Run the application Tests locally.
```shell
python3 -m tests.test_api
```

## Other Repos
* [Throne-iOS](https://github.com/NickJosephson/Throne-iOS)
* [Throne-Android](https://github.com/NickJosephson/Throne-Android)
* [Throne-Web](https://github.com/DiljotSG/Throne-Web)

## Project Boards
* [Main Application Board](https://github.com/DiljotSG/Throne-Backend/projects/1)
* [iOS Board](https://github.com/NickJosephson/Throne-iOS/projects/1)
* [Web Board](https://github.com/DiljotSG/Throne-Web/projects/1)
