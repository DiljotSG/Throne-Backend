# User Authentication

## Overview

To provide user accounts and authentication, Throne integrates with Amazon Cognito. Cognito provides a "User Pools" service which maintains a store of users and their credentials. Cognito also provides hosted web UI and OAuth 2.0 APIs for handling user login, signup, and other account management functionality. The Throne web and iOS clients, use these APIs to generate authentication tokens for secure interaction with the Throne backend API. The Throne backend uses Amazon API Gateway to manage  API REST endpoints. The API Gateway for Throne is configured with Cognito to ensure all API calls are authenticated with valid tokens. Throne also extends the functionality of Congino through Amazon Lambda Functions that are triggered by certain actions such as user sign up.

## Setup
