import socketserver

buffer_size = 1024


class MyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            # 接收消息
            data = self.request.recv(buffer_size)
            msg = data.decode('utf-8')
            if not data: break
            if msg == 'exit':
                self.request.sendall(data)
            print('msg',self.client_address)

            # 发送消息 将收到的字母转换为大写
            send_msg = msg.upper()
            self.request.sendall(send_msg.encode('utf-8'))

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',8000),MyHandler)
    server.serve_forever()

