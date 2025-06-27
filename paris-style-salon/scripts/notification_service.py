import smtplib
import schedule
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración de base de datos
DATABASE_URL = "sqlite:///./paris_style.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class NotificationService:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = "parisStyle@gmail.com"
        self.sender_password = "tu_password_de_aplicacion"
    
    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        """Envía un email usando SMTP"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'html'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email enviado exitosamente a {to_email}")
            return True
        except Exception as e:
            logger.error(f"Error enviando email a {to_email}: {e}")
            return False
    
    def send_appointment_reminder(self):
        """Envía recordatorios de citas para el día siguiente"""
        db = SessionLocal()
        try:
            # Buscar citas para mañana
            tomorrow = datetime.now() + timedelta(days=1)
            tomorrow_start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
            tomorrow_end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=999999)
            
            query = text("""
                SELECT c.id, c.fecha_hora, u.nombre, u.email, s.nombre as servicio_nombre, 
                       e.nombre as estilista_nombre, s.precio
                FROM citas c
                JOIN usuarios u ON c.cliente_id = u.id
                JOIN servicios s ON c.servicio_id = s.id
                LEFT JOIN estilistas e ON c.estilista_id = e.id
                WHERE c.fecha_hora BETWEEN :start AND :end
                AND c.estado = 'confirmada'
                AND c.id NOT IN (
                    SELECT cita_id FROM notificaciones 
                    WHERE tipo = 'recordatorio' AND enviado = 1
                )
            """)
            
            result = db.execute(query, {
                'start': tomorrow_start,
                'end': tomorrow_end
            })
            
            citas = result.fetchall()
            
            for cita in citas:
                # Crear email de recordatorio
                subject = "Recordatorio de Cita - Paris Style"
                body = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #D97706;">Recordatorio de Cita - Paris Style</h2>
                    <p>Hola <strong>{cita.nombre}</strong>,</p>
                    <p>Te recordamos que tienes una cita programada para mañana:</p>
                    
                    <div style="background-color: #FEF3C7; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #92400E;">Detalles de tu Cita</h3>
                        <p><strong>Servicio:</strong> {cita.servicio_nombre}</p>
                        <p><strong>Fecha:</strong> {cita.fecha_hora.strftime('%d/%m/%Y')}</p>
                        <p><strong>Hora:</strong> {cita.fecha_hora.strftime('%H:%M')}</p>
                        {f'<p><strong>Estilista:</strong> {cita.estilista_nombre}</p>' if cita.estilista_nombre else ''}
                        <p><strong>Precio:</strong> ${cita.precio:,}</p>
                    </div>
                    
                    <p>Si necesitas reagendar o cancelar tu cita, por favor contáctanos con al menos 2 horas de anticipación.</p>
                    
                    <div style="background-color: #F3F4F6; padding: 15px; border-radius: 8px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Dirección:</strong> Calle 123 #45-67, Bogotá</p>
                        <p style="margin: 5px 0 0 0;"><strong>Teléfono:</strong> +57 300 123 4567</p>
                    </div>
                    
                    <p>¡Te esperamos en Paris Style!</p>
                    
                    <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #E5E7EB;">
                        <p style="color: #6B7280; font-size: 12px;">
                            Este es un mensaje automático, por favor no responder a este email.
                        </p>
                    </div>
                </div>
                """
                
                # Enviar email
                if self.send_email(cita.email, subject, body):
                    # Registrar notificación como enviada
                    insert_notification = text("""
                        INSERT INTO notificaciones (usuario_id, cita_id, tipo, mensaje, enviado, fecha_envio)
                        SELECT u.id, :cita_id, 'recordatorio', :mensaje, 1, :fecha_envio
                        FROM usuarios u
                        WHERE u.email = :email
                    """)
                    
                    db.execute(insert_notification, {
                        'cita_id': cita.id,
                        'mensaje': f'Recordatorio enviado para cita del {cita.fecha_hora.strftime("%d/%m/%Y %H:%M")}',
                        'fecha_envio': datetime.now(),
                        'email': cita.email
                    })
            
            db.commit()
            logger.info(f"Procesados {len(citas)} recordatorios de citas")
            
        except Exception as e:
            logger.error(f"Error procesando recordatorios: {e}")
            db.rollback()
        finally:
            db.close()
    
    def send_confirmation_emails(self):
        """Envía emails de confirmación para citas pendientes"""
        db = SessionLocal()
        try:
            # Buscar citas pendientes de confirmación
            query = text("""
                SELECT c.id, c.fecha_hora, u.nombre, u.email, s.nombre as servicio_nombre, 
                       e.nombre as estilista_nombre, s.precio
                FROM citas c
                JOIN usuarios u ON c.cliente_id = u.id
                JOIN servicios s ON c.servicio_id = s.id
                LEFT JOIN estilistas e ON c.estilista_id = e.id
                WHERE c.estado = 'pendiente'
                AND c.fecha_creacion >= :since
                AND c.id NOT IN (
                    SELECT cita_id FROM notificaciones 
                    WHERE tipo = 'confirmacion' AND enviado = 1
                )
            """)
            
            # Buscar citas creadas en las últimas 2 horas
            since = datetime.now() - timedelta(hours=2)
            result = db.execute(query, {'since': since})
            citas = result.fetchall()
            
            for cita in citas:
                subject = "Confirmación de Cita - Paris Style"
                body = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
                    <h2 style="color: #D97706;">¡Cita Agendada Exitosamente!</h2>
                    <p>Hola <strong>{cita.nombre}</strong>,</p>
                    <p>Tu cita ha sido agendada exitosamente en Paris Style.</p>
                    
                    <div style="background-color: #ECFDF5; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #10B981;">
                        <h3 style="margin-top: 0; color: #065F46;">Detalles de tu Cita</h3>
                        <p><strong>Servicio:</strong> {cita.servicio_nombre}</p>
                        <p><strong>Fecha:</strong> {cita.fecha_hora.strftime('%d/%m/%Y')}</p>
                        <p><strong>Hora:</strong> {cita.fecha_hora.strftime('%H:%M')}</p>
                        {f'<p><strong>Estilista:</strong> {cita.estilista_nombre}</p>' if cita.estilista_nombre else ''}
                        <p><strong>Precio:</strong> ${cita.precio:,}</p>
                    </div>
                    
                    <p>Recibirás un recordatorio 24 horas antes de tu cita.</p>
                    
                    <div style="background-color: #FEF2F2; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #EF4444;">
                        <p style="margin: 0; color: #991B1B;"><strong>Política de Cancelación:</strong></p>
                        <p style="margin: 5px 0 0 0; color: #991B1B;">Las cancelaciones deben realizarse con al menos 2 horas de anticipación.</p>
                    </div>
                    
                    <p>¡Esperamos verte pronto en Paris Style!</p>
                </div>
                """
                
                if self.send_email(cita.email, subject, body):
                    # Registrar notificación
                    insert_notification = text("""
                        INSERT INTO notificaciones (usuario_id, cita_id, tipo, mensaje, enviado, fecha_envio)
                        SELECT u.id, :cita_id, 'confirmacion', :mensaje, 1, :fecha_envio
                        FROM usuarios u
                        WHERE u.email = :email
                    """)
                    
                    db.execute(insert_notification, {
                        'cita_id': cita.id,
                        'mensaje': f'Confirmación enviada para cita del {cita.fecha_hora.strftime("%d/%m/%Y %H:%M")}',
                        'fecha_envio': datetime.now(),
                        'email': cita.email
                    })
            
            db.commit()
            logger.info(f"Procesadas {len(citas)} confirmaciones de citas")
            
        except Exception as e:
            logger.error(f"Error procesando confirmaciones: {e}")
            db.rollback()
        finally:
            db.close()

def run_notification_service():
    """Función principal para ejecutar el servicio de notificaciones"""
    notification_service = NotificationService()
    
    # Programar tareas
    schedule.every().day.at("18:00").do(notification_service.send_appointment_reminder)
    schedule.every(30).minutes.do(notification_service.send_confirmation_emails)
    
    logger.info("Servicio de notificaciones iniciado")
    logger.info("Recordatorios programados para las 18:00 diariamente")
    logger.info("Confirmaciones cada 30 minutos")
    
    while True:
        schedule.run_pending()
        time.sleep(60)  # Verificar cada minuto

if __name__ == "__main__":
    run_notification_service()
