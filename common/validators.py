from django.core.exceptions import ValidationError

MAX_UPLOAD_SIZE_MB = 15


def validate_image_size(file):
    limit_bytes = MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if file.size > limit_bytes:
        raise ValidationError(
            f"Slika je prevelika. Maksimalna veličina je {MAX_UPLOAD_SIZE_MB}MB."
        )