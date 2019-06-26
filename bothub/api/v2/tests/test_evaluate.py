import json

from django.test import RequestFactory
from django.test import TestCase
from rest_framework import status

from bothub.api.v2.evaluate.views import EvaluateViewSet
from bothub.common import languages
from bothub.common.models import RepositoryExample, RepositoryUpdate, Repository, RepositoryEvaluate
from .utils import create_user_and_token


# TestCases

class NewEvaluateTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.owner, self.owner_token = create_user_and_token('owner')
        self.user, self.token = create_user_and_token()
        self.authorization_header = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(self.token.key),
        }

        self.repository = Repository.objects.create(
            owner=self.owner,
            name='Testing',
            slug='test',
            language=languages.LANGUAGE_EN
        )

        self.repository_update = RepositoryUpdate.objects.create(
            repository=self.repository,
            language=languages.LANGUAGE_EN,
            algorithm='statistical_model',
        )

        self.example_1 = RepositoryExample.objects.create(
            repository_update=self.repository_update,
            text="test",
            intent="greet",
        )

    def request(self, data):
        request = self.factory.post(
            '/api/v2/evaluate/',
            json.dumps(data),
            content_type='application/json',
            **self.authorization_header)
        response = EvaluateViewSet.as_view({'post': 'create'})(request)
        response.render()
        content_data = json.loads(response.content)
        return (response, content_data,)

    def test_okay(self):
        response, content_data = self.request(
            {
                'repository': str(self.repository.uuid),
                'text': 'haha',
                'language': languages.LANGUAGE_EN,
                'intent': 'greet',
                'entities': []
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED)

    def test_intent(self):
        response, content_data = self.request(
            {
                'repository': str(self.repository.uuid),
                'text': 'haha',
                'language': languages.LANGUAGE_EN,
                'intent': '',
                'entities': []
            }
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST)
        self.assertIn('intent', content_data)

    def test_entities_not_exists(self):
        response, content_data = self.request(
            {
                'repository': str(self.repository.uuid),
                'text': 'haha',
                'language': languages.LANGUAGE_EN,
                'intent': 'greet',
                'entities': [{"entity": "hello", "start": 0, "end": 3}]
            }
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST)

        self.assertIn('entities', content_data)


class EvaluateDestroyTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.owner, self.owner_token = create_user_and_token('owner')
        self.user, self.token = create_user_and_token()

        self.repository = Repository.objects.create(
            owner=self.owner,
            name='Testing',
            slug='test',
            language=languages.LANGUAGE_EN
        )

        self.repository_update = RepositoryUpdate.objects.create(
            repository=self.repository,
            language='en',
            algorithm='statistical_model',
        )

        self.example_1 = RepositoryExample.objects.create(
            repository_update=self.repository_update,
            text="test",
            intent="greet",
        )

        self.repository_evaluate = RepositoryEvaluate.objects.create(
            repository_update=self.repository_update,
            text="test",
            intent="greet"
        )

    def request(self, token):
        authorization_header = {
            'HTTP_AUTHORIZATION': 'Token {}'.format(token.key),
        }

        request = self.factory.delete(
            '/api/v2/evaluate/{}/'.format(self.repository_evaluate.id),
            **authorization_header)
        response = EvaluateViewSet.as_view(
            {'delete': 'destroy'})(request, pk=self.repository_evaluate.id)
        return response

    def test_okay(self):
        response = self.request(self.owner_token)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT)

    def test_private_okay(self):
        response = self.request(self.token)
        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN)

    def test_already_deleted(self):
        self.repository_evaluate.delete()
        response = self.request(self.owner_token)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT)
        self.assertIsNotNone(
            self.repository_evaluate.deleted_in
        )
