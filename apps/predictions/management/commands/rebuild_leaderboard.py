from django.core.management.base import BaseCommand
from apps.scoring.services import rebuild_all_leaderboards

class Command(BaseCommand):
    help = "Reconstruye todos los leaderboards."

    def handle(self, *args, **options):
        rebuild_all_leaderboards()
        self.stdout.write(self.style.SUCCESS("Leaderboards reconstruidos."))
