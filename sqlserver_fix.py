# Fix for #20685: SQL checks fail when schemas_collection is enabled

# 1. Fix FOREIGN_KEY_QUERY in queries.py
FOREIGN_KEY_QUERY_FIXED = """
SELECT
    FK.parent_object_id AS table_id,
    FK.name AS foreign_key_name,
    OBJECT_NAME(FK.parent_object_id) AS referencing_table,
    STRING_AGG(COL_NAME(FKC.parent_object_id, FKC.parent_column_id),',') AS referencing_column,
    OBJECT_NAME(FK.referenced_object_id) AS referenced_table,
    STRING_AGG(COL_NAME(FKC.referenced_object_id, FKC.referenced_column_id),',') AS referenced_column,
    FK.delete_referential_action_desc AS delete_action,
    FK.update_referential_action_desc AS update_action
FROM
    sys.foreign_keys AS FK
    JOIN sys.foreign_key_columns AS FKC ON FK.object_id = FKC.constraint_object_id
WHERE
    FK.parent_object_id IN ({})
GROUP BY
    FK.object_id,  -- ADD THIS LINE - this was missing!
    FK.name,
    FK.parent_object_id,
    FK.referenced_object_id,
    FK.delete_referential_action_desc,
    FK.update_referential_action_desc;
"""

# 2. Fix _create_deadlock_rows in deadlocks.py
def _create_deadlock_rows_fixed(self):
    db_rows = self._query_deadlocks()
    
    # FIX: Handle case where db_rows is None
    if db_rows is None:
        self._log.debug("No deadlock data returned from query")
        return []
    
    deadlock_events = []
    total_number_of_characters = 0
    for i, row in enumerate(db_rows):
        # ... rest of the method remains the same
        pass
