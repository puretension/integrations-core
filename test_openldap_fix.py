#!/usr/bin/env python3
"""
Simple test to verify OpenLDAP search_scope fix logic
"""

# Mock ldap3 constants
class MockLDAP3:
    BASE = 0
    LEVEL = 1
    SUBTREE = 2

ldap3 = MockLDAP3()

def convert_search_scope(search_scope_str):
    """Convert string to ldap3 constant - our fix logic"""
    if search_scope_str.lower() == "base":
        return ldap3.BASE
    elif search_scope_str.lower() == "level":
        return ldap3.LEVEL
    else:  # default to subtree
        return ldap3.SUBTREE

# Test cases
test_cases = [
    ("base", ldap3.BASE),
    ("level", ldap3.LEVEL), 
    ("subtree", ldap3.SUBTREE),
    ("SUBTREE", ldap3.SUBTREE),  # case insensitive
    ("invalid", ldap3.SUBTREE),  # default
    ("", ldap3.SUBTREE),  # empty string
]

print("Testing search_scope conversion logic:")
print("=" * 40)

all_passed = True
for input_val, expected in test_cases:
    result = convert_search_scope(input_val)
    status = "✅ PASS" if result == expected else "❌ FAIL"
    print(f"{status} '{input_val}' -> {result} (expected {expected})")
    if result != expected:
        all_passed = False

print("=" * 40)
print(f"Overall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")
