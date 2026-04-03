from django.test import TestCase
from apps.scoring.services import calculate_points

class ScoringTests(TestCase):
    def test_exact_result_scores_five(self):
        class Obj: pass
        pred = Obj(); pred.home_score = 2; pred.away_score = 1
        result = Obj(); result.home_score = 2; result.away_score = 1
        pts, exact, outcome = calculate_points(pred, result)
        self.assertEqual(pts, 5)
        self.assertTrue(exact)
        self.assertTrue(outcome)
