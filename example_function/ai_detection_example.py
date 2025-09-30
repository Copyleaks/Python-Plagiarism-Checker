from copyleaks.models.submit.ai_detection_document import NaturalLanguageDocument
from copyleaks.copyleaks import Copyleaks

def run(auth_token, scan_id):

    print("Submitting a new text for AI detection...")
    sample_text = "Lions are social animals, living in groups called prides, typically consisting of several females, their offspring, and a few males. Female lions are the primary hunters, working together to catch prey. Lions are known for their strength, teamwork, and complex social structures."
    
    natural_language_submission = NaturalLanguageDocument(sample_text)
    natural_language_submission.set_sandbox(True)
    
    response = Copyleaks.AiDetectionClient.submit_natural_language(auth_token, scan_id, natural_language_submission)
    print(response)
