import socket
import pickle

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5000))
print('Connected!')
buf = 4096

data = client.recv(buf)
data = pickle.loads(data)

k = data[0]
wh = data[1]
numThr = data[2]
w = data[3]
xa = data[4]
xd = data[5]
ya = data[6]
yd = data[7]
h = data[8]
maxIt = data[9]

response = []
for i in range(k, wh, numThr):
    kx = i % w
    ky = int(i / w)
    a = xa + xd * kx / (w - 1.0)
    b = ya + yd * ky / (h - 1.0)
    x = a
    y = b
    for kc in range(maxIt):
        x0 = x * x - y * y + a
        y = 2.0 * x * y + b
        x = x0
        if x * x + y * y > 4:
            red = (kc % 8) * 32
            green = (16 - kc % 16) * 16
            blue = (kc % 16) * 16
            pixel = (kx, ky, red, green, blue)
            response.append(pixel)
            break


data = pickle.dumps(response)
client.send(data)
client.close()
