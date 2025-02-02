import aiohttp
import smtplib
from email.mime.text import MIMEText
from app.core.config import settings

async def send_notification(channel: str, data: dict) -> bool:
    """
    Send notification through specified channel.
    """
    try:
        if channel == "telegram":
            return await send_telegram_notification(data)
        elif channel == "email":
            return send_email_notification(data)
        elif channel == "discord":
            return await send_discord_notification(data)
        else:
            raise ValueError(f"Unsupported notification channel: {channel}")
    except Exception as e:
        print(f"Error sending notification: {str(e)}")
        return False

async def send_telegram_notification(data: dict) -> bool:
    """
    Send notification via Telegram bot.
    """
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID
    
    message = format_telegram_message(data)
    
    async with aiohttp.ClientSession() as session:
        try:
            url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            payload = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": "HTML"
            }
            
            async with session.post(url, json=payload) as response:
                return response.status == 200
                
        except Exception as e:
            print(f"Telegram notification error: {str(e)}")
            return False

def send_email_notification(data: dict) -> bool:
    """
    Send notification via email.
    """
    try:
        sender = settings.EMAIL_SENDER
        recipient = settings.EMAIL_RECIPIENT
        password = settings.EMAIL_PASSWORD
        
        message = format_email_message(data)
        
        msg = MIMEText(message, 'html')
        msg['Subject'] = f"Memecoin Alert: {data['memecoin_symbol']}"
        msg['From'] = sender
        msg['To'] = recipient
        
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, recipient, msg.as_string())
            
        return True
        
    except Exception as e:
        print(f"Email notification error: {str(e)}")
        return False

async def send_discord_notification(data: dict) -> bool:
    """
    Send notification via Discord webhook.
    """
    webhook_url = settings.DISCORD_WEBHOOK_URL
    
    message = format_discord_message(data)
    
    async with aiohttp.ClientSession() as session:
        try:
            payload = {
                "content": message,
                "username": "Memecoin Alert Bot",
                "avatar_url": "https://your-bot-avatar-url.com/image.png"
            }
            
            async with session.post(webhook_url, json=payload) as response:
                return response.status == 204
                
        except Exception as e:
            print(f"Discord notification error: {str(e)}")
            return False

def format_telegram_message(data: dict) -> str:
    """
    Format notification message for Telegram.
    """
    message = f"""
🚨 <b>Memecoin Alert</b> 🚨

<b>{data['memecoin_name']} ({data['memecoin_symbol']})</b>

Type: {data['alert_type']}

Details:
"""
    
    for key, value in data['trigger_data'].items():
        message += f"• {key}: {value}\n"
    
    message += "\n#memecoin #crypto"
    
    return message

def format_email_message(data: dict) -> str:
    """
    Format notification message for email.
    """
    message = f"""
    <html>
        <body>
            <h2>🚨 Memecoin Alert 🚨</h2>
            <h3>{data['memecoin_name']} ({data['memecoin_symbol']})</h3>
            <p><strong>Alert Type:</strong> {data['alert_type']}</p>
            <h4>Details:</h4>
            <ul>
    """
    
    for key, value in data['trigger_data'].items():
        message += f"<li><strong>{key}:</strong> {value}</li>"
    
    message += """
            </ul>
        </body>
    </html>
    """
    
    return message

def format_discord_message(data: dict) -> str:
    """
    Format notification message for Discord.
    """
    message = f"""
**🚨 Memecoin Alert 🚨**

**{data['memecoin_name']} ({data['memecoin_symbol']})**

Type: {data['alert_type']}

Details:
"""
    
    for key, value in data['trigger_data'].items():
        message += f"• {key}: {value}\n"
    
    message += "\n#memecoin #crypto"
    
    return message 