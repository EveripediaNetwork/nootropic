#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional, Callable


class BaseWrapper:
    def __init__(
        self,
        client_attr: Any,
        prefix: Optional[str] = None,
        postfix: Optional[str] = None,
        system: Optional[str] = None,
    ):
        self._client_attr = client_attr
        self._prefix = prefix
        self._postfix = postfix
        self._system = system

    def _modify_messages(self, messages: List[Dict[str, str]]) -> None:
        for message in messages:
            if message['role'] == 'user':
                message['content'] = self._modify_content(message['content'])

    def _handle_system_prompt(self, kwargs: Dict[str, Any]) -> None:
        if self._system:
            kwargs['system'] = self._system

    def _modify_content(self, content: str) -> str:
        if self._prefix:
            content = '{0} {1}'.format(self._prefix, content)
        if self._postfix:
            content = '{0} {1}'.format(content, self._postfix)
        return content


class GenerateWrapper(BaseWrapper):
    def __call__(
        self,
        prompt: Optional[str] = None,
        system_prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        **kwargs: Any,
    ) -> str:
        if messages:
            self._modify_messages(messages)
            kwargs['messages'] = messages
        elif prompt:
            kwargs['prompt'] = self._modify_content(prompt)

        if system_prompt or self._system:
            kwargs['system_prompt'] = system_prompt or self._system

        return self._client_attr(**kwargs)


class ChatWrapper(BaseWrapper):
    def __call__(self, **kwargs: Any) -> Any:
        if 'messages' in kwargs:
            self._modify_messages(kwargs['messages'])
        self._handle_system_prompt(kwargs)

        return self._client_attr.chat(**kwargs)

    @property
    def completions(self) -> 'CompletionsWrapper':
        return CompletionsWrapper(
            self._client_attr.completions,
            self._prefix,
            self._postfix,
            self._system,
        )


class CompletionsWrapper(BaseWrapper):
    def create(self, **kwargs: Any) -> Any:
        if 'messages' in kwargs:
            self._modify_messages(kwargs['messages'])
        if self._system:
            kwargs['messages'] = [
                {
                    'role': 'system',
                    'content': self._system,
                },
            ] + kwargs.get('messages', [])

        return self._client_attr.create(**kwargs)


class MessagesWrapper(BaseWrapper):
    def create(self, **kwargs: Any) -> Any:
        if 'messages' in kwargs:
            self._modify_messages(kwargs['messages'])
        self._handle_system_prompt(kwargs)

        return self._client_attr.create(**kwargs)

    def stream(self, **kwargs: Any) -> Any:
        if 'messages' in kwargs:
            self._modify_messages(kwargs['messages'])
        self._handle_system_prompt(kwargs)

        return self._client_attr.stream(**kwargs)


class Nootropic:
    def __init__(
        self,
        client: Any,
        prefix: Optional[str] = None,
        postfix: Optional[str] = None,
        system: Optional[str] = None,
    ):
        self._client = client
        self._prefix = prefix
        self._postfix = postfix
        self._system = system

    # Fallback to the original client
    def __getattr__(self, name: str) -> Any:
        return getattr(self._client, name)

    @property
    def generate(self) -> Callable:
        return GenerateWrapper(
            self._client.generate,
            self._prefix,
            self._postfix,
            self._system,
        )

    @property
    def chat(self) -> ChatWrapper:
        return ChatWrapper(
            self._client.chat,
            self._prefix,
            self._postfix,
            self._system,
        )

    @property
    def messages(self) -> MessagesWrapper:
        return MessagesWrapper(
            self._client.messages,
            self._prefix,
            self._postfix,
            self._system,
        )
