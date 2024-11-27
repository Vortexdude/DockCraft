from typing import Optional
from pydantic import BaseModel


class HttpRes(BaseModel):
    status_code: Optional[int]
    api_version: Optional[str]
    content_type: Optional[str] = "application/json"
    docker_experimental: bool
    ostype: Optional[str]
    server: Optional[str]
    date: Optional[str]
    content_length: Optional[int] = 0
    body: Optional[dict | list] = {}

    @classmethod
    def format(cls, data):
        _tmp = {}
        print(f"{data=}")
        for key, value in data.items():
            key = key.replace("-", "_").lower()
            if isinstance(value, dict):
                pass
            elif isinstance(value, list):
                pass
            elif value.isdigit():
                value = int(value)
            elif value.lower() == "true":
                value = True
            elif value.lower() == "false":
                value = False
            _tmp[key] = value

        return cls.model_validate(_tmp)
