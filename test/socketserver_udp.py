import socketserver

class MyHandler(socketserver.BaseRequestHandler):

    def handle(self):
        # 接收消息
        data = self.request[0] # 客户端发来的消息
        msg = data.decode('utf-8')
        if not data: return
        if msg == 'exit':
            self.request[1].sendto(msg.encode('utf-8'),self.client_address)
        print('客户端的消息为：',msg)

        # 发送消息
        send_msg = msg.upper()
        self.request[1].sendto(send_msg.encode('utf-8'),self.client_address)

if __name__ == '__main__':
    server = socketserver.ThreadingUDPServer(('127.0.0.1',8000),MyHandler)
    server.serve_forever()