import secrets
import string

CODE_LENGTH = 8

def generate_random_string() -> str:
    """
    Generate a unique string with ascii alphabets and digits
    """
    alphabet = string.ascii_letters + string.digits
    uni_str = "".join(secrets.choice(alphabet) for i in range(CODE_LENGTH))
    return uni_str
