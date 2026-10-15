from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.helpers.copyleaks_multipart import CopyleaksMultipart
from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismResponseModel import CopyleaksImagePlagiarismResponseModel


class _ImagePlagiarismClient:
    @staticmethod
    def check(auth_token, scan_id, submission, timeout=None):
        '''
        Search the web for copies of an image (`CopyleaksImagePlagiarismRequestModel`); `scan_id` is 3 to 36 characters.
        Returns `CopyleaksImagePlagiarismResponseModel`.
        Docs: https://docs.copyleaks.com/reference/actions/image-plagiarism-detector/check
        '''
        assert scan_id and submission

        CopyleaksClientHelper.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v1/image-plagiarism-detector/{scan_id}/check"
        fields = {
            'filename': submission.file_name,
            'sandbox': CopyleaksMultipart.bool_field(submission.sandbox),
        }
        if submission.developer_payload is not None:
            fields['developerPayload'] = submission.developer_payload
        files = {'image': CopyleaksMultipart.file_part(submission.file_name, submission.image)}
        response = CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(auth_token, None),
                                               data=fields, files=files, timeout=timeout)
        return CopyleaksImagePlagiarismResponseModel.model_validate(response.json())
