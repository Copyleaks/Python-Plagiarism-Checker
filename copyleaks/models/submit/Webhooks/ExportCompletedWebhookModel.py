'''
 The MIT License(MIT)
 
 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

from typing import List
from pydantic import Field, field_validator
from .HelperModels.BaseModels.CopyleaksWebhookBaseModel import none_to_empty_list
from .HelperModels.BaseModels.WebhookModel import WebhookModel
from .HelperModels.ExportModels.TaskModel import TaskModel


class ExportCompletedWebhookModel(WebhookModel):
    """
    Represents a webhook payload indicating an export process has completed.
    Inherits from Webhook. Parse the webhook body with `ExportCompletedWebhookModel(**request.json)`.
    Check that `completed` is True, and that every task is healthy with a 2xx `http_status_code`.
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
