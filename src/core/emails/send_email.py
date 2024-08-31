from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from core.settings.common import EMAIL_HOST_USER


def send_html_email(subject: str, recipients, template_name: str, context: dict):
    subject = subject
    from_email = EMAIL_HOST_USER
    to = [recipients]

    # Render HTML email content
    html_content = render_to_string(template_name, context)
    # Plain text email content
    text_content = strip_tags(html_content)

    # Create the email and attach the HTML version
    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
