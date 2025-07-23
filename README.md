# 🗺️ Map My World - Geolocalización con FastAPI y Docker

Este proyecto es una Rest API desarrollada con **FastAPI**, que permite administrar ubicaciones geográficas 
categorizadas y obtener recomendaciones sobre las mismas segun el criterio del administrador. 

El proyecto está dockerizado para facilitar el despliegue y el desarrollo.


## 🚀 Características principales

- Crear ubicaciones con coordenadas, nombre, descripción y categorías asociadas.
- Crear y listar categorías.
- Asociar ubicaciones con categorías.
- Marcar combinaciones de ubicación y categoría como "revisadas".
- Obtener recomendaciones frescas: hasta 10 combinaciones ubicación-categoría que no han sido revisadas en los últimos 30 días.
- Interfaz básica con mapa utilizando HTML y Jinja2.
- Base de datos SQLite.
- Contenedor Docker preconfigurado con Docker Compose.

---


## 🐳 Docker & Docker Compose

### 📄 `Dockerfile`

El `Dockerfile` crea una imagen ligera basada en `python:3.11-slim`:

Si ya tienes instalado docker, para correr la rest api, solo necesitas ejecutar:
```sudo docker compose up```
eso levantará la aplicación y podrás acceder a ella en `http://localhost:8000`.

Si aun no lo tienes instalado y deseas correr la api en Docker, puedes seguir las siguentes instrucciones:

### Instrucciones para correr la aplicación en Docker
https://www.hostinger.com/co/tutoriales/como-instalar-y-usar-docker-en-ubuntu

---

## 📝 Requisitos (si corres sin Docker)
Si decides correr sin Docker:

Crea un entorno virtual con: ```python3 -m venv venv```, 
activa el entorno vitual ```source venv/bin/activate``` 
instala las dependencias necesarias:  ```pip install -r requirements.txt``` 
desde la terminal ubícate a la altura de main.py e inicializa el servidor uvicorn : ```uvicorn main:app --reload``` 
accede a la aplicación en `http://localhost:8000`.
---


### 📜 Rutas del API

| Método | Ruta                    | Descripción                                     |
| ------ |-------------------------|-------------------------------------------------|
| GET    | `/`                     | Página principal con el mapa                    |
| GET    | `/docs`                 | Documentacion interactiva Swager                |
| POST   | `/locations/`           | Crear una nueva ubicación                       |
| GET    | `/list/locations`       | Listar todas las ubicaciones                    |
| POST   | `/categories/`          | Crear una nueva categoría                       |
| GET    | `/categories/`          | Listar todas las categorías                     |
| POST   | `/location-categories/` | Asociar una ubicación con una categoría         |
| POST   | `/reviews/`             | Marcar una ubicación-categoría como revisada    |
| GET    | `/recommendations/`     | Obtener 10 combinaciones que necesitan revisión |
```



## 🧱 Estructura del proyecto

```map_my_world/
├── db/ # Configuración y conexión de base de datos
│ └── database.py
├── models/ # Modelos ORM SQLAlchemy
│ └── models.py
├── routes/ # Rutas principales del API
│ └── crud_routes.py
├── schemas/ # Esquemas de entrada/salida con Pydantic
│ └── schemas.py
├── templates/ # Plantillas HTML (Jinja2)
│ └── map.html
├── utils/ # Lógica auxiliar, categorías por defecto, recomendaciones
│ └── default_categories.py
│ └── fresh_recommendations.py
├── main.py # Punto de entrada principal de la app
├── Dockerfile # Imagen personalizada de la app
├── docker-compose.yml # Orquestación de servicios
├── requirements.txt # Dependencias Python
└── README.md # Este archivo```