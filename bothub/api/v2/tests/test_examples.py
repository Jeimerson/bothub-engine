import json
from django.conf import settings

from django.test import TestCase
from django.test import RequestFactory
from rest_framework import status

from bothub.common.models import Repository, RepositoryIntent
from bothub.common.models import RepositoryExample
from bothub.common.models import RepositoryTranslatedExample
from bothub.common.models import RepositoryExampleEntity
from bothub.common import languages

from bothub.api.v2.tests.utils import create_user_and_token
from bothub.api.v2.examples.views import ExamplesViewSet
from bothub.api.v2.repository.views import RepositoryExampleViewSet


class DefaultExamplesAPITestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.owner, self.owner_token = create_user_and_token("owner")
        self.user, self.user_token = create_user_and_token("user")

        self.repository = Repository.objects.create(
            owner=self.owner,
            name="Repository 1",
            slug="repo",
            language=languages.LANGUAGE_EN,
        )
        self.example_intent_1 = RepositoryIntent.objects.create(
            text="greet",
            repository_version=self.repository.current_version().repository_version,
        )
        self.example_intent_2 = RepositoryIntent.objects.create(
            text="farewell",
            repository_version=self.repository.current_version().repository_version,
        )
        self.example_1 = RepositoryExample.objects.create(
            repository_version_language=self.repository.current_version(),
            text="hi",
            intent=self.example_intent_1,
        )
        entity_1 = RepositoryExampleEntity.objects.create(
            repository_example=self.example_1, start=0, end=0, entity="hi"
        )
        entity_1.entity.set_group("greet")
        entity_1.entity.save()
        self.example_2 = RepositoryExample.objects.create(
            repository_version_language=self.repository.current_version(),
            text="hello",
            intent=self.example_intent_1,
        )
        self.example_3 = RepositoryExample.objects.create(
            repository_version_language=self.repository.current_version(),
            text="bye",
            intent=self.example_intent_2,
        )
        self.example_4 = RepositoryExample.objects.create(
            repository_version_language=self.repository.current_version(),
            text="bye bye",
            intent=self.example_intent_2,
        )

        self.repository_2 = Repository.objects.create(
            owner=self.owner,
            name="Repository 2",
            slug="repo2",
            language=languages.LANGUAGE_EN,
        )
        self.example2_intent_1 = RepositoryIntent.objects.create(
            text="greet",
            repository_version=self.repository_2.current_version().repository_version,
        )
        self.example_5 = RepositoryExample.objects.create(
            repository_version_language=self.repository_2.current_version(),
            text="hi",
            intent=self.example2_intent_1,
        )
        self.example_6 = RepositoryExample.objects.create(
            repository_version_language=self.repository_2.current_version(
                languages.LANGUAGE_PT
            ),
            text="oi ",
            intent=self.example2_intent_1,
        )
        self.translation_6 = RepositoryTranslatedExample.objects.create(
            original_example=self.example_6, language=languages.LANGUAGE_EN, text="hi"
        )


class ListExamplesAPITestCase(DefaultExamplesAPITestCase):
    def request(self, data={}, token=None):
        authorization_header = (
            {"HTTP_AUTHORIZATION": "Token {}".format(token.key)} if token else {}
        )

        request = self.factory.get("/v2/examples/", data, **authorization_header)

        response = ExamplesViewSet.as_view({"get": "list"})(request)
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_okay(self):
        response, content_data = self.request(
            {"repository_uuid": self.repository.uuid}, self.owner_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 4)

        response, content_data = self.request(
            {"repository_uuid": self.repository_2.uuid}, self.owner_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 2)

    def test_deleted(self):
        self.example_1.delete()
        response, content_data = self.request(
            {"repository_uuid": self.repository.uuid}, self.owner_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 3)

    def test_withuout_repository_uuid(self):
        response, content_data = self.request()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_text(self):
        response, content_data = self.request(
            {"repository_uuid": self.repository.uuid, "text": self.example_1.text},
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 1)
        self.assertEqual(content_data.get("results")[0].get("id"), self.example_1.id)

    def test_filter_part_text(self):
        response, content_data = self.request(
            {"repository_uuid": self.repository.uuid, "search": "h"}, self.owner_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 2)

    def test_filter_language(self):
        response, content_data = self.request(
            {
                "repository_uuid": self.repository_2.uuid,
                "language": languages.LANGUAGE_PT,
            },
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 1)

    def test_filter_has_translation(self):
        response, content_data = self.request(
            {"repository_uuid": self.repository_2.uuid, "has_translation": False},
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 1)

        response, content_data = self.request(
            {"repository_uuid": self.repository_2.uuid, "has_translation": True},
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 1)

    def test_filter_has_not_translation_to(self):
        response, content_data = self.request(
            {
                "repository_uuid": self.repository_2.uuid,
                "has_not_translation_to": languages.LANGUAGE_ES,
            },
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 2)

        response, content_data = self.request(
            {
                "repository_uuid": self.repository_2.uuid,
                "has_not_translation_to": languages.LANGUAGE_EN,
            },
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 1)

    def test_filter_order_by_translation(self):
        response, content_data = self.request(
            {
                "repository_uuid": self.repository_2.uuid,
                "order_by_translation": languages.LANGUAGE_EN,
            },
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = content_data.get("results")
        self.assertEqual(0, len(results[0].get("translations")))
        self.assertEqual(1, len(results[1].get("translations")))

    def test_filter_order_by_translation_inverted(self):
        response, content_data = self.request(
            {
                "repository_uuid": self.repository_2.uuid,
                "order_by_translation": "-{}".format(languages.LANGUAGE_EN),
            },
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = content_data.get("results")
        self.assertEqual(1, len(results[0].get("translations")))
        self.assertEqual(0, len(results[1].get("translations")))

    def test_filter_intent(self):
        response, content_data = self.request(
            {"repository_uuid": self.repository.uuid, "intent": "farewell"},
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 2)

    def test_filter_intent_id(self):
        response, content_data = self.request(
            {
                "repository_uuid": self.repository.uuid,
                "intent_id": self.example_intent_2.pk,
            },
            self.owner_token,
        )
        for result in content_data.get("results"):
            self.assertEqual(result.get("intent"), self.example_intent_2.text)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 2)

    def test_filter_label(self):
        response, content_data = self.request(
            {"repository_uuid": self.repository.uuid, "group": "greet"},
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 1)

    def test_filter_entity(self):
        response, content_data = self.request(
            {"repository_uuid": self.repository.uuid, "entity": "hi"}, self.owner_token
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(content_data.get("count"), 1)


class CreateExamplesAPITestCase(DefaultExamplesAPITestCase):
    def request(self, data, token):
        authorization_header = {"HTTP_AUTHORIZATION": "Token {}".format(token.key)}
        request = self.factory.post(
            "/v2/repository/example/",
            json.dumps(data),
            content_type="application/json",
            **authorization_header,
        )

        response = RepositoryExampleViewSet.as_view({"post": "create"})(request)
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data)

    def test_ok(self):
        data = {
            "repository": str(self.repository.uuid),
            "repository_version": self.repository.current_version().repository_version.pk,
            "text": "testing 123 yés ///????³³²²¹¹£  ++++-----",
            "language": "en",
            "entities": [
                {
                    "start": 9,
                    "end": 11,
                    "entity": "numero",
                }
            ],
            "intent": str(self.example_intent_1.pk),
            "is_corrected": False,
        }

        response, content_data = self.request(
            data,
            self.owner_token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_text_without_letters(self):
        data = {
            "repository": str(self.repository.uuid),
            "repository_version": self.repository.current_version().repository_version.pk,
            "text": " ---- //// -----",
            "language": "en",
            "entities": [
                {
                    "start": 9,
                    "end": 11,
                    "entity": "numero",
                }
            ],
            "intent": str(self.example_intent_1.pk),
            "is_corrected": False,
        }
        response, content_data = self.request(
            data,
            self.owner_token,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_text_words_limit(self):
        limit = settings.REPOSITORY_EXAMPLE_TEXT_WORDS_LIMIT + 1
        text = " ".join(["teste" for _ in range(limit)])
        data = {
            "repository": str(self.repository.uuid),
            "repository_version": self.repository.current_version().repository_version.pk,
            "text": text,
            "language": "en",
            "entities": [
                {
                    "start": 9,
                    "end": 11,
                    "entity": "numero",
                }
            ],
            "intent": str(self.example_intent_1.pk),
            "is_corrected": False,
        }
        response, content_data = self.request(
            data,
            self.owner_token,
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
