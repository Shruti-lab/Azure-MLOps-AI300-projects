# Agent Guidelines

## Pydantic Models vs. Python Dataclasses

Use Pydantic models for data that crosses an application boundary or needs runtime validation:

- FastAPI request and response schemas
- Configuration and environment settings
- Data loaded from documents, files, databases, queues, or external APIs
- Any user-provided or otherwise untrusted input

Define these models with `pydantic.BaseModel` or an appropriate Pydantic subclass such as `BaseSettings`. Pydantic validates fields at runtime and may coerce compatible input values according to the project's Pydantic configuration.

Use Python `@dataclass` for trusted, internal application data:

- Internal domain objects
- Internal service state and return values
- Small value objects whose fields have already been validated
- Data passed only between controlled internal functions

Dataclasses provide structure and generated methods but do not validate or coerce field types at runtime. Do not use a dataclass directly as a FastAPI boundary schema or for untrusted input.

Example:

```python
from dataclasses import dataclass

from pydantic import BaseModel


class UserAPI(BaseModel):
    id: int
    name: str


@dataclass
class UserInternal:
    id: int
    name: str
```

When adding a new model, first identify whether its data is entering or leaving the application. If it is, use Pydantic; if it is internal and already validated, use a dataclass.