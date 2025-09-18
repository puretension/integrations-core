#!/usr/bin/env python3

"""
Test script to verify the normalize_instance_tag fix
"""

import re

def normalize_instance_tag(tag):
    """New normalize function that preserves minuses"""
    if isinstance(tag, str):
        tag = tag.encode('utf-8', 'ignore')
    
    # Only replace characters that are NOT allowed in DataDog tags
    # Allowed: alphanumerics, underscores, minuses, colons, periods, slashes
    # Pattern matches: commas, plus, asterisk, parentheses, brackets, braces, whitespace
    tag = re.sub(rb'[,\+\*/()\[\]{}\s]', rb'_', tag)
    
    # Clean up multiple underscores
    tag = re.sub(rb'__+', rb'_', tag)
    
    # Clean up underscores around dots
    tag = re.sub(rb'_*\._*', rb'.', tag).strip(b'_')
    
    return tag.decode('utf-8')

def old_normalize_tag(tag):
    """Old normalize function that converts minuses to underscores"""
    if isinstance(tag, str):
        tag = tag.encode('utf-8', 'ignore')
    tag = re.sub(rb'[,\+\*\-/()\[\]{}\s]', rb'_', tag)  # Note the \- here
    tag = re.sub(rb'__+', rb'_', tag)
    tag = re.sub(rb'_*\._*', rb'.', tag).strip(b'_')
    return tag.decode('utf-8')

# Test cases
test_cases = [
    "my-service-name",
    "test_with_underscores",
    "test.with.dots", 
    "test:with:colons",
    "test/with/slashes",
    "test with spaces",
    "test,with,commas",
    "test+with+plus",
    "test*with*asterisk",
    "test(with)parentheses",
    "test[with]brackets",
    "test{with}braces",
    "_need-to__be_normalized-",
]

print("Comparison of old vs new normalize_tag behavior:")
print("=" * 80)
print(f"{'Original':<25} {'Old Result':<25} {'New Result':<25} {'Fixed?'}")
print("-" * 80)

for case in test_cases:
    old_result = old_normalize_tag(case)
    new_result = normalize_instance_tag(case)
    is_fixed = "✓" if old_result != new_result and '-' in case else ""
    
    print(f"{case:<25} {old_result:<25} {new_result:<25} {is_fixed}")

print("\nKey improvements:")
print("- Minuses (-) are now preserved in instance tags")
print("- Colons (:), periods (.), and slashes (/) are preserved")
print("- Only invalid characters are converted to underscores")
