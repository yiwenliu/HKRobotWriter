#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by yiwen on 2017/4/23

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


def send_email(body, subject):
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = Header("机器人写稿程序", 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    from_addr = 'airlyw@hotmail.com'
    password = '13b@qre381'
    to_addr = ['xinhua381@hotmail.com']
    #to_addr = ['gjleaf@hotmail.com']
    smtp_server = 'smtp-mail.outlook.com'
    smtp_port = 587
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
        return True
    except smtplib.SMTPException:
        return False
