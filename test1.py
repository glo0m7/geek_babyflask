import re
username = '<>'
username = re.search(r'<(\w+)>', username).group(1) if re.search(r'<(\w+)>', username) is not None else username
print(username)