# TASK-TECHFORING [DJANGO DEVELOPER]
## Overview

TechForing Limited is building a project management tool that allows teams to collaborate on projects. This API is designed to manage users, projects, tasks, and comments, and will be consumed by their front-end web application and mobile application.

---

## Table of Contents
- [API Endpoints](#api-endpoints)
  - [User](#user)
  - [Projects](#projects)
  - [Task](#task)
  - [Comments](#comments)
- [API Documentation](#api-documentation)
- [Project Installation Guide](#project-installation-guide)

---

## API Endpoints

### **User**
- **Register**: `POST /api/users/register/`
- **Login**: `POST /api/users/login/`
- **Get User**: `GET /api/users/{user_id}/`
- **Update User**: `PATCH /api/users/{user_id}/`
- **Delete User**: `DELETE /api/users/{user_id}/`

### **Projects**
- **Create Project**: `POST /api/projects/`
- **Get Project List**: `GET /api/projects/`
- **Get Project Details**: `GET /api/projects/{project_id}/`
- **Update Project Details**: `PATCH /api/projects/{project_id}/`
- **Delete Project**: `DELETE /api/projects/{project_id}/`

### **Task**
- **Create Task**: `POST /api/projects/{project_id}/tasks/`
- **Get Task List**: `GET /api/projects/{project_id}/tasks/`
- **Get Task Details**: `GET /api/tasks/{task_id}/`
- **Update Task Details**: `PATCH /api/tasks/{task_id}/`
- **Delete Task**: `DELETE /api/tasks/{task_id}/`

### **Comments**
- **Create Comment**: `POST /api/tasks/{task_id}/comments/`
- **Get Comment List**: `GET /api/tasks/{task_id}/comments/`
- **Get Comment Details**: `GET /api/comments/{comment_id}/`
- **Update Comment Details**: `PATCH /api/comments/{comment_id}/`
- **Delete Comment**: `DELETE /api/comments/{comment_id}/`

---

## API Documentation

- **Swagger API Documentation**: `GET /api/documentation/`
- **Download Schema**: `GET /api/schema/`

---


### Project Installation Guide

Clone the repo and go to the project root.
```bash
git clone https://github.com/tanzid64/project-management-techforing.git
```
```bash
cd 
```
**Docker Setup**

```bash
sudo docker compose up --build --remove-orphans -d
```
***Bash***
```bash
sudo docker exec -it <container name> bash
```
***Logs***
```bash
sudo docker logs <container name>
```

**Local Machine Setup**
```bash
virtualenv .venv
```
```bash
source .venv/bin/activate
```
***Set up the .env file***

`.env.example > .env`

In your `.env` set the following environment variables:

- `SECRET_KEY` : Your Secret Key.
- `DEBUG` : True / False.
- `DATABASE_URL` : Your Postgres Database URL.

```bash
python manage.py migrate
```
***To run test cases***
```bash
python manage.py test
```
***Run server***
```bash
python manage.py runserver
```
