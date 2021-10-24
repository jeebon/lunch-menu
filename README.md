# Installation
```bash
docker-compose up
```

Server: localhost:8000

# Create Super User:
```bash
docker-compose run app sh -c "python manage.py createsuperuser"
```

##Testing:
```bash
docker-compose run app sh -c "python manage.py test"
```

##Linting:
```bash
docker-compose run app sh -c " flake8"
```