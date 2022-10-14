import threading
import socket
import pickle
from PIL import Image

w = 600  # image width
h = 600  # image height
image = Image.new("RGB", (w, h))
wh = w * h
maxIt = 50

xa = -2.0
xb = 1.0
ya = -1.5
yb = 1.5
xd = xb - xa
yd = yb - ya
numThr = int(input('How many clients do you want: '))

host = '127.0.0.1'
port = 5000
buf = 4096

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


collected = []


def handle(client, k):
    try:
        info = (k, wh, numThr, w, xa, xd, ya, yd, h, maxIt)
        data = pickle.dumps(info)
        client.send(data)

        total_data = []
        while True:
            data = client.recv(buf)
            if not data:
                break
            total_data.append(data)
        data = b''.join(total_data)
        data = pickle.loads(data)
        for item in data:
            collected.append(item)
    except:
        print('error')


print(f'Server started! Waiting for {numThr} connections...')
clients = []
while len(clients) < numThr:
    client, address = server.accept()
    print(f'{str(address)} CONNECTED')
    clients.append(client)

print(f'{numThr} clients connected! Calculations starting...')

threads = []
for k in range(numThr):
    thread = threading.Thread(target=handle, args=(clients[k], k,))
    threads.append(thread)

for k in range(numThr):
    threads[k].start()

for k in range(numThr):
    threads[k].join()

for pixel in collected:
    image.putpixel((pixel[0], pixel[1]), (pixel[2], pixel[3], pixel[4]))
image.save('fractal.png', 'PNG')
print('Image saved!')
server.close()
