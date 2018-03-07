import uuid

from django.db import models
from django.utils.translation import gettext as _

from bothub.authentication.models import User
from . import languages


class RepositoryCategory(models.Model):
    class Meta:
        verbose_name = _('repository category')
        verbose_name_plural = _('repository categories')

    name = models.CharField(
        _('name'),
        max_length=32)


class Repository(models.Model):
    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _('repositories')

    uuid = models.UUIDField(
        _('UUID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    owner = models.ForeignKey(
        User,
        models.CASCADE)
    name = models.CharField(
        _('name'),
        max_length=64)
    slug = models.CharField(
        _('slug'),
        unique=True,
        max_length=32)
    language = models.CharField(
        _('language'),
        choices=languages.LANGUAGE_CHOICES,
        max_length=2)
    categories = models.ManyToManyField(
        RepositoryCategory)
    description = models.TextField(
        _('description'),
        blank=True)
    is_private = models.BooleanField(
        _('private'),
        default=False)
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True)

    def current_update(self, language=None):
        language = language or self.language
        repository_update, created = self.updates.get_or_create(
            language=language,
            training_started_at=None)
        return repository_update

    def current_rasa_nlu_data(self, language):
        return self.current_update(language).rasa_nlu_data

    def last_trained_update(self, language):
        return self.updates.filter(
            by__isnull=False).first()

    def get_user_authorization(self, user):
        if self.is_private and self.owner.pk is not user.pk:
            return False

        get, created = RepositoryAuthorization.objects.get_or_create(
            user=user,
            repository=self)

        return get


class RepositoryUpdate(models.Model):
    class Meta:
        verbose_name = _('repository update')
        verbose_name_plural = _('repository updates')
        ordering = ['-created_at']

    repository = models.ForeignKey(
        Repository,
        models.CASCADE,
        related_name='updates')
    language = models.CharField(
        _('language'),
        choices=languages.LANGUAGE_CHOICES,
        max_length=2)
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True)
    bot_data = models.TextField(
        _('bot data'),
        blank=True,
        editable=False)
    by = models.ForeignKey(
        User,
        models.CASCADE,
        blank=True,
        null=True)
    training_started_at = models.DateTimeField(
        _('training started at'),
        blank=True,
        null=True)
    trained_at = models.DateTimeField(
        _('trained at'),
        blank=True,
        null=True)

    @property
    def examples(self):
        examples = RepositoryExample.objects.filter(
            models.Q(repository_update__language=self.language) |
            models.Q(translations__language=self.language),
            repository_update__repository=self.repository)
        if self.training_started_at:
            t_started_at = self.training_started_at
            examples = examples.exclude(
                models.Q(deleted_in=self) |
                models.Q(deleted_in__training_started_at__lt=t_started_at))
        else:
            examples = examples.exclude(deleted_in=self)
        return examples

    @property
    def rasa_nlu_data(self):
        return {
            'common_examples': list(map(
                lambda example: example.to_rsa_nlu_data(self.language),
                self.examples))
        }


class DoesNotHaveTranslation(Exception):
    pass


class RepositoryExample(models.Model):
    class Meta:
        verbose_name = _('repository example')
        verbose_name_plural = _('repository examples')

    repository_update = models.ForeignKey(
        RepositoryUpdate,
        models.CASCADE,
        related_name='added',
        editable=False)
    deleted_in = models.ForeignKey(
        RepositoryUpdate,
        models.CASCADE,
        related_name='deleted',
        blank=True,
        null=True)
    text = models.TextField(
        _('text'))
    intent = models.CharField(
        _('intent'),
        max_length=64,
        blank=True)
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True)

    def get_translation(self, language):
        try:
            return self.translations.get(language=language)
        except RepositoryTranslatedExample.DoesNotExist:
            raise DoesNotHaveTranslation()

    def get_text(self, language=None):
        if not language or language == self.repository_update.language:
            return self.text
        return self.get_translation(language).text

    def get_entities(self, language):
        if not language or language == self.repository_update.language:
            return self.entities.all()
        return self.get_translation(language).entities.all()

    def to_rsa_nlu_data(self, language):
        return {
            'text': self.get_text(language),
            'intent': self.intent,
            'entities': [
                entity.to_rsa_nlu_data for entity in self.get_entities(
                    language)],
        }

    def delete(self):
        self.deleted_in = self.repository_update.repository.current_update(
            self.repository_update.language)
        self.save(update_fields=['deleted_in'])


class RepositoryTranslatedExample(models.Model):
    class Meta:
        verbose_name = _('repository translated example')
        verbose_name_plural = _('repository translated examples')
        unique_together = ['original_example', 'language']

    original_example = models.ForeignKey(
        RepositoryExample,
        models.CASCADE,
        related_name='translations',
        editable=False)
    language = models.CharField(
        _('language'),
        choices=languages.LANGUAGE_CHOICES,
        max_length=2)
    text = models.TextField(
        _('text'))


class EntityBase(models.Model):
    class Meta:
        verbose_name = _('repository example entity')
        verbose_name_plural = _('repository example entities')
        abstract = True

    start = models.PositiveIntegerField(
        _('start'))
    end = models.PositiveIntegerField(
        _('end'))
    entity = models.CharField(
        _('entity'),
        max_length=64)
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True)

    @property
    def value(self):
        return self.get_example().text[self.start:self.end]

    @property
    def to_rsa_nlu_data(self):
        return {
            'start': self.start,
            'end': self.end,
            'value': self.value,
            'entity': self.entity,
        }

    def get_example(self):
        pass


class RepositoryExampleEntity(EntityBase):
    repository_example = models.ForeignKey(
        RepositoryExample,
        models.CASCADE,
        related_name='entities',
        editable=False)

    def get_example(self):
        return self.repository_example


class RepositoryTranslatedExampleEntity(EntityBase):
    repository_translated_example = models.ForeignKey(
        RepositoryTranslatedExample,
        models.CASCADE,
        related_name='entities',
        editable=False)

    def get_example(self):
        return self.repository_translated_example


class RepositoryAuthorization(models.Model):
    class Meta:
        verbose_name = _('repository authorization')
        verbose_name_plural = _('repository authorizations')
        unique_together = ['user', 'repository']

    uuid = models.UUIDField(
        _('UUID'),
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    user = models.ForeignKey(
        User,
        models.CASCADE)
    repository = models.ForeignKey(
        Repository,
        models.CASCADE)
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True)
