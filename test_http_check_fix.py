#!/usr/bin/env python3

"""
Comprehensive test for the http_check normalize_instance_tag fix
"""

import re

def normalize_instance_tag(tag):
    """New normalize function that preserves minuses and other valid characters"""
    if isinstance(tag, str):
        tag = tag.encode('utf-8', 'ignore')
    
    # Only replace characters that are NOT allowed in DataDog tags
    # Allowed: alphanumerics, underscores, minuses, colons, periods, slashes
    # Pattern matches: commas, plus, asterisk, parentheses, brackets, braces, whitespace
    # Note: We exclude / from replacement since it's allowed in DataDog tags
    tag = re.sub(rb'[,\+\*()\[\]{}\s]', rb'_', tag)
    
    # Clean up multiple underscores
    tag = re.sub(rb'__+', rb'_', tag)
    
    # Clean up underscores around dots
    tag = re.sub(rb'_*\._*', rb'.', tag).strip(b'_')
    
    return tag.decode('utf-8')

def test_datadog_tag_compliance():
    """Test that the new function follows DataDog tag rules"""
    
    # Test cases based on DataDog documentation:
    # "May contain alphanumerics, underscores, minuses, colons, periods, and slashes"
    
    valid_chars_tests = [
        ("my-service", "my-service"),  # minuses should be preserved
        ("my_service", "my_service"),  # underscores should be preserved  
        ("my:service", "my:service"),  # colons should be preserved
        ("my.service", "my.service"),  # periods should be preserved
        ("my/service", "my/service"),  # slashes should be preserved
        ("MyService123", "MyService123"),  # alphanumerics should be preserved
    ]
    
    invalid_chars_tests = [
        ("my,service", "my_service"),  # commas should be converted
        ("my+service", "my_service"),  # plus should be converted
        ("my*service", "my_service"),  # asterisk should be converted
        ("my service", "my_service"),  # spaces should be converted
        ("my(service)", "my_service"),  # parentheses should be converted
        ("my[service]", "my_service"),  # brackets should be converted
        ("my{service}", "my_service"),  # braces should be converted
    ]
    
    edge_cases = [
        ("_need-to__be_normalized-", "need-to_be_normalized-"),  # Original test case
        ("--multiple--dashes--", "--multiple--dashes--"),  # Multiple dashes preserved
        ("__multiple__underscores__", "multiple_underscores"),  # Multiple underscores cleaned
        ("service.v1.2", "service.v1.2"),  # Version-like naming preserved
        ("api/v1/users", "api/v1/users"),  # API path-like naming preserved
        ("db:primary", "db:primary"),  # Database role naming preserved
    ]
    
    print("Testing DataDog tag compliance:")
    print("=" * 60)
    
    all_passed = True
    
    for test_cases, category in [
        (valid_chars_tests, "Valid characters (should be preserved)"),
        (invalid_chars_tests, "Invalid characters (should be converted)"),
        (edge_cases, "Edge cases")
    ]:
        print(f"\n{category}:")
        print("-" * 40)
        
        for input_val, expected in test_cases:
            result = normalize_instance_tag(input_val)
            passed = result == expected
            status = "✓ PASS" if passed else "✗ FAIL"
            
            print(f"{input_val:<25} -> {result:<25} {status}")
            if not passed:
                print(f"  Expected: {expected}")
                all_passed = False
    
    print(f"\nOverall result: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    return all_passed

if __name__ == "__main__":
    test_datadog_tag_compliance()
