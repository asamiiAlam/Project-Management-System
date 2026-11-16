#create a 6 digit OTP

def generate_otp():
    import random
    return str(random.randint(100000, 999999))
import resend
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def send_otp_email(email, otp):
    resend.api_key = settings.RESEND_API_KEY

    params = {
        "from": f"PMS <{settings.RESEND_FROM_EMAIL}>",
        "to": [email],
        "subject": "Password Reset OTP",
        "text": (
            f"Your OTP for password reset is: {otp}\n\n"
            "This OTP expires in 5 minutes."
        ),
    }

    try:
        response = resend.Emails.send(params)
        if not response or not response.get("id"):
            logger.error("Resend did not return an email ID.")
            return False

        return True

    except Exception:
        logger.exception("Failed to send OTP using Resend")
        return False