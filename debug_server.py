from uvicorn.config import LOGGING_CONFIG
from uvicorn import run

LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s %(levelprefix)s %(message)s"
if __name__ == "__main__":
    run("api.main:app",
        host="127.0.0.1",
        port=5050,
        reload=True,
        log_level="info",
        use_colors=True,
        workers=4,
        reload_dirs=['./api']  # следит за изменениями только в папке api.
        )
