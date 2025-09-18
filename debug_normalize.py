#!/usr/bin/env python3

import re

# Reproduce the normalize_tag logic from base.py (exact copy)
TAG_REPLACEMENT = re.compile(rb'[,\+\*\-/()\[\]{}\s]')
MULTIPLE_UNDERSCORE_CLEANUP = re.compile(rb'__+')
DOT_UNDERSCORE_CLEANUP = re.compile(rb'_*\._*')

def normalize_tag(tag):
    """Reproduce the normalize_tag function"""
    if isinstance(tag, str):
        tag = tag.encode('utf-8', 'ignore')
    tag = TAG_REPLACEMENT.sub(rb'_', tag)
    tag = MULTIPLE_UNDERSCORE_CLEANUP.sub(rb'_', tag)
    tag = DOT_UNDERSCORE_CLEANUP.sub(rb'.', tag).strip(b'_')
    return tag.decode('utf-8')

# Test the problematic case
test_name = "_need-to__be_normalized-"
result = normalize_tag(test_name)

print(f"Original: '{test_name}'")
print(f"Normalized: '{result}'")
print(f"Expected: 'need_to_be_normalized'")
print(f"Match: {result == 'need_to_be_normalized'}")

# Test other cases
test_cases = [
    "test-with-dashes",
    "test_with_underscores", 
    "test.with.dots",
    "test with spaces",
    "test,with,commas",
    "test+with+plus",
    "test*with*asterisk",
    "test/with/slash",
    "test(with)parentheses",
    "test[with]brackets",
    "test{with}braces"
]

print("\nOther test cases:")
print("=" * 50)
for case in test_cases:
    normalized = normalize_tag(case)
    print(f"'{case}' -> '{normalized}'")
