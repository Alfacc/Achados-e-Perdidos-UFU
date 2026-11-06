from django.conf import settings
from django.core.exceptions import ValidationError


def validate_ufu_email(value: str) -> None:
    """Aceita apenas e-mails dos domínios institucionais configurados."""
    domain = value.rsplit("@", 1)[-1].strip().lower()
    allowed = [d.lower() for d in settings.ALLOWED_EMAIL_DOMAINS]
    if not any(domain == d or domain.endswith("." + d) for d in allowed):
        raise ValidationError(
            "Use seu e-mail institucional da UFU (" + ", ".join("@" + d for d in allowed) + ")."
        )


def validate_password_rules(value: str) -> None:
    """Regras da senha: 8+ caracteres, maiúscula, minúscula e número."""
    missing = []
    if len(value) < 8:
        missing.append("pelo menos 8 caracteres")
    if not any(c.isupper() for c in value):
        missing.append("uma letra maiúscula")
    if not any(c.islower() for c in value):
        missing.append("uma letra minúscula")
    if not any(c.isdigit() for c in value):
        missing.append("um número")
    if missing:
        raise ValidationError("A senha deve ter " + ", ".join(missing) + ".")