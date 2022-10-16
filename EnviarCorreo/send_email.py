import smtplib
from email.message import EmailMessage
from kafka.kafka import KafkaConsumerNotificaciones

kafka_consumer_notificaciones = KafkaConsumerNotificaciones()

def send_email_notification():
    notificaciones = kafka_consumer_notificaciones.enviarNotificacion()
    for m in notificaciones:
        body = """
            <!DOCTYPE html>
                <head>
                    <body>
                        <h1>Notificación de Conversión de Audio</h1>

                        <p>Hola <b>{}</b>, </p>
                        <p>El archivo <i>{}</i> ha sido convertido a formato {} exitosamente.</p>
                    </body>
                </head>
            """.format(m['user'],m['file'],m['new_format'])

        # Objeto emailMessage
        message = EmailMessage()

        # Propiedades del mensaje
        email_subject = "Conversor de Audio"
        sender_email_address = "cloud.uniandes.202215@gmail.com"
        receiver_email_address = m['email_user']

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

