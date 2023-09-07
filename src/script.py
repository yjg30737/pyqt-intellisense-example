import json
import os.path

def get_suggestions(line):
    builtin_functions_weights = dict()
    weights_filename = 'weights.json'
    # load the data
    if os.path.exists(weights_filename):
        with open(weights_filename, 'r') as f:
            builtin_functions_weights = json.load(f)
    else:
        # save the data
        with open(weights_filename, 'w') as f:
            builtin_functions_weights = {func: 1 for func in ['abs', 'len', 'open', 'print', 'range', 'length', 'type']}
            json.dump(builtin_functions_weights, f)

    suggestions = []

    # Loop through all built-in functions
    suggestions_not_include = []
    for func, weight in builtin_functions_weights.items():
        if func.startswith(line):
            suggestions.append((func, weight))
        else:
            suggestions_not_include.extend(line.split())
            suggestions_not_include.append(line)

    builtin_functions_weights.update({ func: 1 for func in suggestions_not_include })

    # Sort by weight
    suggestions.sort(key=lambda x: x[1], reverse=True)
    sorted_suggestions = [s[0] for s in suggestions]

    # Update weight based on new input (example)
    if line in builtin_functions_weights:
        builtin_functions_weights[line] += 1

    # save the data
    with open(weights_filename, 'w') as f:
        json.dump(builtin_functions_weights, f)

    return sorted_suggestions


def run_suggestion(query):
    # Get auto-completion suggestions based on the input line
    suggestions = get_suggestions(query)
    responses = 'Suggestions: '
    if len(suggestions) > 0:
        responses += ", ".join(suggestions)
    else:
        responses += 'Nothing! Sorry.'
    return responses

