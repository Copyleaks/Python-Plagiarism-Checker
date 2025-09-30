from copyleaks.models.submit.writing_assistant_document import WritingAssistantDocument
from copyleaks.models.submit.score_weights import ScoreWeights
from copyleaks.copyleaks import Copyleaks

def run(auth_token, scan_id):
    
    print("Submitting a new text for Writing Assistant feedback...")
    sample_text = "Lions are social animals, living in groups called prides, typically consisting of several females, their offspring, and a few males. Female lions are the primary hunters, working together to catch prey. Lions are known for their strength, teamwork, and complex social structures."
    
    score_weight = ScoreWeights()
    score_weight.set_grammar_score_weight(0.2)
    score_weight.set_mechanics_score_weight(0.3)
    score_weight.set_sentence_structure_score_weight(0.5)
    score_weight.set_word_choice_score_weight(0.4)
    
    submission = WritingAssistantDocument(sample_text)
    submission.set_score(score_weight)
    submission.set_sandbox(True)
    
    response = Copyleaks.WritingAssistantClient.submit_text(auth_token, scan_id, submission)
    print(response)
