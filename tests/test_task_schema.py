"""Unit tests for the Task priority and title rules in TaskCreate."""

import pytest
from pydantic import ValidationError

from app.schemas.tasks import TaskCreate


def make_task(**overrides):
    """Build a TaskCreate from valid defaults plus any field overrides."""
    data = {
        "title": "Write unit tests",
        "description": "Cover the Task schema rules",
        "project_id": 1,
    }
    data.update(overrides)
    return TaskCreate(**data)


def test_priority_defaults_to_three_when_omitted():
    # EP: the "priority omitted" partition always receives the default.
    task = make_task()

    assert task.priority == 3


@pytest.mark.parametrize("priority", [1, 5])
def test_priority_accepts_inclusive_bounds(priority):
    # BVA: 1 and 5 are the edges of the valid range and must be accepted.
    task = make_task(priority=priority)

    assert task.priority == priority


@pytest.mark.parametrize("priority", [0, 6])
def test_priority_rejects_values_just_outside_bounds(priority):
    # BVA: 0 and 6 sit one step outside the valid range and must be rejected.
    with pytest.raises(ValidationError) as exc_info:
        make_task(priority=priority)

    assert exc_info.value.errors()[0]["loc"] == ("priority",)


def test_title_accepts_60_characters_and_rejects_61():
    # BVA: 60 characters is the maximum; 61 is one past it.
    assert len(make_task(title="a" * 60).title) == 60

    with pytest.raises(ValidationError) as exc_info:
        make_task(title="a" * 61)

    assert exc_info.value.errors()[0]["type"] == "string_too_long"


def test_title_of_only_whitespace_is_rejected():
    # EP: whitespace-only titles form an invalid partition, because
    # str_strip_whitespace empties them before min_length=1 is checked.
    with pytest.raises(ValidationError) as exc_info:
        make_task(title="   ")

    assert exc_info.value.errors()[0]["type"] == "string_too_short"
