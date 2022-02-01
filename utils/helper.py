import bleach
import re

from rest_framework import status

from .error_handler import *


class Helper:
    """
    This is a helper class for the project and contains so vital functions and 
    repetitive task so that the code base will follow DRY principle
    """
    def clean_username(name):
        """
        The first methods cleans the username by escaping html tags (prevents XSS attacks)
        and checks for special characters
        """
        if not name:
            raise ValueError("Username is required")
        name = bleach.clean(name)
        bad_char = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
        if not bad_char.search(name):
            return re.sub(r'\s+', '', name)
        else:
            raise ValueError("This username contains forbidden characters!")

    def get_status_code(code):
        status_text = {
            200: status.HTTP_200_OK,
            201: status.HTTP_201_CREATED,
            204: status.HTTP_204_NO_CONTENT,
            202: status.HTTP_202_ACCEPTED,
            400: status.HTTP_400_BAD_REQUEST,
            401: status.HTTP_401_UNAUTHORIZED,
            403: status.HTTP_403_FORBIDDEN,
            422: status.HTTP_422_UNPROCESSABLE_ENTITY,
            404: status.HTTP_404_NOT_FOUND
        }
        status_code = status_text.get(code) or status.HTTP_400_BAD_REQUEST
        return status_code
