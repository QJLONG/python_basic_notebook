from email.header import Header  # 对中文编码
from email.mime.text import MIMEText # 邮件对象
from email.utils import parseaddr,formataddr # 格式化邮箱
import smtplib # 发送邮件

# 格式化邮箱，不格式化会被放进垃圾邮箱或者发送失败
def format_addr(s):
    name,addr = parseaddr(s)  # 比如 hummer,<hzlqjmct@163.com>
    return formataddr((Header(name,'utf-8').encode('utf-8'),addr))

# 准备数据
from_addr = 'hzlqjmct@163.com' # 发件人

password = 'HMASTUMSFBQAKHPH' # 授权码

smtp_server = 'smtp.163.com' # 163服务器

to_addr = input('收件人邮箱：') # 收件人

# ------------构建一个发送内容对象---------start--------

msg = MIMEText("来自hummer的亲切问候","plain","utf-8")
# 标准邮件需要三个头部信息，From，To，Subject
msg["From"] = format_addr(u'hummer<%s>'%from_addr) # 发件人
to_name = input('收件人名称：')
msg["To"] = format_addr(u'{}<%s>'.format(to_name) % to_addr) # 收件人
msg['Subject'] = Header(u'email_test','utf-8').encode('utf-8') # 标题

# ------------构建一个发送内容对象---------end--------


# ------------发送-----------------start---------

server = smtplib.SMTP(smtp_server,25) # 163smtp服务默认端口为25
server.set_debuglevel(1) # 是否显示发送日志，1显示，0不显示
server.login(from_addr,password) # 登录邮箱
server.sendmail(from_addr,[to_addr],msg.as_string()) # 发送

# ------------发送-----------------end-----------