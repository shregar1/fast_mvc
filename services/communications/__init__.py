"""
High-level communication services (email, SMS, chat, etc.).

This package currently provides an email service abstraction with
pluggable SMTP and SendGrid backends, and a Slack chat abstraction.
Additional providers (Twilio, Teams, etc.) can be added following the same pattern.
"""

from services.communications.email import EmailService
from services.communications.slack import SlackService

__all__ = ["EmailService", "SlackService"]

