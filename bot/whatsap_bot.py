import httpx
from config.settings import Settings

def send_whatsapp_message(to_number: str, message: str):
    settings = Settings()
    headers = {
        "Authorization": f"Bearer {settings.whatsapp.access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message}
    }
    response = httpx.post(
        f"https://graph.facebook.com/v17.0/{settings.whatsapp.phone_number_id}/messages",
        json=payload,
        headers=headers
    )
    print(response.status_code, response.text)