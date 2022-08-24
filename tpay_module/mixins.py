"""TPay module mixins file."""
# Django
from django.core.exceptions import ValidationError


class SingleInstanceMixin(object):
    """Single instance mixin - limit model creation to single instance."""

    def clean(self):  # noqa: D102
        model = self.__class__
        if model.objects.exists() and self.id != model.objects.get().id:
            raise ValidationError(
                f'Można utworzyć tylko jedne ustawienia {model.__name__}',
            )
        super().clean()
