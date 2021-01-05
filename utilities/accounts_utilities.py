from django.core.mail.backends.smtp import EmailBackend
from cryptography.fernet import Fernet

domains = {
    'gmail.com': {'smtp_server': 'smtp.gmail.com', 'port': 587, 'use_tls': True},
    'yahoo.com': {'smtp_server': 'smtp.mail.yahoo.com', 'port': 465, 'use_tls': True},
    'hotmail.com': {'smtp_server': 'smtp.live.com', 'port': 465, 'use_tls': True},
    'outlook.com': {'smtp_server': 'smtp.live.com', 'port': 587, 'use_tls': True},
}


def set_mailing_credentials(email, user):
    from accounts.models import MailingCredential
    domain = email.split("@")[1]
    if domains.get(domain):
        smtp_server = domains[domain]['smtp_server']
        port = domains[domain]['port']
        use_tls = domains[domain]['use_tls']
        mailing_info = MailingCredential.objects.create(smtp_server=smtp_server, port=port, use_tls=use_tls, user=user)
        mailing_info.save()
    else:
        mailing_info = MailingCredential.objects.create(user=user)
        mailing_info.save()


def open_connection(user_mailing_credentials):
    smtp_server = user_mailing_credentials.smtp_server
    port = user_mailing_credentials.port
    email = user_mailing_credentials.email
    password = user_mailing_credentials.password
    use_tls = user_mailing_credentials.use_tls
    connection = EmailBackend(host=smtp_server, port=port, username=email, password=password, use_tls=use_tls)
    return connection
