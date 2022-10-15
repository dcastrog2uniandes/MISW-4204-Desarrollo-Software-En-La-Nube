import smtplib
from email.message import EmailMessage

def send_email_notification(params:dict):

    body = """
         <!DOCTYPE html>
            <head>
                <body>
                    <h1>Notificación de Conversión de Audio</h1>

                    <p>Hola <b>{}</b>, </p>
                    <p>El archivo <i>{}</i> ha sido convertido a formato .wav</p>
                </body>
            </head>
        """.format(params['user'],params['file'])

    # Objeto emailMessage
    message = EmailMessage()

    # Propiedades del mensaje
    email_subject = "Conversor de Audio"
    sender_email_address = "cloud.uniandes.202215@gmail.com"
    receiver_email_address = params['user_email']

    # Encabezados del mensaje
    message['Subject'] = email_subject
    message['From'] = sender_email_address
    message['To'] = receiver_email_address

    # Contenido del mensaje
    message.set_content(body,subtype='html')

    # Servdior smtp y puerto
    email_smtp = "smtp.gmail.com"
    server = smtplib.SMTP(email_smtp, '587')

    # Identificar este cliente al servidor SMTP
    server.ehlo()

    # Conexión SMTP segura
    server.starttls()

    # Loguearse en la cuenta de google
    server.login(sender_email_address, 'bprmtqpprjffzpxe')

    # Enviar email
    server.send_message(message)

    # Detener la conexión al servidor
    server.quit()

send_email_notification(
    {
        'user_email':'d.castrog2@uniandes.edu.co',
        'user':'David Castro',
        'file': 'mi_cancion.mp3'
    }
    )