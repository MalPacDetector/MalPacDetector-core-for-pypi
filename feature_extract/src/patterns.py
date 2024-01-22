DOMAIN_PATTERN = r'((?!-)[a-zA-Z0-9-]{1,63}(?<!-)\.)+[a-zA-Z]{2,6}'
IP_PATTERN = r'(\d{1,3}\.){3}\d{1,3}'
BASE64_PATTERN = r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'
SENSITIVE_STRING_PATTERN = r'(\/etc\/shadow)|(\.bashrc)|(\.zshrc)|(\/etc\/hosts)|(\/etc\/passwd)|(\/bin\/sh)'