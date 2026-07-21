"""
DrugAI — Celery tasks for sending emails.
"""
from __future__ import annotations

import time
from celery import shared_task

from core.logging import get_logger

log = get_logger(__name__)

import smtplib
from email.message import EmailMessage
from core.config import settings

@shared_task
def send_verification_email(email: str, token: str):
    """Send a verification email using SMTP."""
    log.info("sending_verification_email", email=email)
    
    if not settings.EMAIL_ENABLED:
        log.info("email_disabled_skipping_send", email=email)
        return {"status": "skipped_disabled", "type": "verification", "to": email}
        
    try:
        msg = EmailMessage()
        msg['Subject'] = f"{settings.EMAILS_FROM_NAME} - Verify your account"
        msg['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg['To'] = email
        
        # Link would normally point to frontend route, mocked here
        link = f"http://localhost:5173/verify?token={token}"
        msg.set_content(f"Welcome to DrugAI! Please verify your account by clicking here: {link}")
        
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            if settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            
        log.info("verification_email_sent", email=email)
        return {"status": "sent", "type": "verification", "to": email}
    except Exception as e:
        log.error("verification_email_failed", email=email, error=str(e))
        return {"status": "failed", "type": "verification", "to": email, "error": str(e)}

@shared_task
def send_password_reset_email(email: str, token: str):
    """Send a password reset email using SMTP."""
    log.info("sending_password_reset_email", email=email)
    
    if not settings.EMAIL_ENABLED:
        log.info("email_disabled_skipping_send", email=email)
        return {"status": "skipped_disabled", "type": "password_reset", "to": email}
        
    try:
        msg = EmailMessage()
        msg['Subject'] = f"{settings.EMAILS_FROM_NAME} - Password Reset Request"
        msg['From'] = f"{settings.EMAILS_FROM_NAME} <{settings.EMAILS_FROM_EMAIL}>"
        msg['To'] = email
        
        link = f"http://localhost:5173/reset-password?token={token}"
        msg.set_content(f"You requested a password reset. Click here to reset: {link}")
        
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            if settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
            
        log.info("password_reset_email_sent", email=email)
        return {"status": "sent", "type": "password_reset", "to": email}
    except Exception as e:
        log.error("password_reset_email_failed", email=email, error=str(e))
        return {"status": "failed", "type": "password_reset", "to": email, "error": str(e)}
