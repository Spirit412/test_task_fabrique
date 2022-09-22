from fastapi import HTTPException, status
from fastapi.responses import JSONResponse

###################   SQLALCHEMY   ###################


def raise_client_not_found(client_id: int) -> JSONResponse:
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content=f"Client ID:{client_id} not found")
