from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib,ssl
import requests 
from requests.auth import HTTPBasicAuth
from email.mime.application import MIMEApplication



def __traer_emails(usuarios):
    text = ', '.join(usuario.email for usuario in usuarios)
    #print(f'emails: {text}')
    return text


def send_mail_for_authorization(pedido, usuarios):
    msg = MIMEMultipart()
    password = "CLARO2019*"
    msg['From'] = "tecnologia@kostazul.com"
    msg['To'] = __traer_emails(usuarios)  
    msg['Subject'] = "Control Compras"
    mensaje = """
    <html>
    <head></head>
    <body>
        <h2>Hola, se ha creado un nuevo pedido y ha sido aprobado por: """ +f'{pedido.usuario_aprobado.first_name} {pedido.usuario_aprobado.last_name}' +"""</h2>
        <h3>Detalles del pedido</h3>
        <h4>Valor estimado pedido: """+f'{pedido.total:,}'+"""</h4>  
        <p>Observaciones: """ +f'{pedido.observaciones}' +"""</p>
        <p>Fecha y usuario de registro: """ +f'{pedido.fecha_registro}- {pedido.usuario_registro.first_name} {pedido.usuario_registro.last_name}' +"""</p>
        <p>Fecha y usuario de aprobacion: """ +f'{pedido.fecha_aprobado}- {pedido.usuario_aprobado.first_name} {pedido.usuario_aprobado.last_name}' +"""</p>
        <p style="color=red;">Por favor Autorizar o recharzar el pedido en el siguiente enlace: <a href=" """ +f'http://wiki.kostazul.com/comprasDetalle/{pedido.id}' +""" ">Autorizacion o Rechazo</a></p>

    </body>
    </html>
    """
    msg.attach(MIMEText(mensaje, 'html'))
    port = 587
    context = ssl.create_default_context()
    with smtplib.SMTP('smtp.office365.com', port) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login('tecnologia@kostazul.com', password)
        server.send_message(msg)