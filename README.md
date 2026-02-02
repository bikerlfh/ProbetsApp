# Probetspp

Table tennis betting prediction platform with a Django REST API backend and React TypeScript frontend.

> **Note**: This project was created in 2021 and is no longer maintained or supported.

## Disclaimer

This project was created for **educational purposes only**. It is intended as a learning exercise in web development, data analysis, and machine learning techniques.

**Regarding betting**: This software does not encourage, promote, or facilitate real-money gambling. The predictions generated are purely illustrative and should not be used for actual betting decisions. Gambling involves significant financial risk and may be illegal in your jurisdiction. The authors are not responsible for any financial losses or legal consequences resulting from the misuse of this software.

## Prerequisites

- Docker & Docker Compose
- Node.js 15+ (for frontend development)
- Python 3.10+ (for local development without Docker)

## Quick Start

### Backend

```bash
# Build and start services (PostgreSQL, Django, Nginx)
make build
make up

# Initialize database
make migrate
make create-superuser

# Access the API at http://localhost:8081
```

### Frontend

```bash
cd probetspp_front
npm install
npm start

# Access the app at http://localhost:3000
```

## Development

### Common Commands

```bash
# Database
make migrate                  # Run migrations
make makemigrations           # Create migrations
make reset-db                 # Reset database
make init-db                  # Reset + migrate + load fixtures
make shell                    # Django shell_plus

# Testing
make run-tests                # Run all tests
make run-tests args="-k test_name"  # Run specific test

# Code quality
make black                    # Format Python code
make dev-check                # Run pre-commit hooks

# Predictions
make create-predictions       # Generate predictions manually
```

### Frontend Commands

```bash
cd probetspp_front
npm start                     # Development server
npm test                      # Run tests
npm run build                 # Production build
```

## Project Structure

```
probetspp/
├── probetspp/               # Django project
│   ├── apps/               # Application modules
│   │   ├── core/          # Base models, utilities
│   │   ├── games/         # Game, Player, League models
│   │   ├── predictions/   # Prediction engine
│   │   ├── data/          # ML weights, analysis
│   │   ├── third_parties/ # Web scrapers (Flashscore, Yajuego)
│   │   └── utils/         # Helpers, S3 integration
│   └── probetspp/         # Settings & configuration
├── probetspp_front/        # React TypeScript frontend
├── config/                 # Nginx, Gunicorn, entrypoint
├── requirements/           # Python dependencies
├── Dockerfile
├── docker-compose.yml
└── makefile
```

## Deployment

### AWS Lambda (Zappa)

```bash
zappa deploy dev
```

Required environment variables:
- `ALLOWED_HOSTS`
- `BUCKET_FILES`
- `DATABASE_HOST`, `DATABASE_NAME`, `DATABASE_USER`, `DATABASE_PASSWORD`, `DATABASE_PORT`
- `ENVIRONMENT=production`
- `SENTRY_URL`
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

### Chromeless Setup

For headless Chrome on AWS Lambda, install [chromeless](https://pypi.org/project/chromeless/) and configure the Lambda function (default name: `chromeless-server-prod`).

Add Lambda environment variable: `TZ=America/Bogota`

## Scheduled Tasks

When deployed to AWS Lambda via Zappa:
- `update_old_scheduled_games` - Daily at 5:05 AM
- `update_events_data` - Every 10 minutes
- `create_periodical_prediction` - Every 25 minutes

## Tech Stack

**Backend**: Django 3.1, Django REST Framework, PostgreSQL, Django-Q, Selenium, Pandas

**Frontend**: React 18, TypeScript, Redux Toolkit, React Router, Chart.js

**Infrastructure**: Docker, Nginx, Gunicorn, AWS Lambda/Zappa, S3
