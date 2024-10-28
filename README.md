# User Management

This project provides a simple User Management API built with Django and Django REST Framework. It supports CRUD operations on users, along with pagination for listing users.

The API allows you to:

	•	List users with pagination support
	•	Retrieve a specific user by ID
	•	Create new users
	•	Update existing users
	•	Delete users

The database used is SQLite, making it easy to set up and run locally.

## Spec
The REST specification can be found in the [API Spec](schema.yml) file.
The project uses DRF spectacular for spec generation.
```
./manage.py spectacular --color --file schema.yml
```

## Setup
To run the project, you need to have Python installed

1. Create a virtual environment
```
python -m venv venv
source venv/bin/activate
```

1. Install the dependencies
```
pip install -r requirements.txt
```

1. Carry out database migrations
```
python manage.py migrate
```

1. Start the Django development server
```
python manage.py runserver
```

1. Access the API at http://127.0.0.1:8000/api (users: http://127.0.0.1:8000/api/users)

DRF provides an intuitive UI for basic CRUD operations. 
This can be extended for client usage through templates, or a separate client side app.

### Docker
The project can also be run using Docker.

1. Build the image
```
docker build -t user-management-api .
```

1. Run the container
```
docker run -p 8000:8000 user-management-api
```

## Testing
To run the tests, use the following command:
``` 
python manage.py test
```
    