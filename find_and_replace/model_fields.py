# coding: utf-8

"""
    django find&replace
    ~~~~~~~~~~~~~~~

    :copyleft: 2015 by find&replace team, see AUTHORS for more details.
    :created: 2015 by JensDiemer.de
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""

from __future__ import absolute_import, print_function

from django.db import models

from django.db.models.loading import get_apps, get_models

from find_and_replace.settings import FIND_AND_REPLACE_APP_LABELS, \
    FIND_AND_REPLACE_FIELDS


def field2dot_name(field):
    return "%s.%s.%s" % (
        field.model._meta.app_label, field.model._meta.object_name, field.get_attname()
    )


def sort_fields(fields):
    return [
        field
        for field in sorted(fields, key=lambda field: field2dot_name(field).lower())
    ]


def filter_model_fields(app_labels=None, model_fields=None):
    """
    Collect a filtered and sorted list of model fields.

    >>> from django.db import models
    >>> fields = filter_model_fields(
    ...     app_labels = ("auth",), model_fields = (models.CharField,)
    ... )
    >>> field2dot_name(fields[0])
    'auth.Group.name'
    >>> [field.get_attname() for field in fields]
    ['name', 'codename', 'name', 'email', 'first_name', 'last_name', 'password', 'username']

    :param app_labels: Filter by app labels, if None: all installed apps
    :param model_fields: List of field classes for filtering
    :return: field list, sorted by dot name representation
    """
    filtered_fields = set()
    for app in get_apps():
        for model in get_models(app):
            for field in model._meta.fields:
                if app_labels is not None:
                    if field.model._meta.app_label not in app_labels:
                        continue

                if not isinstance(field, model_fields):
                    continue

                filtered_fields.add(field)

    return sort_fields(filtered_fields)


def field_list2choices(fields):
    return [
        (index, field2dot_name(field)) for index, field in enumerate(fields)
    ]

def get_filtered_field_choices(app_labels=None, model_fields=None):
    return field_list2choices(
        filter_model_fields(
            app_labels=app_labels,
            model_fields=model_fields
        )
    )

def get_model_fields():
    return tuple([getattr(models, field_name) for field_name in FIND_AND_REPLACE_FIELDS])


def field_choices():
    return get_filtered_field_choices(
        app_labels=FIND_AND_REPLACE_APP_LABELS,
        model_fields=get_model_fields(),
    )

def get_fields_from_choice(field_choice):
    all_fields = filter_model_fields(
        app_labels=FIND_AND_REPLACE_APP_LABELS,
        model_fields=get_model_fields(),
    )
    fields = []
    for index in field_choice:
        fields.append(all_fields[int(index)])

    return fields
