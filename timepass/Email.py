import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login("theevilsharma009@gmail.com", "Cloud1234")

msg = "YOUR MESSAGE!"
server.sendmail("theevilsharma009@gmail.oom", "sapan2211@yahoo.com", msg)
server.quit()
