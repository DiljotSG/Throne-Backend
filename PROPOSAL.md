# Project Proposal

## Vision Statement

Throne is a web and mobile application which allows users to find nearby washrooms tailored to their preferences and requirements. Throne presents up-to-date information by enabling users to provide feedback and information on the washrooms they visit.

## Motivation

### What is Throne?

Throne is washroom information app, whose core functionality can be summarized by locating, reviewing, and adding new washrooms for other users to find. Users of the app will have the ability to find, search for, and leave feedback on washrooms they have visited. Users will also be able to view washroom details including cleanliness, privacy, quality, accessibility, and available amenities. When adding a new washroom to the map, users will be required to provide basic information about the washroom – other users can then verify the accuracy of this information. This will eventually lead to a database of washrooms with accurate information. Finally, the user will have the ability to customize their experience by setting preferred terminology and washroom preferences.

### Who is Throne for?

Throne is for anyone looking to answer the simple question, “Which washroom is best for me?”. By catering to users with specific accessibility requirements and privacy preferences, Throne will help a broad and diverse set of people who want to use a great washroom.In its early phase, Throne will be targeted towards the students and faculty of the University of Manitoba, which will provide us with a manageable amount of initial data. As Throne scales up, we could increase the number of supported areas by either expanding to the rest of Winnipeg or targeting specific cities.

### Why is Throne valuable?

The value of Throne will come from the curated and accurate list of washrooms – a crucial aspect to providing users with up-to-date information. Throne will also add value by unifying all washroom data into a single accessible application. As a result, people with specific washroom requirements (wheelchair, gender neutral, changing stations, etc...) will be presented with nearby washrooms that meet their needs.

### Measurable Success Criteria

The success criteria for the Throne application is centered around the data collected and the user base. From a data standpoint, Throne would be successful in its initial phase if 80% of the public washrooms on the University of Manitoba campus were available on the app. With regards to users, if Throne received 200 installs and 20 daily active users within the first four months it would also be considered a success.

## Application Technical Details

The following is a brief overview and justification of the technical specifications for Throne.

### Backend & API

The first and possibly most important decision that we made was the choice of backend technology for Throne. After some research we agreed that Python was the best decision for the project. One of the factors in this decision was the reduced amount of boilerplate code needed to get a functional prototype. As an added benefit, Python can be developed natively with ease on multiple platforms. Additionally, many of our team members are familiar with Python in both an academic and industry setting. The shorter ramp-up time that comes with experience and familiarity will allow us to develop a functional prototype quicker.

We will utilize the Flask framework for Python to create our API endpoints. By using a well-established and documented framework like Flask, we have a large collection of resources at our disposal to guide us. This will allow us to begin creating API endpoints early on in development.

We decided to create our backend as a serverless platform using AWS Lambda. One of the factors in our team’s decision is the amount of experience we have with AWS Lambda in a real-world setting. This will allow us to get the critical backend up and running faster.

An advantage of AWS Lambda is that it handles a number of tedious tasks, including running API code, creating public endpoint URLs, and exposing API routes. AWS Lambda abstracts away all environment-related details, allowing us to easily expose our RESTful API with a public endpoint URL. This will allow our team to develop a working backend quickly, when compared to developing directly on EC2. With this in mind, we will still be using EC2 to host our web application.

Aside from ease of use, cost is equally as important. AWS Lambda is a cost-effective solution for our limited use case, as the free one million monthly requests will likely not be exceeded over the duration of this course. Additionally, AWS Lambda can be scaled easily, by requiring minimal additional configuration and setup procedures when compared to using EC2 or other alternative backend solutions.

### Data & Storage

Regarding data storage, we have decided to use two storage solutions, each to fulfill a specific purpose. Firstly, Amazon RDS is a relational database service that will allow us to run the API in the cloud using AWS Lambda. This will eliminate our need for a persistent local storage solution like SQLite running on EC2. We chose a relational database over a non-relational database as the data schema we decided on will remain relatively fixed throughout the lifetime of the application. Lastly, we will use Amazon S3 for general purpose cloud file storage for various tasks such as updating our Lambda code and storing application assets.

### Web Application

For the web application component of Throne, we will use the React JavaScript framework for frontend development. By creating a web-based application using React, we can deploy our application to a number of platforms. This will allow us to deliver the application to users regardless of platform, from mobile devices to desktop browsers.

The decision to use React instead of the other numerous JavaScript frameworks was made due to a number of factors. To begin with, the majority of our team members with web development experience have used the React framework in an industry setting. This will not only enable us to have a quicker ramp-up time but will also allow us to exercise best practices learned through real-world experience. Another benefit to using React is the extensive and active community surrounding it. As one of the most actively maintained and documented JavaScript frameworks, our team will have many channels and resources available to facilitate the development process.

### Mobile

Beyond the web application, we will provide a first-class mobile experience, as this is the main platform for many users. Throne will have a native iOS application built using the Swift programming language and Cocoa Touch frameworks including SwiftUI, UIKit, and Foundation. We have chosen these native iOS technologies for a number of reasons. Firstly, they provide a good mix of familiarity and novelty – team members are familiar with the Swift programming language, while new UI frameworks like SwiftUI provide an exciting learning opportunity. Additionally, a native iOS application will provide the best experience for users of Throne. SwiftUI provides the native user experience and performance that iOS users expect, with automatic support for features like dark mode, responsive interface layout, and accessibility. Lastly, using the recommended technologies of the platform is conducive to cleaner code, and provides us access to plenty of documentation and online support from Apple and the iOS development community.

To limit the scope of this project, the Android application will consist of a wrapper around our web application. Considering the fact that our web application will be designed with a mobile-first approach, it will feel similar to a native app.

## User Stories

All user stories and tasks will be tracked using GitHub Issues which can be found on the repository page found [here](https://github.com/DiljotSG/throne-app).

### High Priority

- As a user, I want to see washrooms near me on a map **(6 days)**
- As a user, I want to leave reviews on washrooms **(3 days)**
- As a user, I want to add new washroom locations to the map **(4 days)**
- As a user, I want to be able to filter washrooms by different criteria **(3 days)**
- As a user, I want to create an account **(3 days)**

### Medium Priority

- As a user, I want to save my washroom preferences **(2 days)**
- As a user, I want to fill out the details in my account profile (**3 days)**
- As a user, I want to ‘favourite’ washrooms **(1 day)**
- As a user, I want to share washrooms with others **(2 days)**

### Low Priority

- As a user, I want to report issues with the details of washrooms **(2 days)**
- As a user, I want to know if washrooms are verified **(2 days)**
- As a user, I want to see an image of the entrance to washrooms **(2 days)**
- As a user, I want to see reviews other users left on washrooms **(2 day)**
- As a user, I want to get rewards for leaving reviews on washrooms **(4 days)**
- As a user, I want to filter washrooms by a search query **(3 days)**
- As a user, I want to see time estimates for how long people spend at specific washrooms **(2 days)**
- As a user, I want to alert businesses to maintenance issues with their washrooms **(2 days)**