# common/utils.py
from django.utils.text import slugify


def generate_unique_slug(instance, base_value, slug_field_name="slug"):
    """
    Generira jedinstveni slug za dani model.

    - instance: instanca modela koja se sprema (self iz save())
    - base_value: tekst iz kojeg se generira slug (npr. title_hr)
    - slug_field_name: ime slug polja na modelu (default "slug")

    Ako je bazni slug zauzet, dodaje -2, -3, itd. dok ne nađe slobodan.
    Kod editiranja postojećeg zapisa, isključuje samog sebe iz provjere
    (inače bi svaki put mislio da je slug "zauzet" sam sa sobom).
    """
    base_slug = slugify(base_value)
    slug = base_slug
    ModelClass = instance.__class__
    counter = 2

    while True:
        queryset = ModelClass.objects.filter(**{slug_field_name: slug})
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)

        if not queryset.exists():
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1