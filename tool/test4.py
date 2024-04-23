import re

javascript_code = """
var isAdmin = false;
if (isAdmin) {
    var topLinksTag = document.getElementsByClassName("top-links")[0];
    var adminPanelTag = document.createElement('a');
    adminPanelTag.setAttribute('href', '/administrator');
    adminPanelTag.innerText = 'Admin panel';
    topLinksTag.append(adminPanelTag);
    var pTag = document.createElement('p');
    pTag.innerText = '|';
    topLinksTag.appendChild(pTag);
}
"""

# Define the regular expression pattern to match the href attribute value
pattern = r"setAttribute\('href',\s*'([^']+)'\)"
# pattern = r"href\s*=\s*[\"']([^\"']+)"
# pattern = r"href\s*=\s*[\"']([^\"']+)"

# Find all matches of the pattern in the JavaScript code
matches = re.findall(pattern, javascript_code)

print(matches)

# Print the href attribute values found
for href_value in matches:
    print(href_value)