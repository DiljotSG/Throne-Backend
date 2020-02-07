Master

![Python application](https://github.com/DiljotSG/Throne-Backend/workflows/Python%20application/badge.svg?branch=master)

Develop

![Python application](https://github.com/DiljotSG/Throne-Backend/workflows/Python%20application/badge.svg?branch=develop)

# Throne Backend
This repository contains the backend for the Throne application.

Throne is a web and mobile application which allows users to find nearby washrooms tailored to their preferences and requirements. Throne presents up-to-date information by enabling users to provide feedback and information on the washrooms they visit.

Throne Component | Reposistory | Project Board
------------ | ------------- | ------------
All Components | - | [User Stories](https://github.com/DiljotSG/Throne-Backend/projects/1)
**Backend** | [Throne-Backend](https://github.com/DiljotSG/Throne-Backend) | [Backend Tasks](https://github.com/DiljotSG/Throne-Backend/projects/2)
Web | [Throne-Web](https://github.com/DiljotSG/Throne-Web) | [Web Tasks](https://github.com/DiljotSG/Throne-Web/projects/1)
iOS | [Throne-iOS](https://github.com/NickJosephson/Throne-iOS) | [iOS Tasks](https://github.com/NickJosephson/Throne-iOS/projects/1)
Android | [Throne-Android](https://github.com/NickJosephson/Throne-Android) | [Android Tasks](https://github.com/NickJosephson/Throne-Android/projects/1)

# API Endpoints

### Production API Endpoint - `master` branch: https://api-prod.findmythrone.com

### Development API Endpoint - `develop` branch: https://api-dev.findmythrone.com

# Setup

This codebase uses Python3.X, particularly Python3.7.X and Python3.8.X (in the Lambda).

## Installing Python3

You'll first need to install Python3. Here is the easiest way to do it for macOS (requires Brew).

```shell
brew install python
```

## Environment Setup for Backend Development
1. Create a Python virtual environment and activate the environment.
```shell
virtualenv -p python3 venv
. venv/bin/activate
```

If you encounter an error at this stage, that says something like `command not found: virtualenv`. You will need to re-install `virtualenv`. The easiest way to do so is as follows.

```shell
pip uninstall virtualenv
sudo pip install virtualenv
```

2. Install Python dependencies.

```shell
pip3 install -r requirements.txt
```

3. Run the Flask application locally.
```shell
python3 handler.py
```

4. Run the application Unit Tests locally.
```shell
python -m unittest discover tests
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
