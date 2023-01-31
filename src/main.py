import uvicorn
from app import create_app

app = create_app()

app_base_configs = {'host': '0.0.0.0', 'port': 8090, 'workers': 1, 'access_log': True}

if __name__ == '__main__':
    uvicorn.run('main:app', **app_base_configs)
