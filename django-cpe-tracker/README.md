# Django CPE Tracker

This project is a Django web application for tracking continuing education credits.

## Features

- User authentication
- Add, edit, and delete continuing education activities
- Track credits by category and date
- Dashboard for credit summary

## Setup

1. Create a virtual environment:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Run initial migrations:

   ```sh
   python manage.py migrate
   ```

4. Create a superuser:

   ```sh
   python manage.py createsuperuser
   ```

5. Start the development server:

   ```sh
   python manage.py runserver
   ```

## Development

- All code should follow PEP8 standards.
- Use environment variables for sensitive settings.

## License

MIT
