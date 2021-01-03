from accounts.models import MailingCredential

domains = {
    'gmail.com': {'smtp_server': 'smtp.gmail.com', 'port': 587, 'use_tls': True},
    'yahoo.com': {'smtp_server': 'smtp.mail.yahoo.com', 'port': 465, 'use_tls': True},
    'hotmail.com': {'smtp_server': 'smtp.live.com', 'port': 465, 'use_tls': True},
    'outlook.com': {'smtp_server': 'smtp.live.com', 'port': 587, 'use_tls': True},
}


def set_mailing_credentials(email, user):
    domain = email.spit("@")[1]
    if domains[domain]:
        pass
    else:
        pass
