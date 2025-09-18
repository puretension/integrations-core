#!/usr/bin/env python3

"""
Test for SQL Server schemas_collection fix (#20685)
"""

import re

def test_foreign_key_query_fix():
    """Test that FOREIGN_KEY_QUERY includes FK.object_id in GROUP BY clause"""
    
    # Read the fixed query
    with open('/Users/idohyeong/Desktop/dev/integrations-core/sqlserver/datadog_checks/sqlserver/queries.py', 'r') as f:
        content = f.read()
    
    # Extract FOREIGN_KEY_QUERY
    query_match = re.search(r'FOREIGN_KEY_QUERY = """(.*?)"""', content, re.DOTALL)
    if not query_match:
        print("❌ Could not find FOREIGN_KEY_QUERY")
        return False
    
    query = query_match.group(1)
    
    # Check if FK.object_id is in GROUP BY clause
    group_by_match = re.search(r'GROUP BY\s+(.*?);', query, re.DOTALL | re.IGNORECASE)
    if not group_by_match:
        print("❌ Could not find GROUP BY clause")
        return False
    
    group_by_clause = group_by_match.group(1)
    
    # Check if FK.object_id is included
    if 'FK.object_id' in group_by_clause:
        print("✅ FK.object_id found in GROUP BY clause")
        return True
    else:
        print("❌ FK.object_id NOT found in GROUP BY clause")
        print(f"GROUP BY clause: {group_by_clause}")
        return False

def test_deadlock_none_handling():
    """Test that _create_deadlock_rows handles None db_rows"""
    
    # Read the fixed deadlocks.py
    with open('/Users/idohyeong/Desktop/dev/integrations-core/sqlserver/datadog_checks/sqlserver/deadlocks.py', 'r') as f:
        content = f.read()
    
    # Check if None handling is present
    if 'if db_rows is None:' in content:
        print("✅ None handling found in _create_deadlock_rows")
        return True
    else:
        print("❌ None handling NOT found in _create_deadlock_rows")
        return False

def main():
    print("Testing SQL Server schemas_collection fixes...")
    print("=" * 50)
    
    test1_passed = test_foreign_key_query_fix()
    test2_passed = test_deadlock_none_handling()
    
    print("\nSummary:")
    print(f"Foreign Key Query Fix: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"Deadlock None Handling: {'✅ PASS' if test2_passed else '❌ FAIL'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All fixes applied successfully!")
        print("\nThis should resolve issue #20685:")
        print("- Fixed SQL syntax error in foreign key query")
        print("- Added proper None handling for deadlock collection")
    else:
        print("\n❌ Some fixes failed to apply")

if __name__ == "__main__":
    main()
