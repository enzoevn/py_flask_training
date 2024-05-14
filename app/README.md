# My Flask App

This is a simple Flask application with a login page.

## Project Structure

The project has the following structure:

```
my-flask-app
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── templates
│   │   ├── index.html
│   │   └── login.html
│   └── static
│       ├── css
│       │   └── main.css
│       └── js
│           └── main.js
├── config.py
├── run.py
└── README.md
```

## Files

- `app/__init__.py`: Initializes the Flask application.
- `app/routes.py`: Defines the routes for the application.
- `app/templates/index.html`: The main page of the application.
- `app/templates/login.html`: The login page.
- `app/static/css/main.css`: Contains the CSS styles for the application.
- `app/static/js/main.js`: Contains the JavaScript code for the application.
- `config.py`: Contains the configuration settings for the Flask application.
- `run.py`: Used to start the Flask application.

## Running the Application

To run the application, execute the following command:

```
python run.py
```

This will start the Flask development server, and the application will be available at `http://localhost:5000`.

## Login

To log in to the application, go to `http://localhost:5000/login` and enter your credentials. After successful login, you will be redirected to the main page.