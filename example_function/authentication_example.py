from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError

def run(email, key):
    
    try:
        auth_token = Copyleaks.login(email, key)
    except CommandError as ce:
        response = ce.get_response()
        print(f"An error occurred (HTTP status code {response.status_code}):")
        print(response.content)
        exit(1)
    
    print("Logged successfully!\nToken:")
    print(auth_token)
    
    return auth_token
