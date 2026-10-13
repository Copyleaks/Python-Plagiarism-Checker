# Changelog

All notable changes to the Copyleaks Python SDK (`pip install copyleaks`) are listed here.

## 6.0.0

This is a major release. The AI Text Detection and Grammar Checker clients now return typed models instead of dicts, and the completed webhook now parses its notifications into typed models. Read the upgrade notes below before you upgrade from 5.x.

### Added

- **New submit properties (BAC-5378).**
  - `ScanProperties.set_ai_source_match(AISourceMatch)`: finds online sources suspected of containing AI-generated text. Turn it on with `AISourceMatch().set_enable(True)`. It currently applies only to documents detected as English. When you leave it unset, the server default (disabled) applies.
  - `ScanProperties.set_display_language(value)`: the language of the scan's PDF report. One of `"en"`, `"es"`, `"pt"`, `"fr"`, `"de"`, `"it"`. The server default is `"en"`.
  - `Pdf.set_report_version(value)`: which version of the PDF report to generate. One of `"v1"`, `"v2"`, `"v3"`, `"latest"` (lowercase strings, not the `PdfVersion` enum). It overrides `Pdf.set_version` when both are set.
- **AI alert in the completed webhook (BAC-5392).**
  - `CompletedWebhookModel.get_ai_detection_alert()` returns the `suspected-ai-text` alert as an `AlertsModel`, or `None` when the scan has no AI alert.
  - `AlertsModel.get_ai_detection_result()` and the shortcut `CompletedWebhookModel.get_ai_detection_result()` decode the alert's `additionalData` JSON string into a typed `CopyleaksAiTextDetectionResponseModel`. They return `None` when there is no AI alert, or when `additionalData` is empty or is JSON that is not an object. They raise `pydantic.ValidationError` when `additionalData` is not valid JSON or does not match the model.
  - New constant `CopyleaksAlertCodes.SUSPECTED_AI_TEXT` (`"suspected-ai-text"`).
  - New AI Text Detection models in `copyleaks.models.AiDetection.Responses`.
- **Typed response models (BAC-5370).**
  - `AiDetectionClient.submit_natural_language` returns a `CopyleaksAiTextDetectionResponseModel`, with attributes such as `summary.ai`, `summary.human`, `model_version`, `results`, `explain`, `scanned_document` and `scan_type`.
  - `WritingAssistantClient.submit_text` (Grammar Checker) returns a `CopyleaksWritingAssistantResponseModel`, with attributes such as `score.corrections.overall_score`, `score.readability`, `corrections.text.chars` and `scanned_document`.
  - New Grammar Checker models in `copyleaks.models.WritingAssistant.Responses`.

### Changed

- **AI Text Detection and Grammar Checker responses are models, not dicts (BAC-5370).** See the upgrade notes.
- **Completed webhook notifications are typed (BAC-5392).** When you build `CompletedWebhookModel(**request.json)`, `notifications` is now a `NotificationsModel` with an `alerts` list of `AlertsModel` objects. In 5.x it stayed the raw dict. `AlertsModel` fields are now public: `category`, `code`, `title`, `message`, `help_link`, `severity` and `additional_data`. `AlertsModel(**alert_json)` accepts the camelCase webhook keys `helpLink` and `additionalData`. Null entries in `alerts` are skipped.
- **README (BAC-5374).** The README now describes the SDK as the Copyleaks platform SDK and lists the products it covers: AI Text Detection, AI Image Detection, Plagiarism Checker, Grammar Checker and Text Moderation. Headings such as "AI Text Detection" now use the product names. There are no code changes in this item.

### Fixed

- **OCR submit (BAC-6742).** `Copyleaks.submit_file_ocr` now calls `PUT /v3/scans/submit/ocr/{scanId}`. Earlier versions called `/v3/scans/submit/file/ocr/{scanId}`, which does not exist, so every OCR submit failed with HTTP 404.

### Upgrade notes

- **Install:** `pip install --upgrade copyleaks`. If you pin versions, change the pin to `copyleaks>=6,<7`. The package name and import paths are unchanged.
- **Typed responses (BAC-5370): what stays backward compatible.** Read-only dict access still works on both response models:
  - `response['summary']['ai']`
  - `response.get('explain')`
  - `'explain' in response`

  Keys are the camelCase names the model defines, and nested values are plain dicts and lists. Values and key names follow the model, not the raw JSON: for example an integer in a float field comes back as a float, a null list as `[]`, and the PascalCase keys some sandbox responses use (`Ai`, `Human`) as camelCase (`ai`, `human`). Only keys that the model defines and that the server sent are available.
- **Typed responses (BAC-5370): what you need to change.** The responses are no longer `dict` objects, so the following no longer work:
  - `isinstance(response, dict)` is `False`.
  - `json.dumps(response)` raises `TypeError`.
  - Dict methods other than `get()`, such as `keys()` and `items()`, do not exist. `len(response)` raises `TypeError`.
  - Assigning a key (`response['x'] = 1`) fails.
  - Iterating over a response yields `(field_name, value)` pairs, not the JSON keys.
  - Fields that the server sends but the model does not define are dropped.

  If you need a plain dict, call `response.model_dump(by_alias=True, exclude_unset=True)`. For new code, prefer attributes such as `response.summary.ai`.
- **Typed responses (BAC-5370): errors.** If the server returns a success response whose body does not match the model, the call raises `pydantic.ValidationError`.
- **Completed webhook (BAC-5392).** `notifications` and its alerts are now models, so dict access on them raises `TypeError`. Change `completed.notifications['alerts']` and `completed.notifications.get('alerts')` to `completed.notifications.alerts`, `alert['code']` to `alert.code`, and `alert['additionalData']` to `alert.additional_data`. Code that built alerts by hand and read `_code` or `_additional_data` should use `code` and `additional_data`. To read the AI alert, use `completed.get_ai_detection_alert()` and `get_ai_detection_result()`.
