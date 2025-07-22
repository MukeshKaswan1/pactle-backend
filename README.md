# EliteStore Backend

A robust Django REST API backend for the EliteStore E-commerce platform. Provides endpoints for products, cart, orders, authentication, Stripe payments, and Slack notifications.

## Features
- Product listing and detail endpoints
- Cart operations (CRUD)
- Order creation and history
- JWT authentication (register/login/profile)
- Stripe payment integration (test mode)
- Order confirmation emails (console/SMTP)
- Slack notifications for new orders
- CORS enabled for frontend integration

## Tech Stack
- [Django](https://www.djangoproject.com/) 4.x
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/)
- [Stripe Python SDK](https://stripe.com/docs/api?lang=python)
- [django-cors-headers](https://github.com/adamchainz/django-cors-headers)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## Getting Started

### 1. Install dependencies
```sh
cd backend
pip install -r requirements.txt
```

### 2. Set up environment variables
Copy `.env.example` to `.env` and fill in your secrets and database credentials:
```sh
cp .env.example .env
```

### 3. Apply migrations
```sh
python manage.py migrate
```

### 4. Create a superuser (optional)
```sh
python manage.py createsuperuser
```

### 5. Run the development server
```sh
python manage.py runserver
```

## Environment Variables
See `.env.example` for all required variables:
- `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`
- `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT`
- `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, `DEFAULT_FROM_EMAIL`
- `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`
- `SLACK_BOT_TOKEN`, `SLACK_CHANNEL_ID`

## Deployment (Render)
- Deploy as a **Web Service** on [Render](https://render.com/):
  - Start Command: `python manage.py runserver 0.0.0.0:$PORT`
  - Set all environment variables in the Render dashboard (use your Render PostgreSQL internal hostname, not `localhost`)
- For production, consider using Gunicorn:
  - Start Command: `gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`

## API Endpoints
- `/api/products/` — List products
- `/api/products/<id>/` — Product detail
- `/api/cart/` — Cart operations (auth required)
- `/api/orders/` — Order operations (auth required)
- `/api/register/` — User registration
- `/api/login/` — JWT login
- `/api/profile/` — User profile (auth required)
- `/api/create-payment-intent/` — Stripe PaymentIntent (auth required)

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

## License
MIT

## Contact
For questions or support, open an issue or contact the maintainer. 