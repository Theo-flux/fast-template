# FastAPI Production Template
A production-ready FastAPI template with a clean, scalable architecture. This template includes authentication, database migrations, Redis caching, email functionality, and comprehensive error handling out of the box.

## Features
✨ Modern FastAPI - Built with FastAPI for high performance async APIs
🔐 Authentication Ready - Pre-configured auth system with security utilities
🗄️ Database Integration - SQLAlchemy ORM with Alembic migrations
⚡ Redis Support - Built-in Redis integration for caching and sessions
📧 Email System - Template-based email sending capabilities
🛡️ Middleware Stack - Custom middlewares for logging, CORS, and error handling
📝 Structured Logging - Centralized logging configuration
✅ Validation Utilities - Reusable validators and schemas
🎨 Template System - Jinja2 template registry for emails and rendering
⚙️ Environment Config - Centralized configuration management

## Project Structure
```
├── app/
│   ├── core/                  # Core functionality
│   │   ├── authentication.py  # Auth logic and decorators
│   │   ├── config.py          # Environment configuration
│   │   ├── exceptions.py      # Custom exception handlers
│   │   ├── logger.py          # Logging configuration
│   │   ├── mail.py            # Email sending utilities
│   │   ├── middlewares.py     # Custom middleware
│   │   ├── security.py        # Security utilities (hashing, JWT)
│   │   └── template_registry.py  # Template management
│   │
│   ├── database/              # Database layer
│   │   ├── base.py            # SQLAlchemy base and session
│   │   ├── models/            # SQLAlchemy models
│   │   └── redis.py           # Redis client configuration
│   │
│   ├── schemas/               # Pydantic schemas
│   │   ├── auth.py            # Authentication schemas
│   │   ├── base.py            # Base schemas
│   │   └── mail.py            # Email schemas
│   │
│   ├── templates/             # Jinja2 templates
│   │   └── context.py         # Template context processors
│   │
│   ├── utils/                 # Utility functions
│   │   └── validators.py      # Custom validators
│   │
│   └── main.py                # Application entry point
│
├── alembic/                   # Database migrations (Alembic)
├── migrations/                # Alternative migrations folder
├── alembic.ini                # Alembic configuration
├── pyproject.toml             # Python project metadata
└── requirements.txt           # Python dependencies


# Getting Started
## Prerequisites

- Python 3.11+
- PostgreSQL (or your preferred SQL database)
- Redis (optional, for caching)

Installation

Clone the repository
```
git clone https://github.com/Theo-flux/fast-template.git
cd fast-template