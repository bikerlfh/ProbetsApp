# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Probetspp is a table tennis betting prediction platform with a Django REST backend and React TypeScript frontend. It collects game data via web scrapers (Flashscore, Yajuego), processes it through ML-based prediction algorithms, and serves predictions through a REST API.

## Development Commands

### Backend (Docker-based)

```bash
# Build and run
make build                    # Build Docker containers
make up                       # Start all services (PostgreSQL, Django, Nginx)
make down                     # Stop all services

# Database
make migrate                  # Run Django migrations
make makemigrations           # Create new migrations
make reset-db                 # Reset database
make init-db                  # Reset + migrate + load fixtures

# Development
make shell                    # Django shell_plus
make create-superuser         # Create admin user
make create-predictions       # Run prediction generation

# Testing
make run-tests                # Run pytest in Docker
make run-tests args="-k test_name"  # Run specific test

# Code quality
make black                    # Format code (line-length=79)
make dev-check                # Run pre-commit hooks
```

### Frontend

```bash
cd probetspp_front
npm start                     # Development server (port 3000)
npm test                      # Run Jest tests
npm run build                 # Production build
```

## Architecture

### Backend Structure (`probetspp/`)

Django apps follow a service-layer pattern:
- **apps/core** - Base models (`BaseModel` abstract class), shared utilities
- **apps/games** - Game, Player, League, PlayerStats models and APIs
- **apps/predictions** - Prediction engine, confidence scoring algorithms
- **apps/data** - ML weights (`DataWeights`), calculated scores (`DataGame`), acceptance thresholds
- **apps/third_parties** - Web scrapers:
  - `flashscore/` - Flashscore data connector
  - `yajuego/` - Yajuego scraper
  - `chrome_custom.py` - Selenium/Chrome driver wrapper
- **apps/utils** - Helpers, formatters, S3 integration

Each app typically contains:
- `models.py` - Django models
- `services.py` - Business logic
- `selectors.py` - Complex database queries
- `serializers.py` - DRF serializers
- `filters.py` - django-filter configurations
- `views.py` - API endpoints

### Frontend Structure (`probetspp_front/`)

React app with Redux state management:
- **containers/** - Page components (DashBoardView, LoginView, GameDetailView, PredictionView)
- **components/** - Reusable UI (GameRow, GameList, GamesChart, PredictionBarChart, RadarChart)
- **api/** - REST client (`APIRest.tsx`), endpoints (`constants.tsx`)
- **actions/** - Redux thunks (auth.js, games.js, dashboard.js)
- **reducers/** - Redux state slices with localStorage persistence
- **types/** - TypeScript interfaces

### Infrastructure

- **Docker Compose**: PostgreSQL 13, Django app (port 8000), Nginx reverse proxy (ports 80, 8081)
- **AWS Lambda**: Zappa deployment with scheduled tasks (game updates every 10min, predictions every 25min)
- **Storage**: S3 for file storage via django-storages

## Code Style

- Python: Black formatter, line-length 79
- Flake8: Ignores W503, F405; excludes migrations and settings
- TypeScript: Standard React/ESLint configuration

## Key Dependencies

**Backend**: Django 3.1.7, DRF 3.12.2, django-filter, Django-Q (task queue), Selenium, Pandas, Boto3

**Frontend**: React 18, Redux Toolkit, React Router 6, Chart.js, TypeScript

## Environment Variables

Required for production (see README.md):
- `DATABASE_HOST`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_PORT`
- `ALLOWED_HOSTS`, `ENVIRONMENT`, `BUCKET_FILES`, `SENTRY_URL`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
