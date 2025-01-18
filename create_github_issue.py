import os
import json
import requests
from rdflib import Graph, Namespace, RDF, URIRef

# Load the issue content from our TTL file
g = Graph()
g.parse('.issues/ontology-framework/001_submodule_support.ttl', format='turtle')

# Get our namespaces - use the full file path for the namespace
base = URIRef('file:///Users/lou/Documents/universal-chaos/.issues/ontology-framework/#')
ns = Namespace(str(base))

# Debug: Print all triples in the graph
print("All triples in graph:")
for s, p, o in g:
    print(f"{s} {p} {o}")

# Extract issue data - find the Issue object first
issue = URIRef(str(base) + 'issue1')  # Direct reference to the issue
print(f"Found issue: {issue}")

title = str(g.value(subject=issue, predicate=ns.title))
print(f"Found title: {title}")

content = str(g.value(subject=issue, predicate=ns.content))
print(f"Found content: {content}")

labels = [str(l) for l in g.objects(subject=issue, predicate=ns.labels)]
print(f"Found labels: {labels}")

# GitHub API setup
token = os.environ.get('GITHUB_TOKEN')
if not token:
    raise EnvironmentError("GITHUB_TOKEN not found in environment")

headers = {
    'Authorization': f'token {token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Create issue
url = 'https://api.github.com/repos/louspringer/ontology-framework/issues'
data = {
    'title': title,
    'body': content,
    'labels': labels
}

# Debug output
print(f"Sending request to: {url}")
print(f"Headers: {json.dumps(headers, indent=2)}")
print(f"Data: {json.dumps(data, indent=2)}")

response = requests.post(url, headers=headers, json=data)
print(f"Response status: {response.status_code}")
print(f"Response body: {json.dumps(response.json(), indent=2)}")

if response.status_code == 201:
    print(f"Issue created: {response.json().get('html_url')}")
else:
    print(f"Error creating issue: {response.json().get('message')}") 