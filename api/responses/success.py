from fastapi.responses import JSONResponse


DELETED_SUCCESSFULLY = JSONResponse(content="Deleted successfully")

DELETED_NOT_SUCCESSFULLY = JSONResponse(content="Deleted not successfully")

TASK_CREATED_FOR_WORKER = JSONResponse(content="Task created for worker")
