import json

from django.utils.translation import gettext as _
from rest_framework import serializers

from bothub.common.models import Repository
from bothub.common.models import RepositoryEvaluate
from bothub.common.models import RepositoryEvaluateEntity
from bothub.common.models import RepositoryEvaluateResult
from bothub.common.models import RepositoryEvaluateResultScore
from bothub.common.models import RepositoryEvaluateResultIntent
from bothub.common.models import RepositoryEvaluateResultEntity

from bothub.common.languages import LANGUAGE_CHOICES

from ..fields import EntityValueField
from .validators import ThereIsEntityValidator
from .validators import ThereIsIntentValidator


class RepositoryEvaluateEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = RepositoryEvaluateEntity
        fields = [
            'entity',
            'start',
            'end',
        ]

    entity = EntityValueField()


class RepositoryEvaluateSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepositoryEvaluate
        fields = [
            'id',
            'repository',
            'text',
            'language',
            'intent',
            'entities',
            'created_at',
        ]
        read_only_fields = [
            'deleted_in',
            'created_at',
        ]

    entities = RepositoryEvaluateEntitySerializer(
        many=True,
        required=False,
    )

    repository = serializers.PrimaryKeyRelatedField(
        queryset=Repository.objects,
        write_only=True,
        required=True,
    )

    language = serializers.ChoiceField(
        LANGUAGE_CHOICES,
        label=_('Language')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(ThereIsEntityValidator())
        self.validators.append(ThereIsIntentValidator())

    def create(self, validated_data):
        entities = validated_data.pop('entities')
        repository = validated_data.pop('repository')
        language = validated_data.pop('language')

        repository_update = repository.current_update(language)
        validated_data.update({'repository_update': repository_update})
        evaluate = RepositoryEvaluate.objects.create(**validated_data)

        for entity in entities:
            RepositoryEvaluateEntity.objects.create(
                repository_evaluate=evaluate, **entity)

        return evaluate

    def update(self, instance, validated_data):
        repository = validated_data.pop('repository')
        language = validated_data.get('language', instance.language)

        instance.text = validated_data.get('text', instance.text)
        instance.intent = validated_data.get('intent', instance.intent)
        instance.repository_update = repository.current_update(language)
        instance.save()
        instance.delete_entities()

        for entity in validated_data.pop('entities'):
            RepositoryEvaluateEntity.objects.create(
                repository_evaluate=instance, **entity)

        return instance


class RepositoryEvaluateResultVersionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepositoryEvaluateResult
        fields = [
            'id',
            'language',
            'created_at',
            'version',
        ]

    language = serializers.SerializerMethodField()

    def get_language(self, obj):
        return obj.repository_update.language


class RepositoryEvaluateResultScore(serializers.ModelSerializer):

    class Meta:
        model = RepositoryEvaluateResultScore
        fields = [
            'precision',
            'f1_score',
            'accuracy',
            'recall',
            'support'
        ]

    precision = serializers.SerializerMethodField()
    f1_score = serializers.SerializerMethodField()
    accuracy = serializers.SerializerMethodField()
    recall = serializers.SerializerMethodField()
    support = serializers.SerializerMethodField()

    def get_precision(self, obj):
        return obj.precision if obj.precision else 0

    def get_f1_score(self, obj):
        return obj.f1_score if obj.f1_score else 0

    def get_accuracy(self, obj):
        return obj.accuracy if obj.accuracy else 0

    def get_recall(self, obj):
        return obj.recall if obj.recall else 0

    def get_support(self, obj):
        return obj.support if obj.support else 0


class RepositoryEvaluateResultIntentSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepositoryEvaluateResultIntent
        fields = [
            'intent',
            'score',
        ]

    score = RepositoryEvaluateResultScore(read_only=True)


class RepositoryEvaluateResultEntitySerializer(serializers.ModelSerializer):

    class Meta:
        model = RepositoryEvaluateResultEntity
        fields = [
            'entity',
            'score',
        ]

    score = RepositoryEvaluateResultScore(read_only=True)
    entity = serializers.SerializerMethodField()

    def get_entity(self, obj):
        return obj.entity.value


class RepositoryEvaluateResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = RepositoryEvaluateResult
        fields = [
            'id',
            'version',
            'created_at',
            'matrix_chart',
            'confidence_chart',
            'log',
            'intents_list',
            'entities_list',
            'intent_results',
            'entity_results',
        ]

    log = serializers.SerializerMethodField()
    intents_list = serializers.SerializerMethodField()
    entities_list = serializers.SerializerMethodField()
    intent_results = RepositoryEvaluateResultScore(read_only=True)
    entity_results = RepositoryEvaluateResultScore(read_only=True)

    def get_intents_list(self, obj):
        return RepositoryEvaluateResultIntentSerializer(
            obj.evaluate_result_intent.all().exclude(intent__exact=''),
            many=True).data

    def get_entities_list(self, obj):
        return RepositoryEvaluateResultEntitySerializer(
            obj.evaluate_result_entity.all(), many=True).data

    def get_log(self, obj):
        intent = self.context.get('request').\
            query_params.get('intent', None)
        min_confidence = self.context.get('request').\
            query_params.get('min', None)
        max_confidence = self.context.get('request').\
            query_params.get('max', None)

        if intent or min_confidence or max_confidence:
            start_filter = True
        else:
            start_filter = False

        def check(result, value, min_per, max_per, filter_start):
            min_confidence = float(
                min_per if min_per is not None else 0
            ) / 100
            max_confidence = float(
                max_per if max_per is not None else 100
            ) / 100

            if filter_start:
                status = False
                if result['intent'] == value:
                    status = True

                if min_per and max_per:
                    confidence = result['intent_prediction']['confidence']
                    if min_confidence <= confidence <= max_confidence:
                        status = True
                    else:
                        status = False

                if status:
                    return result
            else:
                return result

        results = filter(
            None,
            list(
                map(
                    lambda result:
                    check(
                        result,
                        intent,
                        min_confidence,
                        max_confidence,
                        start_filter
                    ),
                    json.loads(obj.log)
                )
            )
        )

        return results
