import typing

import strawberry
import uvicorn
from dependency_injector import containers, providers
from dependency_injector.wiring import Provide, inject
from fastapi import FastAPI
from strawberry.extensions import FieldExtension
from strawberry.fastapi import GraphQLRouter
from strawberry.types import Info


class DependencyExtension(FieldExtension):
    def __init__(self):
        self.dependency_args: list[typing.Any] = []

    def apply(self, field) -> None:
        # Remove dependency_injector provider arguments from the list that strawberry tries to resolve
        di_arguments = []
        keep_arguments = []
        for arg in field.arguments:
            if isinstance(arg.default, Provide):
                di_arguments.append(arg)
                continue
            keep_arguments.append(arg)
        field.arguments = keep_arguments
        self.dependency_args = di_arguments

    async def resolve_async(
        self,
        next_: typing.Callable[..., typing.Any],
        source: typing.Any,
        info: Info,
        **kwargs,
    ) -> typing.Any:
        res = await next_(source, info, **kwargs)
        return res