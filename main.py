import uvicorn
from function.config_manager import ConfigManager
from app.app_init import create_app, create_connection

conn_all = create_connection(ConfigManager)
app = create_app(*conn_all)

if __name__ == "__main__":
    uvicorn.run(app="main:app", host='0.0.0.0', port=ConfigManager.server.port, workers=4, loop="asyncio",
                log_level="info", limit_concurrency=1000)
