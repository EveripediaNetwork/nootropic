import re
import json
from typing import Dict, List, Optional, Union, Any
from abc import ABC, abstractmethod


class BaseExtractor(ABC):
    @staticmethod
    @abstractmethod
    def extract(
        text: str,
        **kwargs: Any,
    ) -> Union[Dict[str, Any], List[Any]]:
        pass


class XMLExtractor(BaseExtractor):
    @staticmethod
    def extract(
        text: str,
        tag: Optional[str] = None,
    ) -> Union[Dict[str, Any], List[str]]:
        def parse_xml(xml_string: str) -> Dict[str, Any]:
            pattern = r'<(\w+)(?:\s+[^>]*)?>(.*?)</\1>'
            matches = re.findall(pattern, xml_string, re.DOTALL)
            result = {}
            for tag_name, content in matches:
                content = content.strip()
                if re.search(r'<\w+', content):
                    result[tag_name] = parse_xml(content)
                else:
                    result[tag_name] = content
            return result

        if tag:
            pattern = '<{0}>(.*?)</{0}>'.format(tag)
            matches = re.findall(pattern, text, re.DOTALL)
            return [
                parse_xml('<root>{0}</root>'.format(m))['root']
                for m in matches
            ]
        else:
            return parse_xml(text)


class JSONExtractor(BaseExtractor):
    @staticmethod
    def extract(text: str) -> List[Dict[str, Any]]:
        def find_json_objects(text: str) -> List[str]:
            # Find all JSON-like structures in the text
            json_pattern = r'\{(?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*\}'
            return re.findall(json_pattern, text)

        def parse_json_object(json_str: str) -> Optional[Dict[str, Any]]:
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                # If parsing fails, return None
                return None

        json_strings = find_json_objects(text)
        return [
            json_obj for json_obj in map(parse_json_object, json_strings)
            if json_obj is not None
        ]
