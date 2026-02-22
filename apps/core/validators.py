from django.core.exceptions import ValidationError


def validate_file_size(file_obj, max_mb: int = 2):
    limit = max_mb * 1024 * 1024
    if file_obj.size > limit:
        raise ValidationError(f'Файл слишком большой. Максимум {max_mb}MB.')
