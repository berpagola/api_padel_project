import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api.endpoints import partidos_router, jugadores_router, torneos_router, auth_router
from app.core.exceptions import APIException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = FastAPI(title="API de Pádel", description="API RESTful para gestionar datos de partidos de pádel")

# Deshabilitar temporalmente la validación de respuesta
app.openapi_schema = None

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ajusta esto según la URL de tu aplicación Next.js
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Outgoing response: Status {response.status_code}")
    return response

app.include_router(partidos_router, prefix="/partidos", tags=["partidos"])
app.include_router(jugadores_router, prefix="/jugadores", tags=["jugadores"])
app.include_router(torneos_router, prefix="/torneos", tags=["torneos"])
app.include_router(auth_router, prefix="/auth", tags=["autenticación"])

@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException):
    logger.error(f"APIException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.get("/")
async def root():
    return {"message": "Bienvenido a la API de Pádel"}

@app.post("/test-partidos/")
async def test_partidos(request: Request):
    logger.info("Test partidos endpoint called")
    body = await request.json()
    logger.info(f"Received body: {body}")
    return {"message": "Test partidos endpoint working"}

logger.info("Application startup complete")