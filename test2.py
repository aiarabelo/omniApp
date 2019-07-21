import re
url = "https://boards.greenhouse.io/circ/jobs/4357552002"
baseURL = "boards.greenhouse.io"


regex = r"(?:https?:\/\/(?:www\.)?" + baseURL + r"\/)([^/\n?\$]+)"
r = re.search(regex, url)
print(r)
print(r.group(0))
print(r.group(1))