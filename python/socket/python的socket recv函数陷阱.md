[TOC]


# 前言
惯例练习历史实验，在编写`tcp`数据流粘包实验的时候，发现一个奇怪的现象。当远程执行的命令返回结果很短的时候可以正常执行，但返回结果很长时，就会发生`json`解码错误，故将排错和解决方法记录下来。

# 一个粘包实验

服务端(用函数）：
```python
import socket
import json
import struct
import subprocess
import sys

from concurrent.futures import ThreadPoolExecutor

def init_socket():
    addr = ('127.0.0.1', 8080)
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(addr)
    server.listen(5)
    print('start listening...')
    return server


def handle(request):
    command = request.decode('utf-8')
    obj = subprocess.Popen(command,
                           shell=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    result = obj.stdout.read() + obj.stderr.read()
    # 如果是win还需要转换编码
    if sys.platform == 'win32':
        result = result.decode('gbk').encode('utf-8')
    return result


def build_header(data_len):
    dic = {
        'cmd_type': 'shell',
        'data_len': data_len,
    }
    return json.dumps(dic).encode('utf-8')


def send(conn, response):
    data_len = len(response)
    header = build_header(data_len)
    header_len = len(header)
    struct_bytes = struct.pack('i', header_len)

    # 粘包发送
    conn.send(struct_bytes)
    conn.send(header)
    conn.send(response)


def task(conn):
    try:
        while True:  # 消息循环
            request = conn.recv(1024)
            if not request:
                # 链接失效
                raise ConnectionResetError

            response = handle(request)
            send(conn, response)

    except ConnectionResetError:
        msg = f'链接-{conn.getpeername()}失效'
        conn.close()
        return msg


def show_res(future):
    result = future.result()
    print(result)


if __name__ == '__main__':
    max_thread = 5
    futures = []
    server = init_socket()

    with ThreadPoolExecutor(max_thread) as pool:
        while True:  # 链接循环
            conn, addr = server.accept()
            print(f'一个客户端上线{addr}')

            future = pool.submit(task, conn)
            future.add_done_callback(show_res)
            futures.append(future)

```

客户端（用类）：
```python
import socket
import struct
import time
import json

class Client(object):
    addr = ('127.0.0.1', 8080)

    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(self.addr)
        print('连接上服务器')

    def get_request(self):
        while True:
            request = input('>>>').strip()
            if not request:
                continue

            return request

    def recv(self):
        # 拆包接收
        struct_bytes = self.socket.recv(4)
        header_len = struct.unpack('i', struct_bytes)[0]
        header_bytes = self.socket.recv(header_len)
        header = json.loads(header_bytes.decode('utf-8'))
        data_len = header['data_len']

        gap_abs = data_len % 1024
        count = data_len // 1024
        recv_data = b''

        for i in range(count):
            data = self.socket.recv(1024)
            recv_data += data
        recv_data += self.socket.recv(gap_abs)

        print('recv data len is:', len(recv_data))
        return recv_data

    def run(self):
        while True:  # 消息循环
            request = self.get_request()
            self.socket.send(request.encode('utf-8'))
            response = self.recv()
            print(response.decode('utf-8'))


if __name__ == '__main__':
    client = Client()
    client.run()
```

# 执行结果
在执行`dir/ipconfig`等命令时可以正常获取结果，但是在执行`tasklist`命令时，发现没有获取完整的执行结果，而且下一条命令将发生报错：
```python
Traceback (most recent call last):
  File "F:/projects/hello/world.py", line 62, in <module>
    client.run()
  File "F:/projects/hello/world.py", line 57, in run
    response = self.recv()
  File "F:/projects/hello/world.py", line 35, in recv
    header = json.loads(header_bytes.decode('utf-8'))
  File "C:\Users\zouliwei\AppData\Local\Programs\Python\Python36\lib\json\__init__.py", line 354, in loads
    return _default_decoder.decode(s)
  File "C:\Users\zouliwei\AppData\Local\Programs\Python\Python36\lib\json\decoder.py", line 339, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
  File "C:\Users\zouliwei\AppData\Local\Programs\Python\Python36\lib\json\decoder.py", line 357, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
```



# 排错思路
1、错误明确指示是`json`的解码发生了错误，解码错误应该是来自于**解码的数据编码不正确**或者读取的**数据不完整**。
2、发生错误的函数在客户端，错误在第`6`行，摘出如下：

```python
 def recv(self):
        # 拆包接收
        struct_bytes = self.socket.recv(4)
        header_len = struct.unpack('i', struct_bytes)[0]
        header_bytes = self.socket.recv(header_len)
        header = json.loads(header_bytes.decode('utf-8'))  # 此行发生错误
        data_len = header['data_len']

        gap_abs = data_len % 1024
        count = data_len // 1024
        recv_data = b''

        for i in range(count):
            data = self.socket.recv(1024)
            recv_data += data
        recv_data += self.socket.recv(gap_abs)

        print('recv data len is:', len(recv_data))
        return recv_data
```
3、继续思考，第`6`行尝试对接收到的头部二进制数据进行`json`解码，而头部二进制在服务器是通过`UTF-8`编码的，查看服务器端编码代码发现没有错误，所以编码错误被排除。剩下的应该就是接收的数据不完整问题。
4、按理说，通过`struct`和`header`来控制每一次读取的字节流可以保证每次收取的时候是准确完整的收取一个消息的数据，但是这里却发生了错误，我通过在下方的`for`函数增加`print`看一下依次循环读取时的长度数据：

```python
for i in range(count):
    data = self.socket.recv(1024)
    print('recv接收的长度是:', len(data))  # 增加此行查看每次循环读取的长度是多少，按理应该是1024
    recv_data += data
```
结果令我意外：
```python
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 400  # 错误
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 400  # 错误
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 400  # 错误
recv接收的长度是: 1024
recv接收的长度是: 1024
recv data len is: 14121
```
按照逻辑，每一次循环应该都收取`1024`字节，却发现有`3`次收取并不完整（每次执行时错误不完全一样，但是都会发生错误），这就是导致最终数据不完整的原因。
因为执行`tasklist`返回的结果很长，导致接收数据不完整，于是下一条执行命令就发生了粘包，`json`解码的数据就不是一个正常的数据，故报错。



# 解决和总结
1、之所以会发生这种情况，我猜测应该是`recv`函数的接收机制原因，`recv`函数一旦被调用，就会尝试获取缓冲中的数据，只要有数据，就会直接返回，如果缓冲中的数据大于`1024`，最多返回`1024`字节，不过如果缓冲只有`400`，也只会返回`400`，这是`recv`函数的读取机制。

2、当客户端需要读取大量数据（执行`tasklist`命令的返回就达到`1w`字节以上）时，需要多次`recv`，每一次`recv`时，客户端并不能保证缓冲中的数据量已经达到`1024`字节（这可能有服务器和客户端发送和接收速度不适配的问题），有可能某次缓冲只有`400`字节，但是`recv`依然读取并返回。


3、最初尝试解决的方法是，在`recv`之前增加`time.sleep(0.1)`来使得每次`recv`之前都有一个充足的时间来等待缓冲区的数据大于`1024`，此方法可以解决问题，不过这方法不是很好，因为如果服务器在远程，就很难控制`sleep`的秒数，因为你不知道网络`IO`会发生多长时间，一旦`sleep`时间过长，就会长期阻塞线程浪费`cpu`时间。


4、查看`recv`函数源码，发现是`c`写的，不过`recv`的接口好像除了`size`之外，还有一个`flag`参数。翻看`《python参考手册》`查找`recv`函数的说明，`recv`函数的`flag`参数可以有一个选项是：`MSG_WAITALL`，书上说，这表示在接收的时候，函数一定会等待接收到指定`size`之后才会返回。


5、最终使用如下方法解决：
```python
for i in range(count):
    # time.sleep(0.1)
    data = self.socket.recv(1024, socket.MSG_WAITALL)
    print('recv接收的长度是:', len(data))
    recv_data += data
```
接收结果：
```python
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv接收的长度是: 1024
recv data len is: 16039
```

6、以后应该还会学习到更好的解决方法，努力学习。