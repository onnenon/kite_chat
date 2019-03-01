from sanic import Sanic, response
from sanic.log import logger
from sanic.websocket import WebSocketProtocol
from websockets import ConnectionClosed

app = Sanic(__name__)

sockets = []


@app.websocket("/chat")
async def chat(request, ws):
    sockets.append(ws)

    while not ws.closed:
        message = await ws.recv()
        logger.debug({"Message": message})
        for socket in sockets:
            try:
                if socket != ws:
                    await socket.send(message)
            except ConnectionClosed:
                sockets.remove(socket)

    sockets.remove(ws)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True, protocol=WebSocketProtocol)
