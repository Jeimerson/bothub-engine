import random
import json

from django.core.management.base import BaseCommand
from django.conf import settings

from bothub.authentication.models import User
from bothub.common.models import RepositoryCategory
from bothub.common.models import RepositoryIntent
from bothub.common.models import Repository
from bothub.common.models import RepositoryExample
from bothub.common.models import RepositoryExampleEntity
from bothub.common.models import RepositoryTranslatedExample
from bothub.common.models import RepositoryTranslatedExampleEntity
from bothub.common.models import RepositoryEvaluate
from bothub.common.models import RepositoryEvaluateEntity
from bothub.common.models import RepositoryEvaluateResult
from bothub.common.models import RepositoryEvaluateResultScore
from bothub.common.models import RepositoryEvaluateResultIntent
from bothub.common.models import RepositoryEvaluateResultEntity

from bothub.common import languages


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        assert settings.DEBUG, "Don't run this command in production"

        # Users

        if not User.objects.filter(email="admin@bothub.it").exists:
            User.objects.create_superuser(
                email="admin@bothub.it", nickname="admin", password="admin", name="Admin"
            )

        if not User.objects.filter(email="user@bothub.it").exists:
            user = User.objects.create_user(
                email="user@bothub.it", nickname="user", password="user", name="User"
            )

        # Categories

        categories = list(
            map(
                lambda x: RepositoryCategory.objects.create(
                    name="Category {}".format(x)
                ),
                range(1, 6),
            )
        )

        # Repositories

        repository_1 = Repository.objects.create(
            owner=user,
            name="Repository 1",
            slug="repo1",
            language=languages.LANGUAGE_EN,
        )
        repository_1.categories.add(categories[0])
        repository_1.categories.add(categories[1])
        repository_1.categories.add(categories[3])

        repository_1.current_version()

        repository_2 = Repository.objects.create(
            owner=user,
            name="Repository 2",
            slug="repo2",
            language=languages.LANGUAGE_EN,
        )
        repository_2.categories.add(categories[0])
        repository_2.categories.add(categories[2])

        repository_2.current_version()

        for x in range(3, 46):
            new_repository = Repository.objects.create(
                owner=user,
                name="Repository {}".format(x),
                slug="repo{}".format(x),
                language=languages.LANGUAGE_EN,
            )
            new_repository.categories.add(random.choice(categories))
            new_repository.current_version()

        # Examples

        intent_greet = RepositoryIntent.objects.create(
            repository_version=repository_1.current_version().repository_version,
            text="greet",
        )

        intent_affirm = RepositoryIntent.objects.create(
            repository_version=repository_1.current_version().repository_version,
            text="affirm",
        )

        intent_restaurant_search = RepositoryIntent.objects.create(
            repository_version=repository_1.current_version().repository_version,
            text="restaurant_search",
        )

        example_1 = RepositoryExample.objects.create(
            repository_version_language=repository_1.current_version(),
            text="hi",
            intent=intent_greet,
        )

        example_2 = RepositoryExample.objects.create(
            repository_version_language=repository_1.current_version(),
            text="hello",
            intent=intent_greet,
        )

        example_3 = RepositoryExample.objects.create(
            repository_version_language=repository_1.current_version(),
            text="yes",
            intent=intent_affirm,
        )

        RepositoryExample.objects.create(
            repository_version_language=repository_1.current_version(),
            text="yep",
            intent=intent_affirm,
        )

        example_5 = RepositoryExample.objects.create(
            repository_version_language=repository_1.current_version(),
            text="show me chinese restaurants",
            intent=intent_restaurant_search,
        )

        # Example Entity

        RepositoryExampleEntity.objects.create(
            repository_example=example_1, start=8, end=15, entity="cuisine"
        )

        RepositoryExampleEntity.objects.create(
            repository_example=example_5, start=8, end=15, entity="cuisine"
        )

        # Translated Example

        RepositoryTranslatedExample.objects.create(
            original_example=example_1, language=languages.LANGUAGE_PT, text="oi"
        )

        RepositoryTranslatedExample.objects.create(
            original_example=example_2, language=languages.LANGUAGE_PT, text="olá"
        )

        RepositoryTranslatedExample.objects.create(
            original_example=example_3, language=languages.LANGUAGE_PT, text="sim"
        )

        tranlated_4 = RepositoryTranslatedExample.objects.create(
            original_example=example_5,
            language=languages.LANGUAGE_PT,
            text="mostre me restaurantes chinês",
        )

        # Translated Example Entity

        RepositoryTranslatedExampleEntity.objects.create(
            repository_translated_example=tranlated_4,
            start=23,
            end=29,
            entity="cuisine",
        )

        # Evaluates

        evalute_1 = RepositoryEvaluate.objects.create(
            repository_version_language=repository_1.current_version(),
            text="show me chinese restaurants",
            intent="restaurant_search",
        )

        evalute_2 = RepositoryEvaluate.objects.create(
            repository_version_language=repository_1.current_version(),
            text="hello",
            intent="greet",
        )

        RepositoryEvaluate.objects.create(
            repository_version_language=repository_1.current_version(),
            text="yes",
            intent="affirm",
        )

        RepositoryEvaluate.objects.create(
            repository_version_language=repository_1.current_version(),
            text="yep",
            intent="affirm",
        )

        RepositoryEvaluateEntity.objects.create(
            repository_evaluate=evalute_1, start=23, end=29, entity="cuisine"
        )

        RepositoryEvaluateEntity.objects.create(
            repository_evaluate=evalute_2, start=0, end=5, entity="greet"
        )

        # Evaluate Report

        for x in range(0, 2):
            intent_results = RepositoryEvaluateResultScore.objects.create(
                f1_score=0.976, precision=0.978, accuracy=0.976
            )

            entity_results = RepositoryEvaluateResultScore.objects.create(
                f1_score=0.977, precision=0.978, accuracy=0.978
            )

            evaluate_log = [
                {
                    "text": "hey",
                    "intent": "greet",
                    "intent_prediction": {
                        "name": "greet",
                        "confidence": 0.9263743763408538,
                    },
                    "status": "success",
                },
                {
                    "text": "howdy",
                    "intent": "greet",
                    "intent_prediction": {
                        "name": "greet",
                        "confidence": 0.8099720606047796,
                    },
                    "status": "success",
                },
                {
                    "text": "hey there",
                    "intent": "greet",
                    "intent_prediction": {
                        "name": "greet",
                        "confidence": 0.8227075176309955,
                    },
                    "status": "success",
                },
                {
                    "text": "test with nlu",
                    "intent": "restaurant_search",
                    "intent_prediction": {
                        "name": "goodbye",
                        "confidence": 0.3875259420712092,
                    },
                    "status": "error",
                },
            ]

            sample_url = "https://s3.amazonaws.com/bothub-sample"
            evaluate_result = RepositoryEvaluateResult.objects.create(
                repository_version_language=repository_1.current_version(),
                intent_results=intent_results,
                entity_results=entity_results,
                matrix_chart="{}/confmat.png".format(sample_url),
                confidence_chart="{}/hist.png".format(sample_url),
                log=json.dumps(evaluate_log),
            )

            intent_score_1 = RepositoryEvaluateResultScore.objects.create(
                precision=1.0, recall=1.0, f1_score=1.0, support=11
            )

            intent_score_2 = RepositoryEvaluateResultScore.objects.create(
                precision=0.89, recall=1.0, f1_score=0.94, support=8
            )

            intent_score_3 = RepositoryEvaluateResultScore.objects.create(
                precision=1.0, recall=1.0, f1_score=1.0, support=8
            )

            intent_score_4 = RepositoryEvaluateResultScore.objects.create(
                precision=1.0, recall=0.93, f1_score=0.97, support=15
            )

            RepositoryEvaluateResultIntent.objects.create(
                evaluate_result=evaluate_result, intent="affirm", score=intent_score_1
            )

            RepositoryEvaluateResultIntent.objects.create(
                evaluate_result=evaluate_result, intent="goodbye", score=intent_score_2
            )

            RepositoryEvaluateResultIntent.objects.create(
                evaluate_result=evaluate_result, intent="greet", score=intent_score_3
            )

            RepositoryEvaluateResultIntent.objects.create(
                evaluate_result=evaluate_result,
                intent="restaurant_search",
                score=intent_score_4,
            )

            entity_score_1 = RepositoryEvaluateResultScore.objects.create(
                precision=1.0, recall=0.90, f1_score=0.95, support=10
            )

            entity_score_2 = RepositoryEvaluateResultScore.objects.create(
                precision=1.0, recall=0.75, f1_score=0.86, support=8
            )

            RepositoryEvaluateResultEntity.objects.create(
                evaluate_result=evaluate_result, entity="cuisine", score=entity_score_1
            )

            RepositoryEvaluateResultEntity.objects.create(
                evaluate_result=evaluate_result, entity="greet", score=entity_score_2
            )
