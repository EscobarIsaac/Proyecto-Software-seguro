#!/usr/bin/env python3
"""
Bot de Telegram para notificaciones del pipeline CI/CD
Proyecto: Pipeline CI/CD Seguro con ML
"""

import os
import sys
import requests
from datetime import datetime

class TelegramNotifier:
    """Cliente para enviar notificaciones a Telegram"""
    
    def __init__(self):
        self.token = os.environ.get('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.environ.get('TELEGRAM_CHAT_ID')
        
        if not self.token:
            print("⚠️ TELEGRAM_BOT_TOKEN no configurado")
        if not self.chat_id:
            print("⚠️ TELEGRAM_CHAT_ID no configurado")
    
    def send_message(self, message, parse_mode='HTML'):
        """Envía mensaje a Telegram"""
        if not self.token or not self.chat_id:
            print(f"📱 [TELEGRAM MOCK] {message}")
            return True
        
        try:
            url = f"https://api.telegram.org/bot{self.token}/sendMessage"
            data = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode
            }
            
            response = requests.post(url, data=data, timeout=10)
            
            if response.status_code == 200:
                print("✅ Notificación Telegram enviada")
                return True
            else:
                print(f"❌ Error Telegram: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error enviando notificación: {e}")
            return False
    
    def notify_security_scan_start(self, pr_number, branch):
        """Notifica inicio de escaneo de seguridad"""
        message = f"""
🔍 <b>ESCANEO DE SEGURIDAD INICIADO</b>

📋 Pull Request: #{pr_number}
🌿 Branch: {branch}
⏰ Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Estado: Analizando código con modelo ML...
"""
        self.send_message(message)
    
    def notify_security_result(self, pr_number, is_vulnerable, probability, details=""):
        """Notifica resultado del análisis de seguridad"""
        if is_vulnerable:
            icon = "🚨"
            status = "VULNERABILIDAD DETECTADA"
            color = "CRÍTICO"
        else:
            icon = "✅"
            status = "CÓDIGO SEGURO"
            color = "APROBADO"
        
        message = f"""
{icon} <b>{status}</b>

📋 Pull Request: #{pr_number}
📊 Probabilidad de vulnerabilidad: {probability:.1%}
🎯 Resultado: {color}

{details if details else 'Sin detalles adicionales'}
"""
        self.send_message(message)
    
    def notify_vulnerability_critical(self, pr_number, probability, vulnerability_type=""):
        """Notifica vulnerabilidad crítica con detalles"""
        message = f"""
🚨🚨 <b>ALERTA CRÍTICA DE SEGURIDAD</b> 🚨🚨

📋 Pull Request: #{pr_number}
⚠️ Probabilidad: {probability:.1%}
🔴 Nivel: CRÍTICO
{f'🐛 Tipo: {vulnerability_type}' if vulnerability_type else ''}

🛑 <b>ACCIONES REQUERIDAS:</b>
• PR bloqueado automáticamente
• Issue creada y vinculada
• Revisión inmediata necesaria
• NO se permite merge a test

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        self.send_message(message)
    
    def notify_merge_to_test(self, pr_number, success=True):
        """Notifica merge a rama test"""
        if success:
            message = f"""
✅ <b>MERGE A TEST EXITOSO</b>

📋 Pull Request: #{pr_number}
🌿 Destino: test branch
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Siguiente fase: Ejecutando pruebas unitarias...
"""
        else:
            message = f"""
❌ <b>MERGE A TEST FALLIDO</b>

📋 Pull Request: #{pr_number}
🌿 Destino: test branch
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Revisar logs para más detalles.
"""
        self.send_message(message)
    
    def notify_tests_result(self, pr_number, passed, failed, total):
        """Notifica resultado de pruebas"""
        if failed == 0:
            icon = "✅"
            status = "TODAS LAS PRUEBAS PASARON"
        else:
            icon = "❌"
            status = "PRUEBAS FALLIDAS"
        
        message = f"""
{icon} <b>{status}</b>

📋 Pull Request: #{pr_number}
📊 Resultados:
  • Total: {total} pruebas
  • Pasadas: {passed} ✅
  • Fallidas: {failed} ❌

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        self.send_message(message)
    
    def notify_deployment_start(self, environment="production"):
        """Notifica inicio de despliegue"""
        message = f"""
🚀 <b>DESPLIEGUE INICIADO</b>

🌐 Ambiente: {environment}
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Estado: Construyendo imagen Docker...
"""
        self.send_message(message)
    
    def notify_deployment_success(self, url, environment="production"):
        """Notifica despliegue exitoso"""
        message = f"""
🎉 <b>DESPLIEGUE EXITOSO</b> 🎉

🌐 Ambiente: {environment}
🔗 URL: {url}
✅ Estado: Online y funcional
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Pipeline completado exitosamente! 🚀
"""
        self.send_message(message)
    
    def notify_deployment_failed(self, error, environment="production"):
        """Notifica fallo en despliegue"""
        message = f"""
❌ <b>DESPLIEGUE FALLIDO</b>

🌐 Ambiente: {environment}
🔴 Error: {error}
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Revisar logs de despliegue para más detalles.
"""
        self.send_message(message)
    
    def notify_pr_blocked(self, pr_number, reason):
        """Notifica bloqueo de PR"""
        message = f"""
🛑 <b>PULL REQUEST BLOQUEADO</b>

📋 PR: #{pr_number}
❌ Razón: {reason}
🏷️ Etiqueta: fixing-required

<b>Acciones requeridas antes de merge:</b>
• Corregir las vulnerabilidades detectadas
• Re-ejecutar análisis de seguridad
• Solicitar nueva revisión

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        self.send_message(message)


def main():
    """Función de prueba"""
    notifier = TelegramNotifier()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "test":
            print("📱 Enviando mensaje de prueba...")
            notifier.send_message("🧪 <b>Test de notificaciones</b>\n\nBot de Telegram configurado correctamente!")
        
        elif command == "security_start":
            notifier.notify_security_scan_start(123, "dev")
        
        elif command == "security_vulnerable":
            notifier.notify_vulnerability_critical(123, 0.95, "SQL Injection")
        
        elif command == "security_safe":
            notifier.notify_security_result(123, False, 0.15)
        
        elif command == "deployment_success":
            notifier.notify_deployment_success("https://tu-app.onrender.com")
        
        else:
            print("Comandos disponibles: test, security_start, security_vulnerable, security_safe, deployment_success")
    else:
        print("Uso: python telegram_notifier.py [comando]")
        print("Ejemplo: python telegram_notifier.py test")


if __name__ == "__main__":
    main()
