import random

import pyquoks.utils
import yaml

from .. import models


class GuidanceProvider:
    test: models.CareerGuidanceTest

    def __init__(self) -> None:
        with open(pyquoks.utils.get_path("assets/career_guidance_test.yaml"), "rb") as file:
            self.test = models.CareerGuidanceTest.model_validate(yaml.load(file, yaml.FullLoader))

    def get_recommended_course(self, professions_rating: dict[int, int]) -> models.CareerGuidanceProfession:
        max_rating = max(professions_rating.values())

        recommended_profession_id = random.choice([
            professions_id for professions_id, rating in professions_rating.items() if rating == max_rating
        ])

        return [profession for profession in self.test.professions if profession.id == recommended_profession_id][0]
