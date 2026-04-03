from django.db import models

class Tournament(models.Model):
    STATUS_CHOICES = (
        ("draft", "Borrador"),
        ("active", "Activo"),
        ("finished", "Finalizado"),
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()

    class Meta:
        ordering = ("-starts_at",)

    def __str__(self):
        return self.name

class Stage(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name="stages")
    code = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    order = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ("tournament", "code")
        ordering = ("order",)

    def __str__(self):
        return f"{self.tournament} - {self.name}"
