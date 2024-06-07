import os

import requests


def send_webhook_notification(webhook_url, directory_path):
    try:
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        '''
            Payload jest przygotowany pod integrację z Matrix Hookshot
            Link do dokumentacji: https://matrix-org.github.io/matrix-hookshot/latest/setup/webhooks.html
        '''
        payload = {
            "text":
                f"---\n\n"
                f"# Faktury zostały wygenerowane.\n\n"
                f"**Zapisano w ścieżce:** {directory_path}\n\n"
                f"**Wygenerowane faktury:**\n\n"
                f"{"\n\n".join(files)}\n\n"
                f"---\n\n"
        }

        response = requests.post(webhook_url, json=payload)

        if 200 <= response.status_code <= 299:
            print(f"Powiadomienie zostało wysłane pomyślnie na {webhook_url}")
        else:
            print(f"Błąd podczas wysyłania powiadomienia: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Wystąpił błąd podczas wysyłania powiadomienia: {e}")
