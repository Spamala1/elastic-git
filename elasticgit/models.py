import uuid

from confmodel.config import Config
from confmodel.errors import ConfigError
from confmodel.fields import (
    ConfigText, ConfigInt, ConfigFloat, ConfigBool, ConfigList,
    ConfigDict, ConfigUrl, ConfigRegex)
from confmodel.fallbacks import SingleFieldFallback


import elasticgit


class TextField(ConfigText):
    """
    A text field
    """

    #: Mapping for Elasticsearch
    mapping = {
        'type': 'string',
    }


class IntegerField(ConfigInt):
    """
    An integer field
    """

    #: Mapping for Elasticsearch
    mapping = {
        'type': 'integer',
    }


class FloatField(ConfigFloat):
    """
    A float field
    """

    #: Mapping for Elasticsearch
    mapping = {
        'type': 'float'
    }


class BooleanField(ConfigBool):
    """
    A boolean field
    """

    #: Mapping for Elasticsearch
    mapping = {
        'type': 'boolean'
    }


class ListField(ConfigList):
    """
    A list field
    """

    #: Mapping for Elasticsearch
    mapping = {
        'type': 'string',
    }


class DictField(ConfigDict):
    """
    A dictionary field
    """

    #: Mapping for Elasticsearch
    mapping = {
        'type': 'string',
    }


class URLField(ConfigUrl):
    """
    A url field
    """

    #: Mapping for Elasticsearch
    mapping = {
        'type': 'string',
    }


class RegexField(ConfigRegex):
    """
    A regex field
    """

    #: Mapping for Elasticsearch
    mapping = {
        'type': 'string',
    }


class ModelVersionField(DictField):
    """
    A field holding the version information for a model
    """
    mapping = {
        'type': 'nested',
        'properties': {
            'language': {'type': 'string'},
            'language_version_string': {'type': 'string'},
            'language_version': {'type': 'string'},
            'package': {'type': 'string'},
            'package_version': {'type': 'string'}
        }
    }

    def __init__(self, doc, required=False, default=None, static=False,
                 fallbacks=()):
        default = default or elasticgit.version_info.copy()
        super(ModelVersionField, self).__init__(
            doc, required=required, default=default, static=static,
            fallbacks=fallbacks)


class UUIDField(TextField):

    def __init__(self, doc, required=False, default=None, static=False,
                 fallbacks=()):
        super(UUIDField, self).__init__(
            doc, required=required, default=default, static=static,
            fallbacks=fallbacks)

    def validate(self, config):
        config._config_data.setdefault(self.name, uuid.uuid4().hex)
        return super(UUIDField, self).validate(config)


class Model(Config):
    """
    Base model for all things stored in Git and Elasticsearch.
    A very thin wrapper around :py:class:`confmodel.Config`.

    Subclass this model and add more field as needed.

    :param dict config_data:
        A dictionary with keys & values to populate this Model
        instance with.
    """
    _version = ModelVersionField('Model Version Identifier')
    uuid = UUIDField('Unique Identifier')

    def __eq__(self, other):
        own_data = dict(self)
        other_data = dict(other)
        own_version_info = own_data.pop('_version')
        other_version_info = other_data.pop('_version')
        return (own_data == other_data and
                own_version_info == other_version_info)

    def __iter__(self):
        for field in self._get_fields():
            yield field.name, field.get_value(self)

ConfigError
SingleFieldFallback
