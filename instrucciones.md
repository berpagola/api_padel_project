# Proyecto de API RESTful para Resultados de Pádel

Este repositorio contiene el desarrollo de una **API RESTful** construida con **FastAPI** y **PostgreSQL** para gestionar y exponer datos de partidos de pádel. La API recibe datos de un script de web scraping y los almacena en una base de datos estructurada. Además, proporciona endpoints para que aplicaciones cliente puedan acceder a los datos de manera eficiente, incluyendo funcionalidades como autenticación de usuarios a través de Google y envío de notificaciones personalizadas.

## Objetivos del Proyecto

- **Recepción de Datos**: Proporcionar un endpoint que reciba datos de partidos de pádel desde el script de web scraping.
- **Almacenamiento Estructurado**: Guardar los datos en una base de datos relacional bien estructurada, separando la información en entidades correspondientes.
- **Exposición de Datos**: Ofrecer endpoints para listar partidos según diversos criterios (torneo, fecha, jugador, ronda).
- **Autenticación de Usuarios**: Permitir a los usuarios iniciar sesión a través de Google OAuth 2.0.
- **Notificaciones Personalizadas**: Enviar notificaciones a los usuarios sobre partidos de interés próximo a comenzar.
- **Escalabilidad y Mantenimiento**: Diseñar la API de manera modular y escalable, facilitando futuras expansiones o mejoras.

## Tecnologías Utilizadas

- **FastAPI**: Framework moderno y de alto rendimiento para construir APIs con Python 3.7+.
- **PostgreSQL**: Sistema de gestión de bases de datos relacional robusto y escalable.
- **SQLAlchemy**: ORM (Object-Relational Mapping) para interactuar con la base de datos de manera más eficiente.
- **Pydantic**: Para validación de datos y definición de esquemas.
- **OAuth 2.0 y OpenID Connect**: Para autenticación de usuarios a través de Google.
- **Otros**:
  - **Uvicorn**: Servidor ASGI para ejecutar la aplicación FastAPI.
  - **Alembic**: Herramienta para manejar migraciones de la base de datos.
  - **APScheduler**: Para programar tareas como el envío de notificaciones.

## Estructura del Proyecto

```plaintext
api_padel_project/
│
├── README.md
├── requirements.txt
├── .gitignore
├── main.py                     # Punto de entrada de la aplicación
│
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── config.py           # Configuraciones generales y variables de entorno
│   │   └── security.py         # Configuraciones de seguridad y autenticación
│   ├── models/
│   │   ├── __init__.py
│   │   ├── partido.py          # Modelo de la entidad Partido
│   │   ├── jugador.py          # Modelo de la entidad Jugador
│   │   ├── pareja.py           # Modelo de la entidad Pareja
│   │   ├── torneo.py           # Modelo de la entidad Torneo
│   │   ├── cancha.py           # Modelo de la entidad Cancha
│   │   └── round.py            # Modelo de la entidad Round
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── partido.py          # Esquemas Pydantic para Partido
│   │   └── ...                 # Esquemas para las demás entidades
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py             # Dependencias comunes
│   │   ├── endpoints/
│   │   │   ├── __init__.py
│   │   │   ├── partidos.py      # Endpoints para partidos
│   │   │   ├── jugadores.py     # Endpoints para jugadores
│   │   │   ├── torneos.py       # Endpoints para torneos
│   │   │   └── auth.py          # Endpoints para autenticación
│   ├── services/
│   │   ├── __init__.py
│   │   ├── notifications.py    # Lógica para envío de notificaciones
│   │   └── ...                 # Otros servicios necesarios
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py             # Base de datos y sesión
│   │   └── init_db.py          # Inicialización de la base de datos
│   └── utils/
│       ├── __init__.py
│       └── helpers.py          # Funciones auxiliares
│
├── alembic/                    # Directorio para migraciones de base de datos
│   └── ...
│
└── tests/
    ├── __init__.py
    ├── test_partidos.py        # Pruebas unitarias para partidos
    └── ...                     # Otras pruebas
```

## Modelos de Datos

La base de datos está estructurada en varias entidades para representar adecuadamente los datos de los partidos de pádel:

### Entidades Principales

1. **Jugador**:
   - **Campos**: `id`, `nombre`, `apellido`, `nacionalidad`, etc.
   - Representa a cada jugador individualmente.

2. **Pareja**:
   - **Campos**: `id`, `jugador1_id`, `jugador2_id`
   - Relaciona dos jugadores que forman una pareja en un partido.

3. **Torneo**:
   - **Campos**: `id`, `nombre`, `fecha_inicio`, `fecha_fin`, `ubicacion`
   - Contiene información sobre el torneo en el que se juega.

4. **Cancha**:
   - **Campos**: `id`, `nombre`, `torneo_id`
   - Representa las diferentes canchas dentro de un torneo.

5. **Round**:
   - **Campos**: `id`, `nombre` (e.g., "Cuartos de Final", "Semifinal", "Final")
   - Indica la fase del torneo en la que se encuentra el partido.

6. **Partido**:
   - **Campos**: `id`, `fecha`, `hora_inicio`, `estado`, `torneo_id`, `cancha_id`, `round_id`, `pareja1_id`, `pareja2_id`, `sets_pareja1`, `sets_pareja2`, `tipo_horario`, `hora_buenos_aires`
   - Es la entidad principal que relaciona todas las demás entidades.

### Relaciones entre Entidades

- **Jugador** y **Pareja**:
  - Una pareja está compuesta por dos jugadores.
- **Partido** y **Pareja**:
  - Un partido involucra a dos parejas (pareja1 y pareja2).
- **Partido** y **Torneo**:
  - Cada partido pertenece a un torneo.
- **Partido** y **Cancha**:
  - Cada partido se juega en una cancha específica.
- **Partido** y **Round**:
  - Cada partido corresponde a una fase del torneo.

### Posibles Entidades Adicionales

- **Usuario**:
  - Para manejar la autenticación y preferencias de los usuarios.
- **Notificación**:
  - Para registrar las notificaciones enviadas a los usuarios.
- **EstadoPartido** (opcional):
  - Si el campo `estado` tiene valores predefinidos, puede ser útil tener una tabla de estados.

## Especificación de la API

### Endpoints Principales

1. **Recepción de Datos de Partidos** (`POST /partidos/`):
   - Recibe un objeto con la estructura de datos del partido.
   - Procesa los datos y crea o actualiza las entidades correspondientes en la base de datos.
   - Valida que los registros (jugadores, parejas, torneos, canchas, rounds) existan, y los crea si no.

2. **Listado de Partidos por Torneo** (`GET /partidos/torneo/{torneo_id}`):
   - Devuelve una lista de partidos asociados a un torneo específico.

3. **Listado de Partidos por Torneo y Fecha** (`GET /partidos/torneo/{torneo_id}/fecha/{fecha}`):
   - Devuelve una lista de partidos de un torneo en una fecha específica.

4. **Listado de Partidos por Jugador** (`GET /partidos/jugador/{jugador_id}`):
   - Devuelve una lista de partidos en los que ha participado un jugador específico.

5. **Listado de Partidos por Torneo y Round** (`GET /partidos/torneo/{torneo_id}/round/{round_id}`):
   - Devuelve una lista de partidos de un torneo en una fase específica.

### Autenticación y Usuarios

- **Inicio de Sesión con Google** (`POST /auth/google`):
  - Permite a los usuarios autenticarse utilizando su cuenta de Google.
  - Maneja el flujo OAuth 2.0 y OpenID Connect.

- **Gestión de Usuarios**:
  - **Registro de Intereses** (`POST /usuarios/{usuario_id}/intereses`):
    - Permite a los usuarios marcar partidos, jugadores o torneos de interés.
  - **Listado de Intereses** (`GET /usuarios/{usuario_id}/intereses`):
    - Devuelve la lista de intereses del usuario.

### Notificaciones

- **Envío de Notificaciones**:
  - Servicio que, basado en los intereses de los usuarios y los partidos próximos, envía notificaciones.
  - Este servicio puede ser interno y no necesariamente expuesto vía API.

## Detalles de Implementación

### Recepción y Procesamiento de Datos del Partido

El endpoint para recibir datos del partido debe:

- **Validar la Estructura de Datos**:
  - Utilizar `Pydantic` para asegurar que los datos recibidos cumplen con el esquema esperado.
- **Procesar las Entidades Asociadas**:
  - **Torneo**:
    - Si el torneo no existe en la base de datos, crearlo.
  - **Cancha**:
    - Asociada al torneo, verificar si existe o crearla.
  - **Round**:
    - Verificar si el round existe o crearlo.
  - **Jugadores y Parejas**:
    - Para cada jugador en `equipo1` y `equipo2`, verificar si existen y crearlos si no.
    - Crear o recuperar las parejas correspondientes.
- **Crear o Actualizar el Partido**:
  - Una vez todas las entidades asociadas están verificadas, crear el registro del partido en la base de datos.
  - Manejar actualizaciones si el partido ya existe (por ejemplo, si el estado ha cambiado a "Completed" y se tienen los resultados).

### Consideraciones sobre la Base de Datos

- **Integridad Referencial**:
  - Definir claves foráneas entre las entidades para mantener la integridad de los datos.
- **Índices y Optimización**:
  - Crear índices en campos utilizados frecuentemente en consultas (e.g., `jugador_id`, `torneo_id`, `fecha`).
- **Migraciones**:
  - Utilizar **Alembic** para manejar cambios en el esquema de la base de datos de manera controlada.

## Instalación y Configuración

### Requisitos Previos

- **Python 3.7** o superior.
- **PostgreSQL** instalado y configurado.
- **Virtualenv** o similar para manejar entornos virtuales.

### Instalación

1. **Clonar el Repositorio**:

   ```bash
   git clone https://github.com/tu_usuario/api_padel_project.git
   cd api_padel_project
   ```

2. **Crear y Activar el Entorno Virtual**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar Dependencias**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno**:

   - Crear un archivo `.env` en el directorio `app/core/` con las variables necesarias (e.g., cadena de conexión a la base de datos, credenciales de Google OAuth).
   - Ejemplo:

     ```env
     DATABASE_URL=postgresql://user:password@localhost:5432/padel_db
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     SECRET_KEY=your_secret_key
     ```

5. **Inicializar la Base de Datos**:

   - Ejecutar las migraciones para crear las tablas en la base de datos:

     ```bash
     alembic upgrade head
     ```

6. **Ejecutar la Aplicación**:

   ```bash
   uvicorn main:app --reload
   ```

   - La aplicación estará disponible en `http://localhost:8000`.

### Documentación de la API

- FastAPI genera automáticamente documentación interactiva.
- Puedes acceder a ella en `http://localhost:8000/docs` (Swagger UI) o `http://localhost:8000/redoc`.

## Mejores Prácticas y Sugerencias

- **Validación de Datos**:
  - Utilizar Pydantic para definir esquemas y validar los datos entrantes y salientes.
- **Manejo de Excepciones**:
  - Implementar manejo de errores para casos como datos faltantes, conflictos en la base de datos, etc.
- **Autenticación Segura**:
  - Asegurar las rutas que requieren autenticación.
  - Manejar tokens de acceso y refresco de manera segura.
- **Optimización de Consultas**:
  - Utilizar el ORM eficientemente para evitar consultas innecesarias.
  - Considerar el uso de consultas asíncronas si es necesario.
- **Pruebas**:
  - Escribir pruebas unitarias y de integración para asegurar el correcto funcionamiento de los endpoints.
- **Documentación**:
  - Mantener la documentación actualizada.
  - Documentar los modelos y endpoints para facilitar el trabajo de otros desarrolladores.

## Notas Adicionales

- **Seguridad**:
  - Nunca expongas información sensible en el repositorio (usa variables de entorno).
  - Utiliza HTTPS en producción para asegurar las comunicaciones.
- **Escalabilidad**:
  - Diseña la API pensando en posibles aumentos en la carga de datos y usuarios.
- **Logs y Monitoreo**:
  - Implementa logging para registrar eventos importantes y errores.
  - Considera integrar herramientas de monitoreo para supervisar el rendimiento.
- **CORS**:
  - Configura las políticas de CORS adecuadamente si la API será consumida desde el front-end en un dominio diferente.

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Si deseas mejorar este proyecto o agregar nuevas funcionalidades, sigue estos pasos