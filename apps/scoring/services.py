from django.db.models import F, Sum
from apps.groups.models import GroupMembership, PrivateGroup
from apps.matches.models import Match
from apps.predictions.models import LeaderboardEntry, Prediction

def calculate_points(prediction, result):
    predicted_outcome = (prediction.home_score > prediction.away_score) - (prediction.home_score < prediction.away_score)
    actual_outcome = (result.home_score > result.away_score) - (result.home_score < result.away_score)

    if prediction.home_score == result.home_score and prediction.away_score == result.away_score:
        return 5, True, True
    if predicted_outcome == actual_outcome:
        return 3, False, True
    return 0, False, False

def recalculate_match_predictions(match_id):
    match = Match.objects.select_related("result").get(pk=match_id)
    if not hasattr(match, "result"):
        return
    for prediction in Prediction.objects.filter(match=match):
        points, _, _ = calculate_points(prediction, match.result)
        prediction.points_awarded = points
        prediction.save(update_fields=["points_awarded"])

def rebuild_group_leaderboard(group):
    member_ids = GroupMembership.objects.filter(group=group).values_list("user_id", flat=True)
    for user_id in member_ids:
        preds = Prediction.objects.filter(user_id=user_id, match__tournament=group.tournament).select_related("match__result")
        total = preds.aggregate(total=Sum("points_awarded"))["total"] or 0
        exact_hits = preds.filter(
            match__result__isnull=False,
            home_score=F("match__result__home_score"),
            away_score=F("match__result__away_score"),
        ).count()
        correct_outcomes = 0
        for pred in preds:
            if hasattr(pred.match, "result"):
                predicted_outcome = (pred.home_score > pred.away_score) - (pred.home_score < pred.away_score)
                actual_outcome = (pred.match.result.home_score > pred.match.result.away_score) - (pred.match.result.home_score < pred.match.result.away_score)
                if predicted_outcome == actual_outcome:
                    correct_outcomes += 1
        LeaderboardEntry.objects.update_or_create(
            group=group,
            user_id=user_id,
            defaults={
                "points_total": total,
                "exact_hits": exact_hits,
                "correct_outcomes": correct_outcomes,
            },
        )

def recalculate_match_and_groups(match_id):
    match = Match.objects.select_related("tournament").get(pk=match_id)
    recalculate_match_predictions(match_id)
    for group in PrivateGroup.objects.filter(tournament=match.tournament):
        rebuild_group_leaderboard(group)

def rebuild_all_leaderboards():
    for group in PrivateGroup.objects.all():
        rebuild_group_leaderboard(group)
