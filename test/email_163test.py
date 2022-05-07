from email.header import Header
from email.mime.text import MIMEText
from email.utils import formataddr,parseaddr
import smtplib

# 创建邮箱地址格式化方法
def format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name,'utf-8').encode('utf-8'),addr))

# 准备数据
from_addr = 'hzlqjmct@163.com'
password = 'HMASTUMSFBQAKHPH'
smtp_server = 'smtp.163.com'
to_addr = input('收件地址：')
to_name = input('收件人名称：')
subject = input('主题：')
content = input('内容：')

# ----------创建邮件发送对象--------start--------

msg = MIMEText(content,"plain","utf-8")
# 标准邮箱头的三个要素
msg["From"] = format_addr("hummer<%s>"%from_addr)
msg["To"] = format_addr("{}<{}>".format(to_name,to_addr))
msg["Subject"] = Header(subject,'utf-8')

# ----------创建邮件发送对象--------end----------


# ---------发送--------start-----------------

server = smtplib.SMTP(smtp_server,25)
server.set_debuglevel(1)
server.login(from_addr,password)
server.sendmail(from_addr,to_addr,msg.as_string())

# ---------发送--------end-------------------


