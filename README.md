# Xkart 🛒

A fully functional e-commerce platform built to demonstrate 
real-world DevOps deployment practices.

## Project Overview

Xkart is the reference application used to develop, test, and demonstrate the Exploy deployment platform. It is built level by level, starting from a static frontend and evolving into a fully containerized application that will be deployed through a complete CI/CD pipeline.

## Tech Stack
- HTML/CSS (Level 1) ✅
- Python + Flask (Level 2) ✅
- Docker + Nginx (Level 3) ✅

## Levels
### Level 1 - Static Frontend (Completed)✅
- Login Page
- Dashboard Page
- Home Page
- Products Page
- Cart Page
- Profile Page
- Settings Page
- Custom 404 Page
- Register Page
- All pages linked together

### Level 2 - Python Flask Backend (Completed)✅
- Backend development with Flask
- User authentication and sessions
- Database integration
- REST APIs for products and cart

### Level 3 - Docker + Nginx (Completed)✅
- Write Dockerfile manually
- Build and run Docker image locally
- Test Xkart in browser via Docker
- Configure Nginx as a reverse proxy inside the Docker container

## Progress

### Level 1 - Static Frontend ✅
- [x] Login page
- [x] Dashboard page
- [x] Home Page
- [x] Products page
- [x] Cart page
- [x] Profile page
- [x] Settings page
- [x] Custom 404 page
- [x] Register page
- [x] All pages linked together

Built a complete static e-commerce frontend using HTML and CSS.
All pages are fully linked and hosted locally in the browser.

### Level 2 - Python Flask Backend ✅
- [x] Flask app setup
- [x] User authentication
- [x] Database integration
- [x] REST APIs

Built a fully functional Python Flask backend with SQLite database, user authentication, sessions, password hashing and REST APIs for products and cart.

### Level 3 - Docker + Nginx ✅
- [x] Write Dockerfile manually
- [x] Build Docker image
- [x] Run Xkart in Docker container
- [x] Test in browser via Docker
- [x] Configure Nginx as a reverse proxy inside the Docker container

Built a fully containerized Flask application using Docker with Nginx as a reverse proxy. Nginx handles incoming requests on port 80 and forwards them to Flask running internally on port 5000 inside the container.

## Architecture

```
Browser
   │
   ▼
Nginx (Port 80)
   │
   ▼
Flask (Port 5000)
   │
   ▼
SQLite Database
```

## How to Run

### Run with Docker (Recommended)
```bash
docker build -t xkart .
docker run -p 80:80 xkart
```
Open http://localhost in browser

### Run Locally
```bash
pip install -r requirements.txt
python3 app.py
```
Open http://localhost:5000 in browser

## Prerequisites
- Docker installed
- Python 3.11+ installed
- Git installed

## About This Project
The frontend (HTML & CSS) was built with AI assistance to accelerate UI development. The backend, Docker, and infrastructure are implemented manually by me as part of my DevOps learning journey. AI is used as a learning and guidance tool throughout the development process.

## Author
Muneeb Rather