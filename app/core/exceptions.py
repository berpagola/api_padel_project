from fastapi import HTTPException, status

class APIException(HTTPException):
    def __init__(self, status_code: int, detail: str):
        super().__init__(status_code=status_code, detail=detail)

class PartidoNotFoundException(APIException):
    def __init__(self, partido_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"Partido con id {partido_id} no encontrado")

class JugadorNotFoundException(APIException):
    def __init__(self, jugador_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"Jugador con id {jugador_id} no encontrado")

class DatabaseOperationException(APIException):
    def __init__(self, operation: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                         detail=f"Error en la operación de base de datos: {operation}")

class ValidationException(APIException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, 
                         detail=f"Error de validación: {detail}")

class TorneoNotFoundException(APIException):
    def __init__(self, torneo_id: int):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, 
                         detail=f"Torneo con id {torneo_id} no encontrado")