# TODO LIST API
### created with django rest framework 

# Description

Vertion 1 of a RESTFul API to create users and tasks. Each users can register and keep tracking of their own task and marke them as completed when they are finished. The user have the posibiltiy to edit the description of the task and delete it. The admin can create staff users to check all the task.

## Auth system

All the request make it to the API need has an *Authorization header* with a valid token and the prefix *Bearer* 
`Authorization: Bearer <token>`

In order to obtain a valid token it's necesary to send a request `POST /api/v1/auth/token/` with *username* and *password*. To register a new user it's necesary to make a request `POST /api/v1/users/` with the params:
```
username String
password String
confirm_password String
```

## End Points
### Auth
`POST /api/v1/auth/refresh/`
`POST /api/v1/auth/token/`

### Users
`POST /api/v1/users/`
The following end points are just available for *staff users*
`POST /api/v1/users/`
`POST /api/v1/users/`
`POST /api/v1/users/`

# Installation process 

## Install the system dependencies
* **git** 
* **node v0.12.0** or greather
* **npm 3.8.6** or greather
* **postgres 9.4** or greather

## Get the code
1. Clone the repository
2. Change to **develop** branch
`git checkout develop`

## Install the project dependencies

`npm install`

## Config the database
1. Go to postgres console and create a new database
2. Create **local.js** file in **/config/env/** and add the following lines:

```json
module.exports = {
    db: {
        name: "DATABASE_NAME",
        password: "DATABASE_PASSWORD",
        username: "DATABASE_USERNAME",
        sync: true
    }
};
```

## Run the command to generate the frontend code
`npm run deploy`

## Run the server for first time
`npm run server`

## Deactivate the model synchronization 
1. Stop the server process
2. Change the flag **sync** to false in **/config/env/local.js**. The flag sync generate the models on the database if it is true the data will be deleted when restart the server.

## Run the server
`npm run server` the application will be running on port 3000
