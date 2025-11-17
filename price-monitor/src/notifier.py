import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from config import (
    EMAIL_USER,
    EMAIL_PASS,
    EMAIL_SMTP,
    EMAIL_PORT,
)

from utils import logger


def send_email(subject: str, body: str, to_email: str):
    """
    Envia um e-mail simples (HTML) usando SMTP.
    """
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_USER
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, to_email, msg.as_string())

        logger.info(f"E-mail enviado para {to_email} — assunto: {subject}")

    except Exception as e:
        logger.error(f"Erro ao enviar e-mail: {e}")


def notify_price_drop(results, receiver_email: str):

    matching_products = [
        r for r in results
        if r["success"] and r["price"] is not None and r["price"] <= r["target_price"]
    ]

    if not matching_products:
        logger.info("Nenhum produto atingiu o preço alvo.")
        return False

    # Monta corpo HTML
    html_body = "<h2>Produtos com preço abaixo do alvo</h2><ul>"

    for product in matching_products:
        html_body += f"""
            <li>
                <strong>{product['name']}</strong><br>
                Preço atual: R$ {product['price']:.2f}<br>
                Preço alvo: R$ {product['target_price']:.2f}<br>
                <a href="{product['url']}" target="_blank">Ver produto</a>
            </li>
            <br>
        """

    html_body += "</ul>"

    # Envia email
    send_email(
        subject="📉 Alerta: Preço atingido!",
        body=html_body,
        to_email=receiver_email
    )

    return True
