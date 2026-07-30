from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)


async def send_password_reset_email(*, email: str, token: str) -> None:
    reset_url = f"{settings.FRONTEND_URL}/reset-password?token={token}"

    if not settings.SMTP_HOST:
        logger.info(
            "Password reset email (SMTP not configured) for %s: %s",
            email,
            reset_url,
        )
        return

    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText

        message = MIMEMultipart("alternative")
        message["Subject"] = "TruthLens AI - Password Reset"
        message["From"] = settings.SMTP_FROM_EMAIL
        message["To"] = email

        html = f"""
        <html>
          <body>
            <p>You requested a password reset for TruthLens AI.</p>
            <p><a href="{reset_url}">Reset your password</a></p>
            <p>This link expires in {settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES} minutes.</p>
          </body>
        </html>
        """
        message.attach(MIMEText(html, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            if settings.SMTP_USE_TLS:
                server.starttls()
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, email, message.as_string())

        logger.info("Password reset email sent to %s", email)
    except Exception as exc:
        logger.error("Failed to send password reset email: %s", exc, exc_info=True)
