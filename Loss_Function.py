import json
from typing import Dict, List

def json_schema_validation(json_data: Dict) -> bool:
    # Simulated schema validation for simplicity
    required_keys = {"tool_name", "arguments"}
    return all(key in json_data for key in required_keys)

def tokenize_json(json_data: Dict) -> List[str]:
    # Simulated tokenization for simplicity
    return [str(item) for item in json_data.values()]

def jaccard_similarity(set1: set, set2: set) -> float:
    # Calculate Jaccard similarity
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union != 0 else 0

def structural_loss(json_correct: Dict, json_generated: Dict) -> float:
    # Simulated structural loss for simplicity
    missing_keys = len(set(json_correct.keys()) - set(json_generated.keys()))
    extra_keys = len(set(json_generated.keys()) - set(json_correct.keys()))

    # Simulated argument_value_difference for simplicity
    arg_val_diff = sum(
        json_correct.get("arguments", []) != json_generated.get("arguments", [])
    )

    return missing_keys + extra_keys + arg_val_diff

def sequence_penalty(ref_sequence: List[str], gen_sequence: List[str]) -> float:
    # Simulated sequence penalty for simplicity
    penalty = sum(1 for ref, gen in zip(ref_sequence, gen_sequence) if ref != gen)
    return penalty

# ... (previous definitions of functions)

def total_loss(json_correct: Dict, json_generated: Dict, ref_sequence: List[str]) -> float:
    # Weights for different components of the loss function
    w_missing_keys = 1.0
    w_extra_keys = 1.0
    w_argument_value_difference = 1.0
    w_sequence_penalty = 1.0
    w_jaccard = 1.0

    # Calculate individual error terms
    error_missing_keys = w_missing_keys * (len(set(json_correct.keys()) - set(json_generated.keys())) / len(set(json_correct.keys())))
    error_extra_keys = w_extra_keys * (len(set(json_generated.keys()) - set(json_correct.keys())) / len(set(json_correct.keys())))

    # Check if schema validation is successful before proceeding
    if json_schema_validation(json_correct) and json_schema_validation(json_generated):
        # Convert dictionaries to frozensets before creating sets
        correct_args = frozenset(
            (
                item["argument_name"],
                tuple(item.get("argument_value", []))  # Use get() to handle missing "argument_value"
            )
            for item in json_correct.get("arguments", [])
        )
        generated_args = frozenset(
            (
                item["argument_name"],
                tuple(item.get("argument_value", []))  # Use get() to handle missing "argument_value"
            )
            for item in json_generated.get("arguments", [])
        )

        # Calculate the Jaccard similarity for both tool names and argument names
        tool_name_jaccard = jaccard_similarity(
            set([json_correct.get("tool_name")]),
            set([json_generated.get("tool_name")])
        )
        arg_name_jaccard = jaccard_similarity(
            set(arg_name for arg_name, _ in correct_args),
            set(arg_name for arg_name, _ in generated_args)
        )

        # Use a set for comparison, not a list
        error_argument_value_difference = w_argument_value_difference * (
            (1 - tool_name_jaccard) + (1 - arg_name_jaccard)
        )
    else:
        error_argument_value_difference = 0.0

    error_sequence_penalty = w_sequence_penalty * (
        sequence_penalty(ref_sequence, list(json_generated.keys())) / len(ref_sequence)
    )
    error_jaccard = w_jaccard * (1 - jaccard_similarity(set(json_correct.keys()), set(json_generated.keys())))

    # Calculate total loss
    loss = (
        error_missing_keys
        + error_extra_keys
        + error_argument_value_difference
        + error_sequence_penalty
        + error_jaccard
    )

    return loss

def total_loss_list(json_list_correct: List[Dict], json_list_generated: List[Dict], ref_sequence: List[str]) -> float:
    # Calculate individual losses for each pair of consecutive JSON objects
    individual_losses = [
        total_loss(json_correct, json_generated, ref_sequence)
        for json_correct, json_generated in zip(json_list_correct, json_list_generated)
    ]

    # Combine individual losses into a single value (sum of losses)
    total_loss_value = sum(individual_losses)

    return total_loss_value

# ...

# Example usage
json_list_correct = [
    {"tool_name": "get_sprint_id"},
    {
        "tool_name": "add_work_items_to_sprint",
        "arguments": [
            {"argument_name": "work_ids", "argument_value": "$$PREV[0]"},
            {"argument_name": "sprint_id", "argument_value": "$$PREV[1]"}
        ]
    },
    {
        "tool_name": "create_a_from_text",
        "arguments": [{"argument_name": "text", "argument_value": "T"}]
    }
]

json_list_generated = [
    {"tool_name": "get_sprint_id", "arguments": []},
    {
        "tool_name": "add_work_items_to_sprint",
        "arguments": [
            {"argument_name": "work_ids", "argument_value": "$$PREV[0]"},
            {"argument_name": "sprint_id", "argument_value": "$$PREV[1]"}
        ]
    },
    {
        "tool_name": "create_actionable_tasks_from_text",
        "arguments": [{"argument_name": "text", "argument_value": "T"}]
    }
]

reference_sequence = ["tool_name", "arguments"]

# Calculate and print the total loss for the entire list
total_loss_value = total_loss_list(json_list_correct, json_list_generated, reference_sequence)
print(f"Total Loss for the Entire List: {total_loss_value}")
