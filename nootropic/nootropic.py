#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Any, Dict, List, Optional, Union
import uuid
import copy


class BaseWrapper:
    def __init__(
        self,
        client_attr: Any,
        prefix: Optional[str] = None,
        postfix: Optional[str] = None,
        system: Optional[str] = None,
        disable_cache: bool = False,
    ):
        self._client_attr = client_attr
        self._prefix = prefix
        self._postfix = postfix
        self._system = system
        self._disable_cache = disable_cache

    def _shallow_copy_messages(
        self,
        messages: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        copied_messages = list(messages)

        for i, message in enumerate(copied_messages):
            copied_messages[i] = dict(message)

        return copied_messages

    def _modify_messages(
        self,
        messages: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        modified_messages = self._shallow_copy_messages(messages)
        for message in modified_messages:
            if message['role'] == 'user':
                message['content'] = self._modify_content(message['content'])
        return modified_messages

    def _modify_content(self, content: str) -> str:
        if self._disable_cache:
            prompt_uid = str(uuid.uuid4())
            content = '{0} {1}'.format(
                '<ignore>{0}</ignore>\n\n'.format(prompt_uid),
                content,
            )
        if self._prefix:
            content = '{0} {1}'.format(self._prefix, content)
        if self._postfix:
            content = '{0} {1}'.format(content, self._postfix)

        return content

    def _add_system_message(
        self,
        messages: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        modified_messages = copy.deepcopy(messages)
        system_message = {
            'role': 'system',
            'content': self._system,
        }
        if modified_messages and modified_messages[0]['role'] == 'system':
            modified_messages[0] = system_message
        else:
            modified_messages.insert(0, system_message)
        return modified_messages

    def __getattr__(self, name: str) -> Any:
        raise NotImplementedError(
            'Method {0} is not implemented in BaseWrapper'.format(name),
        )


# llmdk
class GenerateWrapper(BaseWrapper):
    def __call__(
        self,
        prompt_or_messages: Union[str, List[Dict[str, str]]],
        system: Optional[str] = None,
        **kwargs: Any,
    ) -> str:
        if isinstance(prompt_or_messages, list):
            kwargs['prompt_or_messages'] = self._modify_messages(
                prompt_or_messages,
            )
        else:
            kwargs['prompt_or_messages'] = self._modify_content(
                prompt_or_messages,
            )

        if system or self._system:
            kwargs['system'] = system or self._system

        return self._client_attr(**kwargs)

    def __getattr__(self, name: str) -> Any:
        raise NotImplementedError(
            'Method {0} is not implemented in GenerateWrapper'.format(name),
        )


# llmdk
class StreamWrapper(BaseWrapper):
    def __call__(
        self,
        prompt_or_messages: Union[str, List[Dict[str, str]]],
        system: Optional[str] = None,
        **kwargs: Any,
    ) -> Any:
        if isinstance(prompt_or_messages, list):
            kwargs['prompt_or_messages'] = self._modify_messages(
                prompt_or_messages,
            )
        else:
            kwargs['prompt_or_messages'] = self._modify_content(
                prompt_or_messages,
            )

        if system or self._system:
            kwargs['system'] = system or self._system

        return self._client_attr(**kwargs)

    def __getattr__(self, name: str) -> Any:
        raise NotImplementedError(
            'Method {0} is not implemented in StreamWrapper'.format(name),
        )


# OpenAI, HuggingFace, Groq, Ollama
class ChatWrapper(BaseWrapper):
    def __call__(self, **kwargs: Any) -> Any:
        if 'messages' in kwargs:
            kwargs['messages'] = self._modify_messages(kwargs['messages'])
        if self._system:
            messages = kwargs.get('messages', [])
            kwargs['messages'] = self._add_system_message(messages)
        return self._client_attr(**kwargs)

    @property
    def completions(self) -> 'CompletionsWrapper':
        return CompletionsWrapper(
            self._client_attr.completions,
            self._prefix,
            self._postfix,
            self._system,
            self._disable_cache,
        )

    def __getattr__(self, name: str) -> Any:
        raise NotImplementedError(
            'Method {0} is not implemented in ChatWrapper'.format(name),
        )


# OpenAI, HuggingFace, Groq
class CompletionsWrapper(BaseWrapper):
    def create(self, **kwargs: Any) -> Any:
        if 'messages' in kwargs:
            kwargs['messages'] = self._modify_messages(kwargs['messages'])
        if self._system:
            messages = kwargs.get('messages', [])
            kwargs['messages'] = self._add_system_message(messages)

        return self._client_attr.create(**kwargs)

    def __getattr__(self, name: str) -> Any:
        raise NotImplementedError(
            'Method {0} is not implemented in CompletionsWrapper'.format(name),
        )


# Anthropic
class MessagesWrapper(BaseWrapper):
    def _prepare_kwargs(self, kwargs: Dict[str, Any]) -> None:
        if 'messages' in kwargs:
            kwargs['messages'] = self._modify_messages(kwargs['messages'])
        if self._system:
            kwargs['system'] = self._system

    def create(self, **kwargs: Any) -> Any:
        self._prepare_kwargs(kwargs)
        return self._client_attr.create(**kwargs)

    def stream(self, **kwargs: Any) -> Any:
        self._prepare_kwargs(kwargs)
        return self._client_attr.stream(**kwargs)

    def __getattr__(self, name: str) -> Any:
        raise NotImplementedError(
            'Method {0} is not implemented in MessagesWrapper'.format(name),
        )


class Nootropic:
    def __init__(
        self,
        client: Any,
        prefix: Optional[str] = None,
        postfix: Optional[str] = None,
        system: Optional[str] = None,
        disable_cache: bool = False,
    ):
        self._client = client
        self._prefix = prefix
        self._postfix = postfix
        self._system = system
        self._disable_cache = disable_cache

    def __getattr__(self, name: str) -> Any:
        raise NotImplementedError(
            'Method {0} is not implemented in Nootropic'.format(name),
        )

    def _create_wrapper(self, attr_name: str, wrapper_class: type) -> Any:
        return wrapper_class(
            getattr(self._client, attr_name, self._client),
            self._prefix,
            self._postfix,
            self._system,
            self._disable_cache,
        )

    # LLMDK
    @property
    def generate(self) -> GenerateWrapper:
        return self._create_wrapper('generate', GenerateWrapper)

    # LLMDK
    @property
    def stream(self) -> StreamWrapper:
        return self._create_wrapper('stream', StreamWrapper)

    # OpenAI, HuggingFace, Groq, Ollama
    @property
    def chat(self) -> ChatWrapper:
        return self._create_wrapper('chat', ChatWrapper)

    # Anthropic
    @property
    def messages(self) -> MessagesWrapper:
        return self._create_wrapper('messages', MessagesWrapper)
