import asyncio
import grpc
from server.proto import notification_pb2_grpc, notification_pb2

async def run():
    async with grpc.aio.insecure_channel('localhost:59380') as channel:
        stub = notification_pb2_grpc.NotificationServiceStub(channel)
        response = await stub.SendEmail(notification_pb2.EmailSendRequest(sender="test", subject="test", message="test"))
        print(f"notification client received: {response.message}")

if __name__ == '__main__':
    asyncio.run(run())