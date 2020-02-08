# Throne App DevOps Setup

## Continuous Integration Pipelines

### Mobile Applications

The first thing that we needed to do as a group was to enable continuous integration pipelines on all of the Throne repositories. We did this using the GitHub Actions platform, it was relatively simple to do. For the Android and iOS repositories: we were just able to create basic workflows that would run the test cases and build the mobile applications, this was easy as GitHub provides a lot of documentation and example workflows.

### Web and Backend Applications

We were also able to enable continuous integration on the web and backend repositories. For the web and backend applications, we install the dependencies for the app, we lint the code for code consistency and formatting and then we finally run all of the unit tests for the app. This allows us to know if any of the changes broke any of the code formatting rules or unit tests.

## Automatic Deployment to AWS

### Backend Application

The backend application is auto deployed to AWS Lambda when a change is merged to the `master` and `develop` branches. When there is a new push to the `master`/`develop` branches a custom workflow is run. To deploy the backend application we are using the [serverless framework](https://github.com/serverless/serverless). The first thing the custom workflow does is install the serverless plugins that we are using and then runs the serverless deployment command, which packages the code for you and installs all of the appropriate dependencies, and then uploads the code to AWS S3, and then updates the Lambda application. The AWS secret key and ID are stored in the GitHub repository settings (GitHub holds them and encrypts them for you). This results in the Backend application being deployed to the following URLs: [Prod API Endpoint](https://api-prod.findmythrone.com/), and [Dev API Endpoint](https://api-dev.findmythrone.com/) for the `master` and `develop` branches respectively. To achieve this workflow we had to create a custom GitHub Action, which can be found [here](https://github.com/DiljotSG/serverless-github-action-python).

### Web Application

The web application is auto deployed to AWS S3 when a change is merged to the `master` and `develop` branches. When there is a new push to the `master`/`develop` branches a custom workflow similar to the backend deployment workflow is run. The first thing the custom workflow does is install the dependencies for the react app and then build the react app. The react app is built differently depending on the branch that is being built. The `develop` branch builds using the environment variables in the `.env.development` file and the `master` branch builds using the environment variables in the `.env.production` file. The difference in these two environment variable files is simply which API endpoint the built react app uses. As such, the `develop` branch uses the Dev API Endpoint, and the `master` branch uses the Prod API Endpoint. Once the react app is built, we simply use a custom GitHub Action to sync the built application with the appropriate S3 bucket. There are two S3 buckets, one for the Prod Web App and another for the Dev Web App. When the files are synced, the newest version of the react app is then available on the web at the following URLs: [Prod Web App](https://app.findmythrone.com/), and [Dev Web App](https://dev.findmythrone.com/) for the `master` and `develop` branches respectively.