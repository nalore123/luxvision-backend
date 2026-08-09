from django.db import models


class SEOModelMixin(models.Model):
    """
    Abstraktni model - ne kreira svoju tablicu u bazi.
    Nasljeđuju ga Gallery i BlogPost da dobiju SEO polja
    bez dupliciranja koda.
    """
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        help_text="Ako je prazno, koristi se glavni naslov. Google obično prikazuje do 60 znakova.",
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Kratki opis za Google rezultate pretrage. Do 160 znakova.",
    )

    class Meta:
        abstract = True