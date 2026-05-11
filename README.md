# Fountain Ministry SA Platform

## 🌍 Live Preview
[![Live Website](https://img.shields.io/badge/Live%20Website-Visit%20Now-success)](https://fountainministrysa.netlify.app/)

---

# 📖 Overview

Fountain Ministry SA Platform is a modern full-stack ministry management and engagement system built to provide an interactive digital experience for church members, visitors, and administrators.

The platform combines a responsive frontend with a Python-powered backend and PostgreSQL database to support dynamic content management, livestream integration, prayer requests, event registrations, announcements, and administrative control.

This project evolves beyond a traditional church website into a scalable ministry platform.

---

# 🎯 Project Goals

- Build a modern online presence for Fountain Ministry SA
- Improve communication between the ministry and members
- Digitize event registrations and prayer requests
- Provide centralized admin content management
- Support livestream engagement
- Build scalable backend architecture

---

# 🛠️ Tech Stack

## Frontend
- HTML5
- CSS3
- JavaScript
- Bootstrap

## Backend
- Python
- Flask
- SQLAlchemy
- Flask-JWT-Extended

## Database
- PostgreSQL

## Hosting & Deployment
- Netlify (Frontend)
- Render (Backend)
- PostgreSQL Database Hosting

## External Services
- Facebook Live Integration
- Brevo Email Services

---

# 🧱 System Architecture

```txt
Client Browser
      │
      ▼
Frontend (HTML/CSS/JS)
      │
      ▼
Flask API Backend
      │
 ┌────┼─────────────┐
 ▼    ▼             ▼
Auth  Services    Admin Panel
 │    │             │
 ▼    ▼             ▼
PostgreSQL Database
```

---

# 📂 Updated Project Structure

```txt
Fountain-Ministry-SA/
│
├── frontend/
│   │
│   ├── index.html
│   ├── about.html
│   ├── contact.html
│   ├── events.html
│   ├── livestream.html
│   │
│   ├── css/
│   │   ├── styles.css
│   │   └── responsive.css
│   │
│   ├── js/
│   │   ├── script.js
│   │   ├── api.js
│   │   └── auth.js
│   │
│   ├── images/
│   └── assets/
│
├── backend/
│   │
│   ├── app/
│   │   │
│   │   ├── routes/
│   │   │   ├── auth_routes.py
│   │   │   ├── prayer_routes.py
│   │   │   ├── event_routes.py
│   │   │   └── sermon_routes.py
│   │   │
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── prayer.py
│   │   │   ├── event.py
│   │   │   └── sermon.py
│   │   │
│   │   ├── services/
│   │   ├── middleware/
│   │   ├── utils/
│   │   ├── config/
│   │   └── templates/
│   │
│   ├── migrations/
│   ├── requirements.txt
│   ├── run.py
│   └── .env
│
├── database/
│   └── schema.sql
│
├── docs/
│   ├── DATAFLOW.md
│   ├── API_DOCUMENTATION.md
│   └── SYSTEM_WORKFLOW.md
│
└── README.md
```

---

# 🔥 Core Features

## 🌐 Public Features
- Responsive website
- About ministry section
- Events & service schedules
- Livestream integration
- Sermons/media section
- Prayer request form
- Contact form
- Newsletter subscription

## 🔐 Admin Features
- Secure login system
- Dashboard analytics
- Event management
- Sermon uploads
- Prayer request moderation
- Livestream link management
- Email announcements

---

# 🗄️ Database Entities

## Main Tables

### Users
Stores admin authentication and role management.

### PrayerRequests
Stores submitted prayer requests.

### Events
Stores church events and registrations.

### Sermons
Stores sermon content and media links.

### Announcements
Stores ministry announcements.

### Subscribers
Stores newsletter subscribers.

---

# 🔄 Application Workflow

## Public User Workflow

```txt
Visitor Opens Website
        │
        ▼
Views Content & Events
        │
 ┌──────┼───────────┐
 ▼      ▼           ▼
Prayer  Register    Subscribe
Request For Event   Newsletter
 │         │            │
 ▼         ▼            ▼
Backend API Processes Request
        │
        ▼
PostgreSQL Database
        │
        ▼
Admin Dashboard Updates
```

---

# 🔁 Admin Workflow

```txt
Admin Login
     │
     ▼
JWT Authentication
     │
     ▼
Admin Dashboard
     │
 ┌───┼───────────────┐
 ▼   ▼               ▼
Manage Events   Manage Sermons
Manage Users    Manage Requests
     │
     ▼
Database Updates
     │
     ▼
Frontend Displays Updated Content
```

---

# 🔄 System Dataflow

```txt
[Frontend UI]
      │
      ▼
[JavaScript Fetch API]
      │
      ▼
[Flask REST API]
      │
 ┌────┼──────────┐
 ▼    ▼          ▼
Auth  Services   Validation
 │    │          │
 ▼    ▼          ▼
[SQLAlchemy ORM]
      │
      ▼
[PostgreSQL Database]
      │
      ▼
[Response Returned to Frontend]
```

---

# 🔐 Authentication Flow

```txt
Admin Login Form
       │
       ▼
Flask Authentication API
       │
       ▼
Password Hash Verification
       │
       ▼
JWT Token Generated
       │
       ▼
Admin Access Granted
```

---

# 📡 API Endpoints

## Authentication
- POST `/api/auth/login`
- POST `/api/auth/register`

## Prayer Requests
- POST `/api/prayers`
- GET `/api/prayers`

## Events
- GET `/api/events`
- POST `/api/events`

## Sermons
- GET `/api/sermons`
- POST `/api/sermons`

---

# 🚀 Deployment Strategy

## Frontend Deployment
Deploy static frontend to:
- Netlify

## Backend Deployment
Deploy Flask backend to:
- Render

## Database
Use:
- PostgreSQL

---

# 📈 Future Improvements

- Real-time livestream notifications
- Mobile app integration
- Member portal
- Online giving integration
- Attendance tracking
- Multi-admin support
- Analytics dashboard

---

# 🧠 Development Principles

This project follows:
- Modular architecture
- Separation of concerns
- REST API principles
- Secure authentication practices
- Responsive-first design
- Scalable backend structure

---

# 🙏 Acknowledgments

Special thanks to:
- Fountain Ministry SA
- Techbridle Foundation
- Open-source community

---

# 👨‍💻 Author

Khulyso John

Software Developer | Full-Stack Learner | Problem Solver

---