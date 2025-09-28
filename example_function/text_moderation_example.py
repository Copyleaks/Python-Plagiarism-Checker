from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationLabel import CopyleaksTextModerationLabel
from copyleaks.models.TextModeration.Requests.CopyleaksTextModerationRequestModel import CopyleaksTextModerationRequestModel
from copyleaks.models.constants.CopyleaksTextModerationConstants import CopyleaksTextModerationConstants
from copyleaks.models.constants.CopyleaksTextModerationLanguages import CopyleaksTextModerationLanguages
from copyleaks.copyleaks import Copyleaks
def run(auth_token, scan_id):
    
    print("Submitting a new text for Text Moderation...")
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
    
    response = Copyleaks.TextModerationClient.submit_text(auth_token, scan_id, model)
    
    print("Text Moderation\n")
    print(response.model_dump_json())
