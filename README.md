# TODO LIST API
### created with django rest framework 

# Description

Vertion 1 of a RESTFul API to create users and tasks. Each user can register and keep track of their own tasks and mark them as complete when they are finished. The user has the posibiltiy to edit the description of the tasks and delete them. The admin can create staff users to check all the tasks.

## Auth system

All the requests made to the API need an *Authorization header* with a valid token and the prefix *Bearer* 
`Authorization: Bearer <token>`

In order to obtain a valid token it's necesary to send a request `POST /api/v1/auth/token/` with *username* and *password*. To register a new user it's necesary to make a request `POST /api/v1/users/` with the params:
```
username String
password String
confirm_password String
```

## End Points
### Auth
* `POST /api/v1/auth/refresh/`
* `POST /api/v1/auth/token/`

### Users
* `POST /api/v1/users/`
The following end points are just available for *staff users*
* `GET /api/v1/users/`
* `PUT /api/v1/users/{username}`
* `GET /api/v1/users/{username}`
* `PATCH /api/v1/users/{username}`
* `DELETE /api/v1/users/{username}`

### Tasks
* `GET /api/v1/tasks/`
* `POST /api/v1/tasks/`
* `PUT /api/v1/tasks/{pk}`
* `GET /api/v1/tasks/{pk}`
* `PATCH /api/v1/tasks/{pk}`
* `DELETE /api/v1/tasks/{pk}`

## Documentation
All the API docs are available in *http://0.0.0.0:8000/docs/*

# Installation process 

## Install the system dependencies
* **git** 
* **pip**

## Get the code
* Clone the repository
`git clone https://github.com/spantons/todo_app.git`

## Install the project dependencies

`pip install -r requirements/development.txt`

## Run the command to generate the database
`python manage.py migrate`

## Generate super user
`python manage.py createsuperuser`

## Run the server
`python manage.py runserver` the application will be running on port 8000 *http://0.0.0.0:8000/*

## Run the test
`python manage.py test`
