import asyncio
import threading
import uvicorn
from general_util.config_manager import ConfigManager
from grpc import aio

from server.proto import notification_pb2_grpc
from app.app_init import create_app, create_connection
from server.server import NotificationService


ConfigManager.read_yaml("config/config.yaml")
server_config = ConfigManager.server.to_dict()
conn_all = create_connection(ConfigManager)
app = create_app(*conn_all, server_config=server_config)

def start_fastapi_server():
    uvicorn.run(app="main:app", host='0.0.0.0', port=server_config["port"],
                log_level="info", limit_concurrency=1000)

async def start_grpc_server():
    server = aio.server()
    server.add_insecure_port(f'[::]:{server_config["g_port"]}')
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(NotificationService(*conn_all), server)
    await server.start()
    print(f"gRPC server running on port {server_config["g_port"]}...")
    await server.wait_for_termination()


def run_servers():
    fastapi_thread = threading.Thread(target=start_fastapi_server)
    fastapi_thread.start()

    asyncio.run(start_grpc_server())


if __name__ == "__main__":
    run_servers()