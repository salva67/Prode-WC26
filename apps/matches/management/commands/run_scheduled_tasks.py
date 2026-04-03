from django.core.management.base import BaseCommand
from apps.matches.tasks import lock_due_matches, mark_live_matches


class Command(BaseCommand):
    help = "Ejecuta tareas programadas de partidos (lock + live)."

    def handle(self, *args, **options):
        lock_due_matches()
        mark_live_matches()
        self.stdout.write(self.style.SUCCESS("Tareas programadas ejecutadas."))
