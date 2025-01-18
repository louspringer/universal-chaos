import os
import re
from collections import defaultdict

def search_ontologies(directory, terms):
    """
    Search through ontology files for relevant terms and return structured results
    """
    # Compile a regex pattern for the search terms
    pattern = re.compile(r'|'.join(terms), re.IGNORECASE)
    
    # Store results in a structured format
    results = defaultdict(list)
    
    # Iterate over all files in the specified directory and subdirectories
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.ttl'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as file:
                        context = []
                        for line_number, line in enumerate(file, start=1):
                            # Store context of surrounding lines
                            context.append(line.strip())
                            if len(context) > 5:  # Keep 5 lines of context
                                context.pop(0)
                                
                            if pattern.search(line):
                                relative_path = os.path.relpath(filepath, directory)
                                match_info = {
                                    'line_number': line_number,
                                    'line': line.strip(),
                                    'context': context.copy(),
                                    'file': relative_path
                                }
                                results[filename].append(match_info)
                except UnicodeDecodeError:
                    print(f"Warning: Could not read {filepath} - encoding issues")

    return results

def print_results(results):
    """Print results in a readable format"""
    if not results:
        print("No matches found in ontology files.")
        return
        
    print("\nSearch Results:")
    print("=" * 80)
    
    for filename, matches in results.items():
        print(f"\nFile: {filename}")
        print("-" * 40)
        
        for match in matches:
            print(f"\nLine {match['line_number']}:")
            print("Context:")
            for ctx_line in match['context']:
                print(f"  {ctx_line}")
            print(f"Match: {match['line']}")
            print("-" * 20)

def main():
    # Define the directory and search terms
    ontology_directory = '../ontology-framework'
    search_terms = [
        'issue', 'task', 'project', 'bug', 'ticket', 
        'tracking', 'workflow', 'status', 'priority',
        'assignee', 'reporter', 'milestone',
        'import', 'version', 'release', 'submodule', 'dependency',
        'validation', 'shape', 'SHACL', 'constraint',
        'path', 'relative', 'absolute'
    ]
    
    print(f"Searching in {ontology_directory} for terms: {', '.join(search_terms)}")
    results = search_ontologies(ontology_directory, search_terms)
    print_results(results)

if __name__ == "__main__":
    main()
