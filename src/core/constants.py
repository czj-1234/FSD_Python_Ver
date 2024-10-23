import re

EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@university\.com$")
PASSWORD_PATTERN = re.compile(r"^[A-Z][a-zA-Z]{4,}[0-9]{3,}$")
