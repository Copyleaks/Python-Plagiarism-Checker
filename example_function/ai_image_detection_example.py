import base64
from copyleaks.models.ImageDetection.Requests.CopyleaksAiImageDetectionRequestModel import CopyleaksAiImageDetectionRequestModel
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.constants.CopyleaksAiImageDetectionModels import CopyleaksAiImageDetectionModels

def run(auth_token, scan_id):

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
