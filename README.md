

author - w2105627
Django Web Application for the 5COSC021W Software Development Project

Sky Engineering Teams Portal

Allows employees and teams to contact each other, arrange meetings and manage the organization and departments.


accounts/ contains the user account functionality, including signup, login, logout and profile management. This keeps authentication separate from the main application logic.

core/ contains the main Sky Engineering Teams application. This includes the database models, forms, views, URL routes, admin registration and tests for teams, departments, organisation data, meetings and audit logging.

static/ contains the static front-end files used by the application, such as the custom CSS and Bootstrap files.

templates/ contains shared HTML templates used across the project, including the base layout and navigation bar. Individual page templates extend these shared files to keep the interface consistent.

w2105627_group_cwk/ contains the main Django project configuration, including settings, project-level URLs, ASGI and WSGI files.

manage.py is the Django command-line file used to run the development server, apply migrations, create users and run tests.

