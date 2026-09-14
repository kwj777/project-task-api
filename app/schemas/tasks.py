"""Request and response schemas for the Task resource."""

from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    """Define fields shared by every Task schema."""

    # These type hints and Field constraints validate data at runtime and also
    # become part of the OpenAPI contract displayed by Swagger UI.
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    title: str = Field(min_length=1, max_length=60)
    description: str = Field(min_length=1, max_length=500)
    completed: bool = False
    # default supplies the value when the client omits the field; ge and le
    # make 1 and 5 inclusive bounds that Pydantic enforces and OpenAPI records.
    priority: int = Field(default=3, ge=1, le=5)
    project_id: int = Field(gt=0)


class TaskCreate(TaskBase):
    """Validate the body used to create a Task."""


class TaskUpdate(TaskBase):
    """Validate the replacement body used to update a Task."""


class TaskResponse(TaskBase):
    """Describe a Task returned by the API."""

    id: int = Field(gt=0)
