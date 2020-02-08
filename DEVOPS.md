# Throne App DevOps Setup

## Continuous Integration Pipelines

In order to enhance and simplify our development process we decided to create continuous integration pipelines for all of the Throne repositories, which was relatively straightforward using the built-in GitHub Actions platform. By running linters and tests before merging code in, it enables us to find and solve problems with new code before integrating it into the production application. 

### Mobile Applications

For the Android and iOS repositories we created basic workflows to run our test suites and build the mobile applications, which was made easier with the documentation and example workflows provided by GitHub.

### Web and Backend Applications

For the web and backend repositories, the pipeline installs app dependencies, runs the code through a linter for consistency and formatting, then finally runs each app's test suites. This allows us to see any broken code, missed formatting, or failed unit tests.

## Automatic Deployment to AWS

### Backend Application

The backend application is auto deployed to AWS Lambda when a change is merged to either `master` or `develop` branches. When there is a new push to `master`/`develop`, a custom workflow is run. To deploy the backend application we are using the [serverless framework](https://github.com/serverless/serverless). 

#### Deployment Workflow

- Install serverless plugins being used
- Run serverless deployment command, which:
  - Packages the code
  - Installs the appropriate dependencies
  - Uploads the code to AWS S3
  - Updates the Lambda application

The AWS secret key and ID are stored in the GitHub repository settings (GitHub stores and encrypts them).

This results in the Backend application being deployed to the following URLs: [Prod API Endpoint](https://api-prod.findmythrone.com/), and [Dev API Endpoint](https://api-dev.findmythrone.com/) for the `master` and `develop` branches respectively. To achieve this workflow we had to create a custom GitHub Action, which can be found [here](https://github.com/DiljotSG/serverless-github-action-python).

### Web Application

The web application is auto deployed to AWS S3 when a change is merged to either `master` and `develop` branches. When there is a new push to `master`/`develop`, a custom workflow similar to the backend deployment workflow is run.

#### Deployment Workflow

- Install the dependencies for the react app
- Build react app (details depend on branch being built).
  - The react app is built differently depending on the branch being built.
    -  `develop`  builds using the environment variables in the `.env.development` file
    -  `master`  builds using the environment variables in the `.env.production` file
  - These separate environment variable files allow us to specifiy different values for different build environments. For example, `master` and `develop` use production and development API endpoints respectively. Having separate `.env` files allows each build to use a different endpoint.
-  Sync the built application with the appropriate S3 bucket using a custom GitHub Action
  - There are two S3 buckets: one for the Prod Web App and another for the Dev Web App.

This results in a successful deployment to the web. The resulting applications can be found at  [Prod Web App](https://app.findmythrone.com/), and [Dev Web App](https://dev.findmythrone.com/) for the `master` and `develop` branches respectively.