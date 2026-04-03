import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime
from apps.tournaments.models import Tournament, Stage
from apps.matches.models import Team, Venue, Match

class Command(BaseCommand):
    help = "Importa fixture desde JSON."

    def add_arguments(self, parser):
        parser.add_argument("path", type=str)

    def handle(self, *args, **options):
        path = Path(options["path"])
        if not path.exists():
            raise CommandError(f"No existe el archivo: {path}")

        payload = json.loads(path.read_text(encoding="utf-8"))

        tournament_data = payload["tournament"]
        tournament, _ = Tournament.objects.update_or_create(
            slug=tournament_data["slug"],
            defaults={
                "name": tournament_data["name"],
                "status": tournament_data.get("status", "draft"),
                "starts_at": parse_datetime(tournament_data["starts_at"]),
                "ends_at": parse_datetime(tournament_data["ends_at"]),
            },
        )

        stage_map = {}
        for stage in payload.get("stages", []):
            obj, _ = Stage.objects.update_or_create(
                tournament=tournament,
                code=stage["code"],
                defaults={"name": stage["name"], "order": stage["order"]},
            )
            stage_map[stage["code"]] = obj

        team_map = {}
        for team in payload.get("teams", []):
            obj, _ = Team.objects.update_or_create(
                fifa_code=team["fifa_code"],
                defaults={
                    "name": team["name"],
                    "short_name": team.get("short_name", team["name"]),
                    "group_code": team.get("group_code", ""),
                    "flag_emoji": team.get("flag_emoji", ""),
                    "flag_image": team.get("flag_image", ""),
                },
            )
            team_map[obj.fifa_code] = obj

        venue_map = {}
        for venue in payload.get("venues", []):
            obj, _ = Venue.objects.update_or_create(
                name=venue["name"],
                city=venue["city"],
                defaults={
                    "country": venue["country"],
                    "timezone": venue.get("timezone", "UTC"),
                    "address": venue.get("address", ""),
                    "capacity": venue.get("capacity", 0),
                },
            )
            venue_map[(obj.name, obj.city)] = obj

        for match in payload.get("matches", []):
            Match.objects.update_or_create(
                tournament=tournament,
                number=match["number"],
                defaults={
                    "stage": stage_map[match["stage_code"]],
                    "group_code": match.get("group_code", ""),
                    "home_team": team_map[match["home_code"]],
                    "away_team": team_map[match["away_code"]],
                    "venue": venue_map[(match["venue_name"], match["venue_city"])],
                    "kickoff_at": parse_datetime(match["kickoff_at"]),
                    "lock_at": parse_datetime(match["lock_at"]),
                    "status": match.get("status", "scheduled"),
                },
            )

        self.stdout.write(self.style.SUCCESS("Fixture importado correctamente."))
