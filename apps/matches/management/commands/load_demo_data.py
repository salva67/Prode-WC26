from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.tournaments.models import Tournament, Stage
from apps.matches.models import Team, Venue, Match

class Command(BaseCommand):
    help = "Carga demo data para desarrollo."

    def handle(self, *args, **options):
        tournament, _ = Tournament.objects.get_or_create(
            slug="world-cup-2026",
            defaults={
                "name": "Mundial 2026",
                "status": "active",
                "starts_at": timezone.now(),
                "ends_at": timezone.now() + timedelta(days=35),
            },
        )

        group_stage, _ = Stage.objects.get_or_create(
            tournament=tournament,
            code="GROUP",
            defaults={"name": "Fase de grupos", "order": 1},
        )

        teams = [
            ("Argentina", "Argentina", "ARG", "G", "🇦🇷"),
            ("Brasil", "Brasil", "BRA", "G", "🇧🇷"),
            ("México", "México", "MEX", "A", "🇲🇽"),
            ("España", "España", "ESP", "B", "🇪🇸"),
        ]
        team_objs = {}
        for name, short, code, group_code, flag in teams:
            team_objs[code], _ = Team.objects.get_or_create(
                fifa_code=code,
                defaults={
                    "name": name,
                    "short_name": short,
                    "group_code": group_code,
                    "flag_emoji": flag,
                },
            )

        venue, _ = Venue.objects.get_or_create(
            name="MetLife Stadium",
            city="New York/New Jersey",
            country="USA",
            defaults={"timezone": "America/New_York", "capacity": 82500},
        )

        base_time = timezone.now() + timedelta(days=1)
        fixtures = [
            (1, "ARG", "BRA", 0),
            (2, "MEX", "ESP", 1),
            (3, "ARG", "MEX", 2),
            (4, "BRA", "ESP", 3),
        ]
        for number, home, away, offset in fixtures:
            Match.objects.get_or_create(
                tournament=tournament,
                number=number,
                defaults={
                    "stage": group_stage,
                    "group_code": "A",
                    "home_team": team_objs[home],
                    "away_team": team_objs[away],
                    "venue": venue,
                    "kickoff_at": base_time + timedelta(days=offset),
                    "lock_at": base_time + timedelta(days=offset, minutes=-15),
                    "status": "scheduled",
                },
            )

        self.stdout.write(self.style.SUCCESS("Demo data cargada."))
