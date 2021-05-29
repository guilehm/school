# School

## Required
* Docker
* Docker Compose

## Installation

Clone this repository

    git clone git@github.com:Guilehm/school.git
    
Enter the repository

    cd school

Start the app

    make run
    
Now the server is running and you may access the app at this url: [http://localhost:8000/](http://localhost:8000/users/)   


## Commands

Running tests

    make test
    
Lint

    make lint
    
Create migrations

    make migrations

Apply migrations
   
    make migrate


## Containers
Stopping containers

    make stop
    
Removing containers

    make down
    
Removing containers and volumes

    make remove
    
Building the app

    make build
    
Start the app

    make run
    

## Use guide

**Creating Teachers and Students:**

There is authentication implemented. So you only need to fill the username and the password to create instances.

![Screenshot from 2021-05-29 15-16-16](https://user-images.githubusercontent.com/33688752/120080834-f7ca8380-c090-11eb-84e1-da364eabc723.png)


**Teacher and Student lists:**

Teachers [http://localhost:8000/teachers/](http://localhost:8000/teachers/)

Students [http://localhost:8000/students/](http://localhost:8000/students/)


**Teacher and Student detail:**

**replace `ID` with teacher or student `id`.*

Teachers http://localhost:8000/teachers/ID/

Students http://localhost:8000/students/ID/


**Creating relations:**

At teacher or student detail pages, you may create the relation between them by clicking in the `add` button:

![Screenshot from 2021-05-29 15-35-37](https://user-images.githubusercontent.com/33688752/120081334-8b9d4f00-c093-11eb-91dd-f11f142c778e.png)


**Starring students:**

At teacher detail page, you may check the `starred` field in the checkbox:

![Screenshot from 2021-05-29 15-33-37](https://user-images.githubusercontent.com/33688752/120081275-47aa4a00-c093-11eb-827f-86a477c54685.png)

**Accessing the admin:**

Create a superuser

    make superuser
    
Access the admin at [http://localhost:8000/admin/](http://localhost:8000/admin/)

## GraphQL API

Endpoint: [http://localhost:8000/graphql/](http://localhost:8000/graphql/)

Retrieve all students *(you can also retrieve their teachers if you want)*:
```graphql
query {
  allStudents {
    id
    username
  }
}
```

Retrieve all teachers and their respective students:
```graphql
query {
  allTeachers {
    id
    username
    students {
      id
      username
      starred
    }
  }
}
```

Retrieve a single Teacher or Student:
```graphql
query {
  teacherByUsername(username: "peter") {
    id
    username
  }
}
```
```graphql
query {
  studentByUsername(username: "mona") {
    id
    username
  }
}
```

Mutation to toggle the `starred` field for the relation between Teacher and Student:
```graphql
mutation myMutation {
  toggleStarred(studentId: 3, teacherId: 1) {
    relation {
      id
      username
      starred
    }
  }
}
```


## Troubleshooting

If you have Postgres running in your machine, please stop it before running the app:

    sudo systemctl stop postgresql
