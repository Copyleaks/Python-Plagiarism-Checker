# Changelog

All notable changes to the Copyleaks Python SDK (`pip install copyleaks`) are listed here.

## 6.0.0

This is a major release. It adds AI Video Detection, Image Plagiarism Detection, asynchronous AI Image Detection and four lookup endpoints, and the scan options and response fields of the current API. The AI Text Detection and Grammar Checker clients now return typed models instead of dicts, and the webhook models now parse the webhook JSON into typed models. Every call now goes through one shared connection pool and has a timeout. Read the upgrade notes below before you upgrade from 5.x.

### Added

- **New endpoints.**
  - `Copyleaks.ImagePlagiarismClient.check(auth_token, scan_id, CopyleaksImagePlagiarismRequestModel)`: Image Plagiarism Detection. Searches the web for copies of an image and returns a `CopyleaksImagePlagiarismResponseModel` with the full and partial matches and the pages where they were found. The image is uploaded as multipart/form-data. Supports `sandbox` and `developer_payload`.
  - `Copyleaks.VideoDetectionClient.submit(auth_token, scan_id, CopyleaksAiVideoDetectionRequestModel)`: AI Video Detection. Submits a video URL; the result is posted to your webhook. Parse it with `CopyleaksAiVideoDetectionResponseModel(**request.json)`. New constant `CopyleaksAiVideoDetectionModels.AI_VIDEO_1_PRO`.
  - `Copyleaks.ImageDetectionClient.submit_async(auth_token, scan_id, CopyleaksAiImageDetectionAsyncRequestModel)`: asynchronous AI Image Detection of an image URL, with the result posted to your webhook. Parse it with `CopyleaksAiImageDetectionResponseModel(**request.json)`.
  - `Copyleaks.AiDetectionClient.credits_balance(auth_token)`: the AI Text Detector credit balance, as a `CopyleaksAiTextDetectionCreditsResponseModel`.
  - `Copyleaks.allowed_cross_languages()`: the languages supported by cross-language plagiarism detection, as a `CopyleaksAllowedCrossLanguagesResponseModel`. `document_languages` and `result_languages` map each language name to its code, and `document_language_codes` and `result_language_codes` list the codes. Public, no login needed.
  - `Copyleaks.supported_ai_text_detection_file_types()`: the file types supported by AI Text Detection. Public, no login needed.
  - `Copyleaks.repository_info(auth_token, repository_id)`: the information of a Private Cloud Hub repository (credits, masking policy, status). New constants `CopyleaksRepositoryRoles` and `CopyleaksRepositoryStatuses`.
- **AI Image Detection.**
  - `Copyleaks.ImageDetectionClient.submit_file(auth_token, scan_id, CopyleaksAiImageDetectionFileRequestModel)` uploads the image file as multipart/form-data, without base64. It is faster and uses less memory for large images.
  - New request options `mask_type` ("binary", "heatmap" or "none", see `CopyleaksAiImageMaskTypes`) and `object_detection` (up to 3 objects such as "face" or "hand").
  - New response fields `is_ai_detected`, `detected_objects`, `result.labels`, `image_info.metadata.content_summary`, `scan_type` and `developer_payload`.
  - `.avif` images are accepted.
- **New scan properties** on `ScanProperties`:
  - `set_sensitive_data_protection(SensitiveDataProtection)`: mask driver's licenses, credentials, passports, network identifiers, URLs, email addresses, credit cards and phone numbers.
  - `set_writing_feedback(WritingFeedback)`: run the Grammar Checker in the scan, with optional `ScoreWeights`.
  - `set_overview(Overview)`: Gen-AI Overview, with its `ignore_*` options.
  - `set_internal_ai_source_match(InternalAISourceMatch)`: match against the Copyleaks internal AI database.
  - `set_references(References)`: Citation Checker.
  - `set_scan_time_zone(value)`, `set_course(Course)`, `set_assignment(Assignment)` and `set_institution(Institution)`.
  - `AIGeneratedText.set_sensitivity(1 to 3)` and `AIGeneratedText.set_explain(AIGeneratedTextExplain)` (AI Logic).
  - `Scanning.set_include(ScanningInclude)`, `ScanningExclude.set_backlinks_domains(...)`, `ScanningExclude.set_text(...)` and `Indexing.set_copyleaks_db(...)`.
  - PDF report colors `ReportCustomizationColors.set_ai_detection(...)` and `set_writing_feedback(...)`, `Pdf.set_colors(...)`, and `PdfVersion.V3`.
- **New request fields.**
  - `UrlDocument.set_verb(...)` and `UrlDocument.set_headers(...)`, to scan URLs that need a POST or custom headers.
  - `Delete.set_headers(...)` for the completion webhook.
  - `Export.set_completion_webhook_headers(...)`, and the export targets `Export.set_ai_detection(ExportAiDetection)`, `set_writing_feedback(ExportWritingFeedback)` and `set_overview(ExportOverview)`.
  - `NaturalLanguageDocument.set_explain(...)` (AI Logic) and `NaturalLanguageDocument.set_sensitivity(1 to 3)` for AI Text Detection.
- **New response and webhook fields.**
  - Completed webhook: `developer_payload`, `scanned_document`, `references_validation`, `results.internal_ai_data` and typed `results`.
  - Error webhook: `error.type`, `error.id`, `error.url` and `error.details`.
  - New result webhook: `internal_ai_data`.
  - Text Moderation response: `modelVersion`.
- **Timeouts and connections.** `Copyleaks.set_timeout(...)` and `Copyleaks.get_timeout()` set the default timeout of every call, and every method that calls the API accepts `timeout=` for that call. `Copyleaks.set_session(...)` sends the calls through your own `requests.Session`, for example to use a proxy.
- **Error details.** `RateLimitError` and `UnderMaintenanceError` now carry the response: `get_response()`, `status_code`, and `retry_after` (the `Retry-After` header in seconds). `CommandError` has `status_code`, and its message is `HTTP <status>: <response body>`.
- **AI alert in the completed webhook.**
  - `CompletedWebhookModel.get_ai_detection_alert()` returns the `suspected-ai-text` alert as an `AlertsModel`, or `None` when the scan has no AI alert.
  - `AlertsModel.get_ai_detection_result()` and the shortcut `CompletedWebhookModel.get_ai_detection_result()` decode the alert's `additionalData` JSON string into a typed `CopyleaksAiTextDetectionResponseModel`. They return `None` when there is no AI alert, or when `additionalData` is empty or is JSON that is not an object. They raise `pydantic.ValidationError` when `additionalData` is not valid JSON or does not match the model.
  - New constant `CopyleaksAlertCodes.SUSPECTED_AI_TEXT` (`"suspected-ai-text"`).
  - New AI Text Detection models in `copyleaks.models.AiDetection.Responses`.
- **New submit properties.**
  - `ScanProperties.set_ai_source_match(AISourceMatch)`: finds online sources suspected of containing AI-generated text. Turn it on with `AISourceMatch().set_enable(True)`. It currently applies only to documents detected as English. When you leave it unset, the server default (disabled) applies.
  - `ScanProperties.set_display_language(value)`: the language of the scan's PDF report. One of `"en"`, `"es"`, `"pt"`, `"fr"`, `"de"`, `"it"`. The server default is `"en"`.
  - `Pdf.set_report_version(value)`: which version of the PDF report to generate. One of `"v1"`, `"v2"`, `"v3"`, `"latest"` (lowercase strings, not the `PdfVersion` enum). It overrides `Pdf.set_version` when both are set.
- **Typed response models.**
  - `AiDetectionClient.submit_natural_language` returns a `CopyleaksAiTextDetectionResponseModel`, with attributes such as `summary.ai`, `summary.human`, `model_version`, `results`, `explain`, `scanned_document` and `scan_type`.
  - `WritingAssistantClient.submit_text` (Grammar Checker) returns a `CopyleaksWritingAssistantResponseModel`, with attributes such as `score.corrections.overall_score`, `score.readability`, `corrections.text.chars` and `scanned_document`.
  - New Grammar Checker models in `copyleaks.models.WritingAssistant.Responses`.

### Changed

- **One shared connection pool.** Every call goes through one `requests.Session`, so TCP and TLS connections are kept alive and reused instead of opened for every call. The default session retries connection errors only, never a request that may have reached the server.
- **Every call has a timeout.** The default is 10 seconds to connect and 180 seconds to read the response. Earlier versions waited forever.
- **HTTP 429 raises `RateLimitError` on every call.** Earlier versions did this only for the credits balance and the usage history, and raised `CommandError` everywhere else. `RateLimitError` is now a subclass of `CommandError`, so code that catches `CommandError` still catches it.
- **AI Text Detection and Grammar Checker responses are models, not dicts.** See the upgrade notes.
- **Webhook models are typed.** `CompletedWebhookModel(**request.json)` and the other webhook models now parse every documented field into typed models with snake_case attributes, for example `completed.scanned_document.scan_id` and `completed.results.internet[0].url`. Fields the model does not define are kept. `AlertsModel(**alert_json)` accepts the camelCase webhook keys `helpLink` and `additionalData`, and null entries in `alerts` are skipped.
- **Dict-style reads are faster.** A typed response is converted to a dict once, on the first `response['key']` read, and reused by later reads, instead of being converted on every read.
- **Smaller request bodies.** Requests are sent as compact JSON. `toJSON()` of the request objects returns compact JSON without indentation or sorted keys.
- `Copyleaks.supported_file_types()` calls the documented `/v3/miscellaneous/supported-plagiarism-file-types` path. The response is the same.
- Text Moderation requests leave out unset fields instead of sending them as `null`.
- The SDK writes nothing to stdout. Failed calls are logged at DEBUG level on the `copyleaks` logger.

### Fixed

- **Cross-language scans.** `Scanning.set_cross_languages` was sent as `cross_languages`, which the API ignores, so cross-language plagiarism detection never ran. It is now sent as `crossLanguages`.
- **PDF report colors.** `Pdf.set_report_customization_colors` was sent as `report_customization_colors`, which the API ignores. It is now sent as `colors`.
- **Webhook models dropped data.** `CompletedWebhookModel(**request.json)` always had `scanned_document` and `developer_payload` set to `None`, and kept `results` as a raw dict. The same happened in `CreditsCheckedWebhookModel`, `ErrorWebhookModel`, `NewResultWebhookModel`, `IndexedWebhookModel` and `ExportCompletedWebhookModel`. `ExportCompletedWebhookModel.tasks` is now a list.
- **OCR submit.** `Copyleaks.submit_file_ocr` now calls `PUT /v3/scans/submit/ocr/{scanId}`. Earlier versions called `/v3/scans/submit/file/ocr/{scanId}`, which does not exist, so every OCR submit failed with HTTP 404.
- AI Image Detection printed the error response to stdout on every failed call.
- AI Image Detection failed with `ValidationError` when the response had no `result` (the "none" mask type). The response fields are now optional.
- Text Moderation failed with `ValidationError` when the response had no credit counts, and sent `"labels": null` when no labels were given.
- `ScoreWeights` rejected a weight of `0.0`. Weights from `0.0` to `1.0` are accepted.
- `WritingAssistantDocument.set_sandbox(False)` and `IndexingRepository.set_masking_policy(MaskingPolicy.NoMask)` raised `AssertionError`.
- `ScanningExclude.set_id_pattern` accepted only booleans. It now takes the pattern string.
- Getters that returned the wrong value: `Filters.get_minor_changes_enabled` (and the new `Filters.get_related_meaning_enabled`), `Filters.get_allow_same_domain`, `Author.get_id` and `Delete.get_purge`.
- `WritingAssistantClient.get_correction_types` raised `CommandError` with the response bytes instead of the response.
- Token expiry checks no longer use the deprecated `datetime.utcnow()`.

### Upgrade notes

- **Install:** `pip install --upgrade copyleaks`. If you pin versions, change the pin to `copyleaks>=6,<7`. The package name and import paths are unchanged.
- **Cross-language scans now run, and cost credits.** If your code called `Scanning.set_cross_languages`, those scans were plain scans in 5.x. In 6.0.0 they scan the extra languages, and each additional language uses credits per page. Remove the call if you do not want cross-language scans. Get the supported languages with `Copyleaks.allowed_cross_languages()`.
- **PDF report colors now apply.** Colors set with `Pdf.set_report_customization_colors` were ignored in 5.x and now change the PDF report.
- **Timeouts.** A call that takes longer than the timeout now raises `requests.exceptions.Timeout`. If you send very long texts or large files, raise the timeout with `Copyleaks.set_timeout((10, 600))` or `timeout=` on the call. `Copyleaks.set_timeout(None)` restores the 5.x behavior of no timeout.
- **Tests that mock `requests`.** The SDK no longer calls `requests.get`, `requests.post`, `requests.put` or `requests.patch`. If your tests patched them, patch `requests.Session.request` instead, or pass a fake session to `Copyleaks.set_session(...)` and reset it with `Copyleaks.set_session(None)`.
- **HTTP 429.** Every call now raises `RateLimitError` on HTTP 429. It is a `CommandError`, so existing `except CommandError` blocks still catch it. If you catch both, put `except RateLimitError` first.
- **Text Moderation `labels`.** `CopyleaksTextModerationRequestModel` now requires `labels` with 1 to 16 labels, and each label id is 1 to 32 characters. The API already rejected requests without labels.
- **Typed responses: what stays backward compatible.** Read-only dict access still works on the AI Text Detection, Grammar Checker and new response models, and on the webhook models and their nested models:
  - `response['summary']['ai']`
  - `response.get('explain')`
  - `'explain' in response`
  - `completed.results['internet'][0]['url']`, `completed.notifications['alerts']`

  Keys are the camelCase names the model defines, and nested values are plain dicts and lists. Values and key names follow the model, not the raw JSON: for example an integer in a float field comes back as a float, a null list as `[]`, and the PascalCase keys some sandbox responses use (`Ai`, `Human`) as camelCase (`ai`, `human`). Only keys that the model defines and that the server sent are available. Treat responses as read-only: the dict is built on the first dict-style read.
- **Typed responses: what you need to change.** The responses are no longer `dict` objects, so the following no longer work:
  - `isinstance(response, dict)` is `False`.
  - `json.dumps(response)` raises `TypeError`.
  - Dict methods other than `get()`, such as `keys()` and `items()`, do not exist. `len(response)` raises `TypeError`.
  - Assigning a key (`response['x'] = 1`) fails.
  - Iterating over a response yields `(field_name, value)` pairs, not the JSON keys.
  - Fields that the server sends but the model does not define are dropped.

  If you need a plain dict, call `response.model_dump(by_alias=True, exclude_unset=True)`. For new code, prefer attributes such as `response.summary.ai`.
- **Typed responses: errors.** If the server returns a success response whose body does not match the model, the call raises `pydantic.ValidationError`.
- **Webhook models.** The nested webhook values (`results`, `notifications`, `error`, `score`, `tasks` and the result lists) are now models instead of raw dicts. The dict-style reads above still work, but `isinstance(..., dict)` and `json.dumps(...)` on them do not; use `model_dump(by_alias=True)` to get the JSON back. Prefer attributes, for example `completed.notifications.alerts`, `alert.code` and `alert.additional_data`. The helper models now keep their data in public fields: code that built them by hand and read underscore attributes such as `_scan_id`, `_code` or `_additional_data` should use `scan_id`, `code` and `additional_data`. The keyword arguments `id_val` and `endpont` still work and map to `id` and `endpoint`.
- **AI Image Detection response.** All fields of `CopyleaksAiImageDetectionResponseModel` are now optional. `result` is `None` when the request used the "none" mask type.
- **Request objects.** `toJSON()` returns compact JSON. `Pdf` stores its colors in `colors` (was `report_customization_colors`) and `Scanning` stores cross-languages in `crossLanguages` (was `cross_languages`); use the getters. `ScoreWeights` setters accept only numbers from `0.0` to `1.0`.
