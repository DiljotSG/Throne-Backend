# User Authentication

## Overview

To provide user accounts and authentication, Throne integrates with Amazon Cognito. Cognito provides a "User Pools" service which maintains a store of users and their credentials. Cognito also provides hosted web UI and OAuth 2.0 APIs for handling user sign up, sign in, and other account management functionality. The Throne web and iOS clients, use these APIs to generate authentication tokens for secure interaction with the Throne backend API. The Throne backend uses Amazon API Gateway to manage  API REST endpoints. The API Gateway for Throne is configured with Cognito to ensure all API calls are authenticated with valid tokens. Throne also extends the functionality of Congino through Amazon Lambda Functions that are triggered by certain actions such as user sign up.

## Setup

Below is a **high level** description of the authentication setup that has been done for various components of Throne. 

### User Pools

1. Created a new Cognito User Pool with storage of minimal user attributes. We store as little personal user information as possible and other user information like washroom preferences are stored in our [database](DATABASE_INFO.md).
2. Configured app clients which define the identity providers and OAuth 2.0 settings to use when interacting with clients. For OAuth flow we use authorization code grant over implicit grant because it is more secure, although it does introduce more work for clients as described below.
3. Configured the hosted UI which provides an OAuth 2.0 authorization server with built-in webpages that can be used to sign up and sign in users.
4. Configured a custom domain to be used with for the hosted UI and OAuth 2.0 API endpoints.

### API Gateway

1. Created a new API Gateway Authorizer which provides controlled access to APIs using Amazon Cognito User Pools. The Authorizer is configured to look for a specific header attribute of requests for an authentication token.
2. Added the Authorizer to all Gateway Resources (routes/paths).
3. Programmed the Lambda Functions triggered by API Gateway to lookup the currently authenticated user in the event information passed to the Lambda.

### Throne Clients
