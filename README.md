# Copyleaks SDK
The official [Copyleaks](https://copyleaks.com/) Python library, supporting Python versions: Python 3.6.+

Copyleaks is the integrity layer for your tech stack that helps organizations and individuals understand what's human-made and original, AI-generated, or manipulated across text, image, audio and video.

This SDK gives you access to the following Copyleaks products:

*   AI Text Detection
*   AI Image Detection
*   AI Video Detection
*   Plagiarism Checker (Authenticity scans: file, URL, OCR)
*   Image Plagiarism Detection
*   Grammar Checker
*   Text Moderation
*   Private Cloud Hub repository information

## 🚀 Getting Started
Before you start, ensure you have the following:

*   An active Copyleaks account. If you don’t have one, [Sign up for free](https://copyleaks.com/signup).
*   You can find your API key on the [API Dashboard](https://api.copyleaks.com/dashboard).

Once you have your account and API key:

**Install the SDK**: 

Use the Python Package Manager - PiPy. When integrating this way, you will automatically be able to update the SDK to its latest version:   
```bash
pip install copyleaks
```

## 📚 Documentation
To learn more about how to use Copyleaks API please check out our [Documentation](https://docs.copyleaks.com/resources/sdks/python/). 

## 💡 Usage Examples
Here are some common usage examples for the Copyleaks SDK. You can also see a comprehensive code example in the `example.py` file on our GitHub repository: [example.py](https://github.com/Copyleaks/Python-Plagiarism-Checker/blob/master/example.py).

### Get Authentication Token
This example demonstrates how to log in to the Copyleaks API and obtain an authentication token.

```python
import base64
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError

# --- Your Credentials ---
EMAIL_ADDRESS = 'YOUR_EMAIL_ADDRESS' # Replace with your Copyleaks registered email
KEY = 'YOUR_API_KEY'               # Replace with your Copyleaks API Key
# --------------------

# Log in to the Copyleaks API
auth_token = Copyleaks.login(EMAIL_ADDRESS, KEY)
print("✅ Logged in successfully!")
```
For a detailed understanding of the authentication process, refer to the Copyleaks Login Endpoint [Documentation](https://docs.copyleaks.com/reference/actions/account/login).
##
### Submit Text for Plagiarism Scan
This example shows how to prepare and submit raw text content for a plagiarism scan.

```python
import base64
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.submit.document import FileDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties

# Prepare your content for scanning
# You can scan a URL, a local file, or raw text.
# This example scans a simple string of text.
print("Submitting text for scanning...")
text_to_scan = "Hello world, this is a test."
base64_content = base64.b64encode(text_to_scan.encode()).decode()

# Configure the scan
scan_id = "my-first-scan" 
scan_properties = ScanProperties("https://your-server.com/webhook/{STATUS}") # IMPORTANT: Replace with your actual webhook URL to receive scan results
scan_properties.set_sandbox(True) # Turn on sandbox mode for testing without consuming credits
file_submission = FileDocument(base64_content, "test.txt")
file_submission.set_properties(scan_properties)

# Submit the scan to Copyleaks
Copyleaks.submit_file(auth_token, scan_id, file_submission)
print(f"🚀 Scan submitted successfully! Scan ID: {scan_id}")
print("You will be notified via your webhook when the scan is complete.")
```
For a full guide please refer to our step by step [Guide](https://docs.copyleaks.com/guides/authenticity/detect-plagiarism-text)

For a detailed understanding of the plagiarism detection process, refer to the Copyleaks Submit Endpoint [Documentation](https://docs.copyleaks.com/reference/actions/scans/submit-file)
##
### Reading the AI alert from the completed webhook
When AI Text Detection is enabled for a scan (`aiGeneratedText.detect`), the completed webhook reports AI-generated text as a `suspected-ai-text` alert in `notifications.alerts`. The alert's `additionalData` is a JSON string, which the SDK decodes into a typed `CopyleaksAiTextDetectionResponseModel`.

```python
import logging
from flask import Flask, request
from pydantic import ValidationError
from copyleaks.models.submit.Webhooks.CompletedWebhookModel import CompletedWebhookModel

app = Flask(__name__)

@app.route('/webhook/completed', methods=['POST'])
def webhook_completed():
    completed = CompletedWebhookModel(**request.json)

    # None when the scan produced no AI alert
    ai_alert = completed.get_ai_detection_alert()
    if ai_alert is not None:
        try:
            # None when the alert carries no AI result
            ai_result = ai_alert.get_ai_detection_result()
        except ValidationError:
            # additionalData is not valid JSON; the raw string is in ai_alert.additional_data
            logging.exception("Could not parse the AI alert additional data")
            ai_result = None
        if ai_result is not None and ai_result.summary is not None:
            logging.info(f"AI: {ai_result.summary.ai}, human: {ai_result.summary.human}, model: {ai_result.model_version}")
            for section in ai_result.results:
                logging.info(f"Section classification: {section.classification}")  # 1 = human, 2 = AI

    # Acknowledge the webhook even when the AI alert could not be parsed.
    return '', 200
```
`get_ai_detection_alert()` returns None when the completed webhook contains no suspected-ai-text alert. Sandbox scans send a mock AI alert, which the SDK parses the same way.

Every field of the completed webhook is typed, for example `completed.developer_payload`, `completed.scanned_document.scan_id`, `completed.results.internet[0].url`, `completed.results.internal_ai_data` and `completed.references_validation.summary`. Read-only dict-style access with the JSON keys, such as `completed.results['internet']`, still works. The other webhooks parse the same way: `ErrorWebhookModel`, `CreditsCheckedWebhookModel`, `IndexedWebhookModel`, `NewResultWebhookModel` and `ExportCompletedWebhookModel`.

For the alert format, refer to the Copyleaks scan completed webhook [Documentation](https://docs.copyleaks.com/reference/data-types/authenticity/webhooks/scan-completed)
##
### AI Text Detection
Use the AI detection client to determine if content was generated by artificial intelligence.

```python
import base64
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.submit.ai_detection_document import NaturalLanguageDocument

scan_id = "your-scan-id"

sample_text = "Lions are social animals, living in groups called prides, typically consisting of several females, their offspring, and a few males. Female lions are the primary hunters, working together to catch prey. Lions are known for their strength, teamwork, and complex social structures."
natural_language_submission = NaturalLanguageDocument(sample_text)
natural_language_submission.set_sandbox(True) # Use sandbox for testing
natural_language_submission.set_explain(True) # Optional: AI Logic, returned in response.explain
natural_language_submission.set_sensitivity(2) # Optional: 1 to 3, the server default is 2
response = Copyleaks.AiDetectionClient.submit_natural_language(auth_token, scan_id, natural_language_submission)
print("\nAI Detection (Natural Language):")
print(f"AI: {response.summary.ai}, human: {response.summary.human}, model: {response.model_version}")
for section in response.results:
    print(f"Section classification: {section.classification}")  # 1 = human, 2 = AI
```
`submit_natural_language` returns a `CopyleaksAiTextDetectionResponseModel`; earlier versions returned a dict. Dict-style reads such as `response['summary']['ai']` still work for backward compatibility, but prefer attributes such as `response.summary.ai`. For a plain dict with the JSON keys, use `response.model_dump(by_alias=True, exclude_unset=True)`.

To check the AI Text Detector credit balance (read-only, uses no credits):

```python
balance = Copyleaks.AiDetectionClient.credits_balance(auth_token)
print(f"AI Text Detector credits: {balance.credits}")

# File types that AI Text Detection supports (public, no login needed)
print(Copyleaks.supported_ai_text_detection_file_types().supported_ai_file_types)
```

For a full guide please refer to our step by step [Guide](https://docs.copyleaks.com/guides/ai-detector/ai-text-detection/)

For a detailed understanding of the AI Text Detection process, refer to the Copyleaks detect natural language Endpoint [Documentation](https://docs.copyleaks.com/reference/actions/writer-detector/check/)
##
### Grammar Checker (WritingAssistantClient)
Get intelligent suggestions for improving grammar, spelling, style, and overall writing quality.

```python
import base64
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError
from copyleaks.models.submit.writing_assistant_document import WritingAssistantDocument
from copyleaks.models.submit.score_weights import ScoreWeights

scan_id = "your-scan-id"

# Define the text to be assessed
sample_text = "Lions are social animals, living in groups called prides, typically consisting of several females, their offspring, and a few males. Female lions are the primary hunters, working together to catch prey. Lions are known for their strength, teamwork, and complex social structures."

# Configure score weights for different aspects of writing quality
score_weight = ScoreWeights()
score_weight.set_grammar_score_weight(0.2)
score_weight.set_mechanics_score_weight(0.3)
score_weight.set_sentence_structure_score_weight(0.5)
score_weight.set_word_choice_score_weight(0.4)

submission = WritingAssistantDocument(sample_text)
submission.set_score(score_weight)
submission.set_sandbox(True) # Use sandbox for testing

response = Copyleaks.WritingAssistantClient.submit_text(auth_token, scan_id, submission)
print("\nWriting Assistant Feedback:")
print(f"Overall score: {response.score.corrections.overall_score}")
print(f"Readability: {response.score.readability.readability_level_text}")
chars = response.corrections.text.chars
for correction_type, start, length, replacement in zip(chars.types, chars.starts, chars.lengths, chars.operation_texts):
    print(f"Type {correction_type}: replace text[{start}:{start + length}] with '{replacement}'")
```
`submit_text` returns a `CopyleaksWritingAssistantResponseModel`; earlier versions returned a dict. Dict-style reads such as `response['score']['corrections']['overallScore']` still work for backward compatibility, but prefer attributes such as `response.score.corrections.overall_score`. For a plain dict with the JSON keys, use `response.model_dump(by_alias=True, exclude_unset=True)`.

For a full guide please refer to our step by step [Guide](https://docs.copyleaks.com/guides/writing/check-grammar/)

For a detailed understanding of the Grammar Checker (WritingAssistantClient) process, refer to the Copyleaks writing feedback Endpoint [Documentation](https://docs.copyleaks.com/reference/actions/writing-assistant/check/)
##
### Text Moderation
Scan and moderate text content for unsafe, inappropriate, or policy-violating material across various categories.

```python
import base64
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationRequestModel import CopyleaksTextModerationRequestModel
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationLabel import CopyleaksTextModerationLabel
from copyleaks.models.constants.CopyleaksTextModerationConstants import CopyleaksTextModerationConstants
from copyleaks.models.constants.CopyleaksTextModerationLanguages import CopyleaksTextModerationLanguages

scan_id = "your-scan-id"

labelsArray=[
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.ADULT_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.TOXIC_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.VIOLENT_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.PROFANITY_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.SELF_HARM_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.HARASSMENT_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.HATE_SPEECH_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.DRUGS_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.FIREARMS_V1),
        CopyleaksTextModerationLabel(id=CopyleaksTextModerationConstants.CYBERSECURITY_V1),
    ]

model = CopyleaksTextModerationRequestModel(
    text="This is some text to scan.",
    sandbox=True,
    language=CopyleaksTextModerationLanguages.ENGLISH,
    labels=labelsArray
)

textModerationResponse = Copyleaks.TextModerationClient.submit_text(auth_token, scan_id, model)
print("\nText Moderation:")
print(textModerationResponse.model_dump_json())
```
`labels` is required and holds 1 to 16 labels.
For a full guide please refer to our step by step [Guide](https://docs.copyleaks.com/guides/moderation/moderate-text/)

For a detailed understanding of the Text moderation process, refer to the Copyleaks text moderation Endpoint [Documentation](https://docs.copyleaks.com/reference/actions/text-moderation/check/)
##
### AI Image Detection
Determine if a given image was generated or partially generated by an AI.

```python
import base64
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionRequestModel import CopyleaksAiImageDetectionRequestModel
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.constants.CopyleaksAiImageDetectionModels import CopyleaksAiImageDetectionModels

scan_id = "your-scan-id"
print("Submitting a new image for AI image detection...")

# Update the path to your image file
image_path = r"PATH TO IMAGE"

with open(image_path, 'rb') as image_file:
    base64_image = base64.b64encode(image_file.read()).decode('utf-8')

payload = CopyleaksAiImageDetectionRequestModel(
    base64=base64_image,
    file_name='my-image.png',
    sandbox=True,
    model=CopyleaksAiImageDetectionModels.AI_IMAGE_1_ULTRA
)
response = Copyleaks.ImageDetectionClient.submit(auth_token, scan_id, payload)

print("Image Detection Response:")
print(response.model_dump_json())


```
To upload the image file directly (multipart, no base64; recommended for large images), ask for a heatmap mask, and locate objects in the image:

```python
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionFileRequestModel import CopyleaksAiImageDetectionFileRequestModel
from copyleaks.models.constants.CopyleaksAiImageMaskTypes import CopyleaksAiImageMaskTypes

with open(image_path, 'rb') as image_file:
    request = CopyleaksAiImageDetectionFileRequestModel(
        image=image_file,
        file_name='my-image.png',
        model=CopyleaksAiImageDetectionModels.AI_IMAGE_1_ULTRA,
        sandbox=True,
        mask_type=CopyleaksAiImageMaskTypes.HEATMAP,  # "binary" (default), "heatmap" or "none"
        object_detection=['face', 'hand']              # optional, up to 3 objects
    )
    response = Copyleaks.ImageDetectionClient.submit_file(auth_token, scan_id, request)

print(f"AI detected: {response.is_ai_detected}, AI: {response.summary.ai}")
for detected in response.detected_objects or []:
    print(f"Found {detected.object}: {len(detected.mask.starts)} mask segments")
```
`mask_type` and `object_detection` work with the base64 `CopyleaksAiImageDetectionRequestModel` too. With the "none" mask type, `response.result` is None.

#### Asynchronous AI Image Detection (image URL and webhook)
```python
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionAsyncRequestModel import CopyleaksAiImageDetectionAsyncRequestModel

request = CopyleaksAiImageDetectionAsyncRequestModel(
    url='https://example.com/image1.png',
    file_name='image1.png',
    model=CopyleaksAiImageDetectionModels.AI_IMAGE_1_ULTRA,
    webhooks={'url': 'https://your-server.com/webhook/ai-image'},
    sandbox=True
)
Copyleaks.ImageDetectionClient.submit_async(auth_token, scan_id, request)
```
The result is posted to your webhook. Parse it with `CopyleaksAiImageDetectionResponseModel(**request.json)` (from `copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResponseModel`).

For a full guide please refer to our step by step [Guide](https://docs.copyleaks.com/guides/ai-detector/ai-image-detection/)

For a detailed understanding of the AI Image Detection process, refer to the Copyleaks image detection Endpoint [Documentation](https://docs.copyleaks.com/reference/actions/ai-image-detector/check/)
##
### AI Video Detection
Submit a video URL. The result is posted to your webhook when processing is complete.

```python
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.VideoDetection.Requests.CopyleaksAiVideoDetectionRequestModel import CopyleaksAiVideoDetectionRequestModel
from copyleaks.models.constants.CopyleaksAiVideoDetectionModels import CopyleaksAiVideoDetectionModels

request = CopyleaksAiVideoDetectionRequestModel(
    url='https://example.com/my-video.mp4',
    file_name='my-video.mp4',
    model=CopyleaksAiVideoDetectionModels.AI_VIDEO_1_PRO,
    webhooks={'url': 'https://your-server.com/webhook/ai-video'},
    sandbox=True  # free mock results for testing
)
Copyleaks.VideoDetectionClient.submit(auth_token, "my-video-scan-1", request)
```
In your webhook handler, parse the result:

```python
from copyleaks.models.VideoDetection.Responses.CopyleaksAiVideoDetectionResponseModel import CopyleaksAiVideoDetectionResponseModel

result = CopyleaksAiVideoDetectionResponseModel(**request.json)
print(f"AI detected: {result.is_ai_detected}, overall AI ratio: {result.summary.overall_ai_ratio}")
```
For more details, refer to the AI Video Detection [Documentation](https://docs.copyleaks.com/reference/actions/ai-video-detector/submit)
##
### Image Plagiarism Detection
Search the web for copies of an image, in one synchronous call. The image file is uploaded as multipart/form-data.

```python
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.ImagePlagiarism.Requests.CopyleaksImagePlagiarismRequestModel import CopyleaksImagePlagiarismRequestModel

with open('my-photo.jpg', 'rb') as image_file:
    request = CopyleaksImagePlagiarismRequestModel(image=image_file, file_name='my-photo.jpg', sandbox=True)
    response = Copyleaks.ImagePlagiarismClient.check(auth_token, "my-image-scan-1", request)

score = response.matches.score
print(f"Total: {score.total_matches}, full: {score.full_matches}, partial: {score.partial_matches}")
for match in response.matches.internet:
    print(match.url, match.match_type, [page.url for page in match.web_pages])  # match_type 0 = full, 1 = partial
```
For more details, refer to the Image Plagiarism Detection [Documentation](https://docs.copyleaks.com/reference/actions/image-plagiarism-detector/check)
##
### More scan options
Plagiarism scans accept more options on `ScanProperties`, for example:

```python
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.submit.properties.ai_generated_text import AIGeneratedText
from copyleaks.models.submit.properties.ai_generated_text_explain import AIGeneratedTextExplain
from copyleaks.models.submit.properties.cross_languages import CrossLanguages
from copyleaks.models.submit.properties.internal_ai_source_match import InternalAISourceMatch
from copyleaks.models.submit.properties.language import Language
from copyleaks.models.submit.properties.overview import Overview
from copyleaks.models.submit.properties.references import References
from copyleaks.models.submit.properties.scanning import Scanning
from copyleaks.models.submit.properties.sensitive_data_protection import SensitiveDataProtection
from copyleaks.models.submit.properties.writing_feedback import WritingFeedback

# AI detection with AI Logic
explain = AIGeneratedTextExplain()
explain.set_enable(True)
ai_text = AIGeneratedText()
ai_text.set_detect(True)
ai_text.set_sensitivity(2)
ai_text.set_explain(explain)
scan_properties.set_ai_generated_text(ai_text)

# Grammar Checker, Gen-AI Overview and Citation Checker in the same scan
writing_feedback = WritingFeedback()
writing_feedback.set_enable(True)
scan_properties.set_writing_feedback(writing_feedback)
overview = Overview()
overview.set_enable(True)
scan_properties.set_overview(overview)
references = References()
references.set_validate(True)
scan_properties.set_references(references)

# Match against the Copyleaks internal AI database
internal_ai = InternalAISourceMatch()
internal_ai.set_enable(True)
scan_properties.set_internal_ai_source_match(internal_ai)

# Mask email addresses and phone numbers in the scanned document
sensitive_data = SensitiveDataProtection()
sensitive_data.set_email_address(True)
sensitive_data.set_phone_number(True)
scan_properties.set_sensitive_data_protection(sensitive_data)

# Cross-language plagiarism: list the supported languages, then pick some
languages = Copyleaks.allowed_cross_languages()  # public, no login needed
print(languages.result_language_codes)            # for example ['sq', 'bg', ...]; result_languages maps names to codes
french = Language()
french.set_code('fr')
cross_languages = CrossLanguages()
cross_languages.set_languages([french])
scanning = Scanning()
scanning.set_cross_languages(cross_languages)
scan_properties.set_scanning(scanning)

scan_properties.set_scan_time_zone('America/New_York')
```
Other options include `set_course`, `set_assignment` and `set_institution`, `Scanning.set_include` (`ScanningInclude`), `ScanningExclude.set_backlinks_domains` and `set_text`, `Indexing.set_copyleaks_db`, and the `ai_detection` and `writing_feedback` PDF colors. To export the AI detection, Grammar Checker or Overview report of a scan, use `Export.set_ai_detection`, `set_writing_feedback` and `set_overview`. URL scans accept `UrlDocument.set_verb` and `set_headers`.

See the scan properties [Documentation](https://docs.copyleaks.com/reference/actions/authenticity/submit-file)
##
### Private Cloud Hub repository information
```python
info = Copyleaks.repository_info(auth_token, "my-repository-id")
print(info.name, info.status, info.current_credits, info.max_credits)
```
Requires the "Super Admin" or "Admin" role on the repository. For more details, refer to the [Documentation](https://docs.copyleaks.com/reference/actions/private-cloud-hub/info)
##
### Timeouts, connections and errors
Every call goes through one shared `requests.Session`, so connections are kept alive and reused. Every call has a timeout: by default 10 seconds to connect and 180 seconds to read the response.

```python
import requests
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError
from copyleaks.exceptions.rate_limit_error import RateLimitError
from copyleaks.exceptions.under_maintenance_error import UnderMaintenanceError

Copyleaks.set_timeout((5, 60))  # (connect, read) seconds for every call; None turns the timeout off
response = Copyleaks.AiDetectionClient.submit_natural_language(auth_token, scan_id, natural_language_submission, timeout=300)  # one call

# Optional: your own session, for example with proxies
session = requests.Session()
session.proxies = {'https': 'http://proxy.example.com:8080'}
Copyleaks.set_session(session)

try:
    Copyleaks.credits_balance(auth_token)
except RateLimitError as e:          # HTTP 429
    print(f"Too many requests, retry in {e.retry_after} seconds")
except UnderMaintenanceError:        # HTTP 503
    print("Copyleaks is under maintenance, retry later")
except CommandError as e:            # any other error status
    print(e.get_response().status_code, e.get_response().text)
```
The SDK writes nothing to stdout. Failed calls are logged at DEBUG level on the `copyleaks` logger.
##
### Further Resources

*   **Copyleaks API Dashboard:** Manage your API keys, monitor usage, and view analytics from your personalized dashboard. [Access Dashboard](https://api.copyleaks.com/dashboard)
*   **Copyleaks SDK Documentation:** Explore comprehensive guides, API references, and code examples for seamless integration. [Read Documentation](https://docs.copyleaks.com/resources/sdks/overview/)

##
### Support
* If you need assistance, please contact Copyleaks Support via our support portal: Contact Copyleaks [Support](https://help.copyleaks.com/s/contactsupport).
* To arrange a product demonstration, book a demo here: [Booking Link](https://copyleaks.com/book-a-demo).
