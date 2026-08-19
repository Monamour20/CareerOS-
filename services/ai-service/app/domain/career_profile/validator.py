import json
import re
from types import UnionType
from typing import Any, Union, get_args, get_origin

from pydantic import BaseModel, ValidationError

from app.core.errors import CareerProfileValidationError, InvalidLLMOutputError
from app.domain.career_profile.models import CareerProfile, ExperienceItem


class CareerProfileValidator:
    def validate(self, llm_output: str | dict[str, Any]) -> CareerProfile:
        if isinstance(llm_output, dict):
            payload = llm_output
        else:
            payload = self._parse_json(llm_output)

        try:
            return CareerProfile.model_validate(payload)
        except ValidationError:
            repaired = self._repair_model_payload(payload, CareerProfile)
            try:
                return CareerProfile.model_validate(repaired)
            except ValidationError as repaired_exc:
                raise CareerProfileValidationError(
                    "LLM output did not match the CareerProfile schema."
                ) from repaired_exc

    def _parse_json(self, output: str) -> dict[str, Any]:
        cleaned = output.strip()
        cleaned = self._strip_markdown_fence(cleaned)
        candidates = [cleaned]

        extracted = self._extract_first_json_object(cleaned)
        if extracted and extracted != cleaned:
            candidates.append(extracted)

        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
            except json.JSONDecodeError:
                continue
            if isinstance(parsed, dict):
                return parsed

        raise InvalidLLMOutputError("LLM did not return valid JSON.")

    def _strip_markdown_fence(self, value: str) -> str:
        match = re.fullmatch(
            r"```(?:json)?\s*(.*?)\s*```", value, flags=re.DOTALL | re.IGNORECASE
        )
        return match.group(1).strip() if match else value

    def _extract_first_json_object(self, value: str) -> str | None:
        start = value.find("{")
        end = value.rfind("}")
        if start == -1 or end == -1 or end <= start:
            return None
        return value[start : end + 1]

    def _repair_model_payload(self, value: Any, model_type: type[BaseModel]) -> dict[str, Any]:
        if not isinstance(value, dict):
            return {}

        normalized = {self._normalize_key(key): item for key, item in value.items()}
        normalized = self._apply_aliases(normalized, model_type)
        repaired: dict[str, Any] = {}

        for field_name, field in model_type.model_fields.items():
            if field_name not in normalized:
                continue
            repaired[field_name] = self._repair_value(normalized[field_name], field.annotation)

        return repaired

    def _repair_value(self, value: Any, annotation: Any) -> Any:
        origin = get_origin(annotation)
        args = get_args(annotation)

        if origin in (UnionType, Union):
            non_none_args = [arg for arg in args if arg is not type(None)]
            if value is None:
                return None
            if str in non_none_args and value == "":
                return None
            if str in non_none_args and value in ([], {}):
                return None
            if non_none_args:
                return self._repair_value(value, non_none_args[0])

        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            return self._repair_model_payload(value, annotation)

        if origin is list and args:
            item_type = args[0]
            if not isinstance(value, list):
                return []
            repaired_items = [self._repair_value(item, item_type) for item in value]
            return [item for item in repaired_items if item is not None]

        if annotation is str:
            if value in (None, "", [], {}):
                return None
            if isinstance(value, dict):
                for key in ("url", "link", "href", "name", "title", "type", "label", "value"):
                    item = value.get(key)
                    if isinstance(item, str) and item.strip():
                        return item
                for item in value.values():
                    if isinstance(item, str) and item.strip():
                        return item
                return None
            if isinstance(value, list):
                strings = [item for item in value if isinstance(item, str) and item.strip()]
                return ", ".join(strings) if strings else None
            return str(value)

        return value

    def _normalize_key(self, key: Any) -> str:
        return str(key).strip().lstrip(".")

    def _apply_aliases(self, value: dict[str, Any], model_type: type[BaseModel]) -> dict[str, Any]:
        if model_type is ExperienceItem:
            if "title" not in value and "role" in value:
                value["title"] = value["role"]
            if "company" not in value and "organization" in value:
                value["company"] = value["organization"]
        return value
