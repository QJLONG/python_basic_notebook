from socket import *
import subprocess
import struct # 封包 拆包

ip_port = ('127.0.0.1',8000)
back_log = 5
buffer_size = 1024

# 创建socket链接 tcp协议
cmd_server = socket(AF_INET,SOCK_STREAM)

# 绑定ip端口
cmd_server.bind(ip_port)

# 设置最大链接数
cmd_server.listen(back_log)

# 外层循环
while True:
    # 得到一个持续链接和客户端的地址
    conn,addr = cmd_server.accept()

    # 通信循环（内层循环）
    while True:
        # 防止客户端异常中断
        try:
            # 接收客户端的消息
            cmd = conn.recv(buffer_size)
            # 客户端输入空 中断该链接
            if not cmd:
                break
            print('客户端的指令是：',cmd.decode('utf-8'))

            # 执行指令
            '''
                args参数为：指令序列或者字符串指令
                shell=Ture参数为：True是指指令为字符串，False指指令为指令序列 默认为False
                stderr:stderr=subprocess.PIPE返回一个file，可以直接展示个客户端，返回错误通道信息 默认为None
                stdin:  返回标准输入通道信息
                stdout:  返回标准通道信息
            '''
            cmd_result = subprocess.Popen(cmd.decode('utf-8'),shell=True,
                             stderr=subprocess.PIPE,
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)

            '''
                从cmd发送命令后，可能返回的结果有：
                    1.错误指令，返回错误通道信息
                    2.正确指令，返回标准通道信息
                        a.指令成功执行，返回空 如：cd .  cd ..
                        b.指令成功执行，返回不为空
            '''
            # 从错误通道获取信息
            err_msg = cmd_result.stderr.read()

            # 如果错误通道有消息，返回给客户端
            if err_msg:
                msg = err_msg
            # 如果错误通道没有消息，获取标准通道消息并返回给客户端
            else:
                msg = cmd_result.stdout.read() # 从标准通道获取信息

            # 执行正确指令并返回空的情况
            if not msg:
                msg = '执行成功'.encode('gbk') # 返回客户端友好提示

            # -----------------------解决粘包-----------------------
            '''
                为字节流加上自定义固定长度报头，报头中包含字节流长度，
                然后一次send到接收端，接收端先从缓存中取出定长报头，
                然后取得真实数据
            '''
            length = len(msg)
            # i 为四字节封装格式 length为报文长度
            data_length = struct.pack('i',length) # 封包
            conn.send(data_length) # 向接收端发送带有报头的字节流长度
            # -----------------------解决粘包-----------------------

            conn.send(msg)
        except Exception as e:
            print('程序发生异常，异常信息为：',e)
            break

    # 与客户端断开连接
    conn.close()
# 关闭服务端
cmd_server.close()