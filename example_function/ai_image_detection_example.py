import base64
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionRequestModel import CopyleaksAiImageDetectionRequestModel
from copyleaks.copyleaks import Copyleaks

def run(auth_token, scan_id):

    print("Submitting a new image for AI image detection...")
    # Update the path to your image file
    image_path = r"PATH TO IMAGE"
    with open(image_path, 'rb') as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    payload = CopyleaksAiImageDetectionRequestModel(
        base64=base64_image,
        file_name='image2.jpg',
        sandbox=True,
        model='ai-image-1-ultra-01-09-2025'
    )
    
    response = Copyleaks.ImageDetectionClient.submit(auth_token, scan_id, payload)
    print("Image Detection Response:")
    print(response.model_dump_json())
