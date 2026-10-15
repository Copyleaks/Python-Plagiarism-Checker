from typing import List
from pydantic import Field, field_validator
from .HelperModels.BaseModels.CopyleaksWebhookBaseModel import none_to_empty_list
from .HelperModels.BaseModels.WebhookModel import WebhookModel
from .HelperModels.ExportModels.TaskModel import TaskModel


class ExportCompletedWebhookModel(WebhookModel):
    """
    Export completed webhook. Parse it with `ExportCompletedWebhookModel(**request.json)`.
    Check that `completed` is True and that every task is healthy with a 2xx `http_status_code`.
    """
    __positional_fields__ = ('completed', 'tasks')

    completed: bool = Field(
        default=False,
        description="Whether the export completed without internal errors on the Copyleaks side.",
        alias="completed"
    )

    tasks: List[TaskModel] = Field(
        default_factory=list,
        description="The export tasks, one per exported item.",
        alias="tasks"
    )

    @field_validator('tasks', mode='before')
    @classmethod
    def tasks_to_list(cls, v):
        if isinstance(v, dict):
            return [v]
        return none_to_empty_list(v)
