# Gestión de Talleres de Formación Profesional

## Descripción del Proyecto

Este proyecto consiste en el desarrollo de una **aplicación web con una API RESTful** para gestionar talleres de formación profesional, como cursos técnicos, capacitaciones prácticas y programas de actualización.

La aplicación permite a:

*  **Estudiantes**: consultar talleres disponibles y registrarse.
*  **Administradores**: crear, modificar y eliminar talleres.

El sistema está construido con **Flask** siguiendo una arquitectura modular y buenas prácticas de desarrollo.

---

##  Tecnologías Utilizadas

* **Backend**: Flask
* **Base de datos**: SQLite (configurable a PostgreSQL o MySQL)
* **ORM**: SQLAlchemy
* **Formato de datos**: JSON
* **Control de versiones**: Git

---

##  Estructura del Proyecto

```
project/
│
├── app.py
├── config.py
├── database.py
├── models.py
├── routes/
│   ├── __init__.py
│   ├── workshops.py
│   └── registrations.py
│
├── requirements.txt
└── README.md
```

---

##  Instalación y Configuración

###  Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/talleres-formacion.git
cd talleres-formacion
```

### 2️ Crear entorno virtual (opcional)

```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

### 3️ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

##  Ejecución de la Aplicación

```bash
python app.py
```

La aplicación estará disponible en:

```
http://127.0.0.1:5000
```

Al iniciarse, Flask crea automáticamente las tablas en la base de datos.

---

##  Endpoints de la API

###  Obtener todos los talleres

```http
GET /workshops
```

###  Obtener un taller por ID

```http
GET /workshops/{id}
```

###  Crear un nuevo taller (Administrador)

```http
POST /workshops
```

###  Modificar un taller (Administrador)

```http
PUT /workshops/{id}
```

###  Eliminar un taller (Administrador)

```http
DELETE /workshops/{id}
```

### Registrar estudiante en un taller

```http
POST /workshops/{id}/register
```
