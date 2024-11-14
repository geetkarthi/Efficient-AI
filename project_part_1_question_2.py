# -*- coding: utf-8 -*-
"""Project part 1 - question 2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ed0vlhW0UsMymgoaiGBKKEogxT7j0VS_
"""

import math
from collections import Counter

data = [
    ['Sunny', 'Sunny', 'Overcast', 'Rain', 'Rain', 'Rain', 'Overcast', 'Sunny', 'Sunny', 'Rain', 'Sunny', 'Overcast', 'Overcast', 'Rain'],
    ['Hot', 'Hot', 'Hot', 'Mild', 'Cool', 'Cool', 'Cool', 'Mild', 'Cool', 'Mild', 'Mild', 'Mild', 'Hot', 'Mild'],
    ['High', 'High', 'High', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'Normal', 'Normal', 'High', 'Normal', 'High'],
    ['Weak', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Weak', 'Weak', 'Strong', 'Strong', 'Weak', 'Strong'],
    ['No', 'No', 'Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'No']
]

data = [list(row) for row in zip(*data)]

def entropy(class_counts):
    total = sum(class_counts)
    ent = 0
    for count in class_counts:
        if count == 0:
            continue
        probability = count / total
        ent -= probability * math.log2(probability)
    return ent

def information_gain(parent_counts, subsets):
    # Parent entropy
    parent_entropy = entropy(parent_counts)

    # Weighted entropy for each subset
    total_samples = sum(parent_counts)
    weighted_entropy = 0
    for subset in subsets:
        subset_entropy = entropy(subset)
        weight = sum(subset) / total_samples
        weighted_entropy += weight * subset_entropy

    # Information gain
    gain = parent_entropy - weighted_entropy
    return gain

# Function to calculate subsets based on a feature split
def split_data(data, feature_col, target_col):
    split = {}
    for row in data:
        feature_value = row[feature_col]
        target_value = row[target_col]

        if feature_value not in split:
            split[feature_value] = []
        split[feature_value].append(target_value)

    # Convert target values to counts for information gain calculation
    subsets = [list(Counter(values).values()) for values in split.values()]
    return subsets, split

# Find the best feature to split
def best_feature_to_split(data, target_col):
    num_features = len(data[0]) - 1
    target_counts = list(Counter(row[target_col] for row in data).values())

    best_gain = -1
    best_feature = None

    for feature_col in range(num_features):
        subsets, _ = split_data(data, feature_col, target_col)
        gain = information_gain(target_counts, subsets)

        if gain > best_gain:
            best_gain = gain
            best_feature = feature_col

    return best_feature

# Recursive function to build the decision tree
def build_tree(data, target_col, depth=0):
    # Check if all examples have the same class
    target_values = [row[target_col] for row in data]
    if len(set(target_values)) == 1:
        return target_values[0]  # Return the class as a leaf node

    # If no features left to split or maximum depth reached, return the majority class
    if len(data[0]) == 1:
        return Counter(target_values).most_common(1)[0][0]

    # Choose the best feature to split
    best_feature = best_feature_to_split(data, target_col)

    if best_feature is None:
        return Counter(target_values).most_common(1)[0][0]

    # Create the subtree
    tree = {f"Feature{best_feature + 1}": {}}

    # Split data by the best feature and build subtrees recursively
    _, split = split_data(data, best_feature, target_col)
    for feature_value, subset_targets in split.items():
        # Create a new subset including only relevant rows and columns
        subset = [
            [value for i, value in enumerate(row) if i != best_feature] + [target]
            for row, target in zip(data, target_values)
            if row[best_feature] == feature_value
        ]

        # Recursively build the subtree
        subtree = build_tree(subset, target_col, depth + 1)
        tree[f"Feature{best_feature + 1}"][feature_value] = subtree

    return tree

# Target column index
target_col = 4

# Build the decision tree
decision_tree = build_tree(data, target_col)
print("Decision Tree:", decision_tree)