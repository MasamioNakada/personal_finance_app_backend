# Personal Finance Backend

## Description / Descripción

A Django REST API for personal finance management. This project provides endpoints for managing personal finances, including expense tracking, budgeting, and financial analytics.

Una API REST de Django para la gestión de finanzas personales. Este proyecto proporciona endpoints para administrar finanzas personales, incluyendo seguimiento de gastos, presupuestos y análisis financiero.

## Features / Características

- User Authentication / Autenticación de usuarios
- JWT Token based security / Seguridad basada en tokens JWT
- Swagger Documentation / Documentación con Swagger
- RESTful API endpoints / Endpoints API RESTful

## Requirements / Requisitos

- Python 3.8+
- Django 4.2
- Django REST Framework
- SQLite (default) or other supported database

## Local Installation / Instalación Local

1. Clone the repository / Clonar el repositorio:
```bash
git clone [repository-url]
cd personal_finance_backend
```

2. Create and activate virtual environment / Crear y activar entorno virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # On Unix or MacOS
.venv\Scripts\activate    # On Windows
```

3. Install dependencies / Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Set up environment variables / Configurar variables de entorno:
```bash
cp .env.example .env
# Edit .env with your configuration / Edita .env con tu configuración
```

5. Run migrations / Ejecutar migraciones:
```bash
python manage.py migrate
```

6. Create superuser / Crear superusuario:
```bash
python manage.py createsuperuser
```

7. Run the development server / Ejecutar el servidor de desarrollo:
```bash
python manage.py runserver
```

## Docker Installation / Instalación con Docker

1. Build and run with Docker Compose / Construir y ejecutar con Docker Compose:
```bash
docker-compose up --build
```

2. Create superuser in Docker / Crear superusuario en Docker:
```bash
docker-compose exec web python manage.py createsuperuser
```

## API Documentation / Documentación de la API

Once the server is running, you can access the API documentation at:
Una vez que el servidor esté en funcionamiento, puedes acceder a la documentación de la API en:

- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## Contributing / Contribuir

Contributions are welcome! Please feel free to submit a Pull Request.
¡Las contribuciones son bienvenidas! No dudes en enviar un Pull Request.

## License / Licencia

This project is licensed under the MIT License - see the LICENSE file for details.
Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.