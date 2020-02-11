import smtplib
from email.mime.text import MIMEText
# 第三方 SMTP 服务
mail_host = "smtp.qq.com"  # SMTP服务器
mail_user = "493341055"  # 用户名
mail_pass = "pkllovesl0310"  # 授权密码，非登录密码

sender = '493341055@qq.com'# 发件人邮箱(最好写全, 不然会失败)
receivers = ['493341055@qq.com']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱

def sendEmail(title):
    content='股市重大变动通知:\n请注意操作!\n\n\nProduced by 英雄莫问'
    message = MIMEText(title, 'plain', 'utf-8')  # 内容, 格式, 编码
    message['From'] = "{}".format(sender)
    message['To'] = ",".join(receivers)
    message['Subject'] = "来自英雄莫问的邮件"
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 465)  # 启用SSL发信, 端口一般是465
        smtpObj.login(mail_user, mail_pass)  # 登录验证
        smtpObj.sendmail(sender, receivers, message.as_string())  # 发送
        print("通知邮件发送成功！")
    except smtplib.SMTPException as e:
        print(e)
if __name__ == '__main__':
    sendEmail("xxxxxx")