import uvicorn
from app import create_app
from settings import PORT, UVICORN_WORKERS

app = create_app()

app_base_configs = {
    "host": "0.0.0.0",
    "port": 8090,
    "workers": 1,
    "access_log": True,
    #"log_config": "logging.ini",
    "timeout_notify": 2
}

if __name__ == "__main__":
    uvicorn.run("main:app", **app_base_configs)