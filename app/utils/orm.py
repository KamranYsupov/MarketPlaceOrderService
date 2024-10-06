from typing import Type, TypeVar, List

import strawberry
from sqlalchemy import select
from sqlalchemy.orm import joinedload, load_only

from .chars import normalize_field_name

ModelType = TypeVar("ModelType")


def flatten(items):
    if not items:
        return items
    if isinstance(items[0], list):
        return flatten(items[0]) + flatten(items[1:])
    return items[:1] + flatten(items[1:])


def get_relation_options(relation: dict, previous_sql=None):
    key, val = next(iter(relation.items()))
    fields = val['fields']
    relations = val['relations']
    if previous_sql:
        sql = previous_sql.joinedload(key).load_only(*fields)
    else:
        sql = joinedload(key).load_only(*fields)
    if len(relations) == 0:
        return sql
    if len(relations) == 1:
        return get_relation_options(relations[0], sql)
    result = []
    for i in relations:
        rels = get_relation_options(i, sql)
        if hasattr(rels, '__iter__'):
            for r in rels:
                result.append(r)
        else:
            result.append(rels)
    return result


def get_orm_statement_by_selected_fields(
    model: ModelType,
    info: strawberry.Info, 
):
    """
    input:
    {
      users: {
        id
        username
        email
        groups {
          id
          name
          category {
            id
            name
          }
        }
      }
    }
    output:
        (select(User).options(
           load_only(User.id, User.username, User.email),
           joinedload(User.groups).load_only(Group.id, Group.name)
          .joinedload(Group.category).load_only(Category.id, Category.name)
        ))
    """
    def process_items(items: List, model: ModelType):
        fields, relations = [], []
        for item in items:
            if item.name.lower() != item.name: 
                item.name = normalize_field_name(item.name)
            if item.name == '__typename':
                continue
            try:
                relation_name = getattr(model, item.name)
            except AttributeError:
                continue
            if not len(item.selections):
                fields.append(relation_name)
                continue
            related_model = relation_name.property.mapper.class_
            relations.append({relation_name: process_items(item.selections, related_model)})
        return dict(fields=fields, relations=relations)

    selections = info.selected_fields[0].selections
    options = process_items(selections, model)

    fields = [load_only(*options['fields'])] if len(options['fields']) else []

    query_options = [
        *fields,
        *flatten([get_relation_options(i) for i in options['relations']])
    ]
    

    return select(model).options(*query_options)

            
            