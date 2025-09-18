#!/usr/bin/env python3

"""
Test script to reproduce the normalize_tag issue in http_check
Issue #21103: The normalization of the instance tag on the http_check is done incorrectly
"""

import sys
import os

# Add the datadog_checks_base to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'datadog_checks_base'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'http_check'))

from datadog_checks.http_check import HTTPCheck

def test_normalize_tag_issue():
    """Test to reproduce the normalize_tag issue"""
    
    # Create a mock instance
    init_config = {}
    instances = [
        {
            'name': 'test-instance-with-dashes',
            'url': 'http://example.com'
        },
        {
            'name': 'test_instance_with_underscores', 
            'url': 'http://example.com'
        },
        {
            'name': 'test.instance.with.dots',
            'url': 'http://example.com'
        },
        {
            'name': 'test instance with spaces',
            'url': 'http://example.com'
        }
    ]
    
    check = HTTPCheck('http_check', init_config, instances)
    
    print("Testing normalize_tag behavior:")
    print("=" * 50)
    
    for instance in instances:
        original_name = instance['name']
        normalized_name = check.normalize_tag(original_name)
        print(f"Original: '{original_name}' -> Normalized: '{normalized_name}'")
        
        # Show what the instance tag would look like
        instance_tag = f"instance:{normalized_name}"
        print(f"Instance tag: {instance_tag}")
        print("-" * 30)

if __name__ == "__main__":
    test_normalize_tag_issue()
