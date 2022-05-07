import socketserver
import struct

class MyHandler(socketserver.BaseRequestHandler):

    def handle(self):
        print('conn:',self.request)
        print('addr',self.client_address)

        # 实现通信
        while True:
            try:
                # 接收消息
                # ----------解决接收粘包------------
                total_length = self.request.recv(4)
                data_length = struct.unpack('i',total_length)[0]
                recv_size = 0
                recv_msg = b''
                while recv_size < data_length:
                    recv_msg += self.request.recv(1024)
                    recv_size = len(recv_msg)
                # ----------解决接收粘包------------
                data = recv_msg.decode('utf-8')
                if not data: break
                if data == 'exit':
                    send_msg = 'exit'
                    # ----------解决发送粘包------------
                    data_length = len(send_msg)
                    total_length = struct.pack('i', data_length)
                    self.request.sendall(total_length)
                    # ----------解决发送粘包------------
                    self.request.sendall(send_msg.encode('utf-8'))
                    self.request.close()
                    break
                print('收到的消息为：',data,self.client_address)

                # 发送消息 将收到的消息转换为大写
                # ----------解决发送粘包------------
                send_msg = data.upper()
                data_length = len(send_msg)
                total_length = struct.pack('i',data_length)
                self.request.sendall(total_length)
                # ----------解决发送粘包------------
                self.request.sendall(send_msg.encode('utf-8'))
            except Exception as e:
                print(e)
                break

if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1',8000),MyHandler)
    server.serve_forever() # 实现连接循环