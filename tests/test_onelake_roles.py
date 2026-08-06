import pytest
import sys
import os

# Add the src directory to the Python path and import the module directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Import the module directly without going through the package __init__.py
import importlib.util
spec = importlib.util.spec_from_file_location("onelake_roles", 
    os.path.join(os.path.dirname(__file__), '..', 'src', 'fabric_utils', 'onelake_roles.py'))
onelake_roles = importlib.util.module_from_spec(spec)
spec.loader.exec_module(onelake_roles)

PermissionRule = onelake_roles.PermissionRule
RowConstraint = onelake_roles.RowConstraint
ColumnConstraint = onelake_roles.ColumnConstraint


class TestPermissionRule:
    """Test class for PermissionRule"""

    def test_permission_rule_creation_basic(self):
        """Test basic PermissionRule creation with table name"""
        rule = PermissionRule(path="doctor_table")
        
        assert len(rule) == 2
        assert rule[0]["attributeName"] == "Path"
        assert rule[0]["attributeValueIncludedIn"] == ["/Tables/doctor_table"]
        assert rule[1]["attributeName"] == "Action"
        assert rule[1]["attributeValueIncludedIn"] == ["Read"]

    def test_permission_rule_creation_all_tables(self):
        """Test PermissionRule creation with 'all' for all tables"""
        rule = PermissionRule(path="all")
        
        assert len(rule) == 2
        assert rule[0]["attributeName"] == "Path"
        assert rule[0]["attributeValueIncludedIn"] == ["/Tables/*"]
        assert rule[1]["attributeName"] == "Action"
        assert rule[1]["attributeValueIncludedIn"] == ["Read"]

    def test_permission_rule_expected_format(self):
        """Test that PermissionRule creates the exact expected structure"""
        rule = PermissionRule(path="doctor_table")
        
        expected = [
            {
                "attributeName": "Path",
                "attributeValueIncludedIn": ["/Tables/doctor_table"]
            },
            {
                "attributeName": "Action",
                "attributeValueIncludedIn": ["Read"]
            }
        ]
        
        assert list(rule) == expected

    def test_permission_rule_add_method(self):
        """Test adding additional tables using the add method"""
        rule = PermissionRule(path="doctor_table")
        rule.add("memo_table")
        
        expected = [
            {
                "attributeName": "Path",
                "attributeValueIncludedIn": [
                    "/Tables/doctor_table",
                    "/Tables/memo_table"
                ]
            },
            {
                "attributeName": "Action",
                "attributeValueIncludedIn": ["Read"]
            }
        ]
        
        assert list(rule) == expected

    def test_permission_rule_add_multiple_tables(self):
        """Test adding multiple tables sequentially"""
        rule = PermissionRule(path="doctor_table")
        rule.add("memo_table")
        rule.add("patient_table")
        rule.add("appointment_table")
        
        # Verify path attribute has all tables
        path_attr = rule[0]
        assert path_attr["attributeName"] == "Path"
        assert "/Tables/doctor_table" in path_attr["attributeValueIncludedIn"]
        assert "/Tables/memo_table" in path_attr["attributeValueIncludedIn"]
        assert "/Tables/patient_table" in path_attr["attributeValueIncludedIn"]
        assert "/Tables/appointment_table" in path_attr["attributeValueIncludedIn"]
        assert len(path_attr["attributeValueIncludedIn"]) == 4

    def test_permission_rule_add_duplicate_table(self):
        """Test that adding duplicate tables doesn't create duplicates"""
        rule = PermissionRule(path="doctor_table")
        rule.add("memo_table")
        rule.add("memo_table")  # Duplicate
        rule.add("doctor_table")  # Also duplicate
        
        path_attr = rule[0]
        assert path_attr["attributeValueIncludedIn"] == [
            "/Tables/doctor_table",
            "/Tables/memo_table"
        ]

    def test_permission_rule_handles_tables_prefix(self):
        """Test that existing /Tables/ prefix is handled correctly"""
        rule = PermissionRule(path="/Tables/doctor_table")
        
        assert rule[0]["attributeValueIncludedIn"] == ["/Tables/doctor_table"]
        
        # Test adding with prefix
        rule.add("/Tables/memo_table")
        assert rule[0]["attributeValueIncludedIn"] == [
            "/Tables/doctor_table",
            "/Tables/memo_table"
        ]

    def test_permission_rule_path_formatting(self):
        """Test various path formatting scenarios"""
        # Test with whitespace
        rule = PermissionRule(path="  doctor_table  ")
        assert rule[0]["attributeValueIncludedIn"] == ["/Tables/doctor_table"]
        
        # Test case sensitivity of 'all'
        rule_all_upper = PermissionRule(path="ALL")
        assert rule_all_upper[0]["attributeValueIncludedIn"] == ["/Tables/*"]
        
        rule_all_mixed = PermissionRule(path="All")
        assert rule_all_mixed[0]["attributeValueIncludedIn"] == ["/Tables/*"]

    # Validation Tests
    def test_permission_rule_invalid_path_type(self):
        """Test that non-string path raises ValueError"""
        with pytest.raises(ValueError, match="path must be a string"):
            PermissionRule(path=123)
            
        with pytest.raises(ValueError, match="path must be a string"):
            PermissionRule(path=None)
            
        with pytest.raises(ValueError, match="path must be a string"):
            PermissionRule(path=[])

    def test_permission_rule_empty_path(self):
        """Test that empty path raises ValueError"""
        with pytest.raises(ValueError, match="path cannot be empty"):
            PermissionRule(path="")
            
        with pytest.raises(ValueError, match="path cannot be empty"):
            PermissionRule(path="   ")  # Only whitespace

    def test_permission_rule_add_invalid_path(self):
        """Test that add method validates inputs"""
        rule = PermissionRule(path="doctor_table")
        
        with pytest.raises(ValueError, match="path must be a string"):
            rule.add(123)
            
        with pytest.raises(ValueError, match="path cannot be empty"):
            rule.add("")

    # Edge cases and special characters
    def test_permission_rule_with_special_characters(self):
        """Test PermissionRule with special characters in table names"""
        rule = PermissionRule(path="table-with-dashes")
        assert rule[0]["attributeValueIncludedIn"] == ["/Tables/table-with-dashes"]
        
        rule.add("table_with_underscores")
        rule.add("table.with.dots")
        
        expected_paths = [
            "/Tables/table-with-dashes",
            "/Tables/table_with_underscores",
            "/Tables/table.with.dots"
        ]
        assert rule[0]["attributeValueIncludedIn"] == expected_paths

    def test_permission_rule_unicode_support(self):
        """Test PermissionRule with unicode characters"""
        rule = PermissionRule(path="médecins")
        assert rule[0]["attributeValueIncludedIn"] == ["/Tables/médecins"]
        
        rule.add("données")
        assert "/Tables/données" in rule[0]["attributeValueIncludedIn"]

    def test_permission_rule_is_list_subclass(self):
        """Test that PermissionRule is a proper list subclass"""
        rule = PermissionRule(path="doctor_table")
        
        # Should be able to use list methods
        assert len(rule) == 2
        assert isinstance(rule, list)
        
        # Should be indexable
        assert rule[0]["attributeName"] == "Path"
        assert rule[1]["attributeName"] == "Action"

    def test_permission_rule_json_serializable(self):
        """Test that PermissionRule is JSON serializable"""
        import json
        
        rule = PermissionRule(path="doctor_table")
        rule.add("memo_table")
        
        # Should be able to serialize without errors
        json_string = json.dumps(rule)
        
        # Should be able to deserialize
        deserialized = json.loads(json_string)
        assert deserialized == list(rule)


# Integration test to verify complete workflow
class TestPermissionRuleIntegration:
    """Integration tests for PermissionRule workflow"""

    def test_complete_workflow_example(self):
        """Test the complete example workflow from the user requirements"""
        # Initial creation as specified
        perm_rule = PermissionRule(path='doctor_table')
        
        expected_initial = [
            {
                "attributeName": "Path",
                "attributeValueIncludedIn": [
                    "/Tables/doctor_table"
                ]
            },
            {
                "attributeName": "Action",
                "attributeValueIncludedIn": [
                    "Read"
                ]
            }
        ]
        
        assert list(perm_rule) == expected_initial
        
        # Add memo_table as specified
        perm_rule.add('memo_table')
        
        expected_after_add = [
            {
                "attributeName": "Path",
                "attributeValueIncludedIn": [
                    "/Tables/doctor_table",
                    "/Tables/memo_table"
                ]
            },
            {
                "attributeName": "Action",
                "attributeValueIncludedIn": [
                    "Read"
                ]
            }
        ]
        
        assert list(perm_rule) == expected_after_add

    def test_multiple_permission_rules(self):
        """Test creating multiple separate PermissionRule instances"""
        rule1 = PermissionRule(path="doctor_table")
        rule2 = PermissionRule(path="patient_table")
        
        # Should be independent
        rule1.add("memo_table")
        
        assert rule1[0]["attributeValueIncludedIn"] == ["/Tables/doctor_table", "/Tables/memo_table"]
        assert rule2[0]["attributeValueIncludedIn"] == ["/Tables/patient_table"]

    def test_all_tables_workflow(self):
        """Test workflow with 'all' tables"""
        rule = PermissionRule(path="all")
        
        # Should create wildcard path
        assert rule[0]["attributeValueIncludedIn"] == ["/Tables/*"]
        
        # Adding specific tables to 'all' rule
        rule.add("specific_table")
        
        # Should now have both wildcard and specific
        expected_paths = ["/Tables/*", "/Tables/specific_table"]
        assert rule[0]["attributeValueIncludedIn"] == expected_paths


class TestRowConstraint:
    """Test class for RowConstraint"""

    def test_row_constraint_creation_basic(self):
        """Test basic RowConstraint creation"""
        rls = RowConstraint(
            table="doctor_table",
            rls_definition="SELECT * FROM doctor_table WHERE department = 'Cardiology'"
        )
        
        assert rls.table == "/Tables/doctor_table"
        assert rls.rls_definition == "SELECT * FROM doctor_table WHERE department = 'Cardiology'"

    def test_row_constraint_expected_format(self):
        """Test that RowConstraint creates the exact expected structure"""
        constraint = RowConstraint(
            table="doctor_table",
            rls_definition="SELECT * FROM doctor_table WHERE department = 'Cardiology'"
        )
        
        expected = [
            {
                "tablePath": "/Tables/doctor_table",
                "value": "SELECT * FROM doctor_table WHERE department = 'Cardiology'"
            }
        ]
        
        assert list(constraint) == expected

    def test_row_constraint_add_constraint_method(self):
        """Test adding additional constraints using add_constraint method"""
        constraint = RowConstraint(
            table="doctor_table",
            rls_definition="SELECT * FROM doctor_table WHERE department = 'Cardiology'"
        )
        
        constraint.add_constraint(
            table="nurse_table",
            rls_definition="SELECT * FROM nurse_table WHERE shift = 'day'"
        )
        
        assert len(constraint) == 2
        assert constraint[0]["tablePath"] == "/Tables/doctor_table"
        assert constraint[1]["tablePath"] == "/Tables/nurse_table"

    def test_row_constraint_invalid_table_type(self):
        """Test that invalid table raises ValueError"""
        with pytest.raises(ValueError, match="table must be a string"):
            RowConstraint(
                table=123,
                rls_definition="SELECT * FROM doctor_table"
            )

    def test_row_constraint_invalid_rls_type(self):
        """Test that invalid rls_definition raises ValueError"""
        with pytest.raises(ValueError, match="rls_definition must be a string"):
            RowConstraint(
                table="doctor_table",
                rls_definition=456
            )

    def test_row_constraint_table_prefix_auto_added(self):
        """Test that table automatically gets /Tables/ prefix when missing"""
        constraint = RowConstraint(
            table="doctor_table",  # Missing /Tables/ prefix
            rls_definition="SELECT * FROM doctor_table"
        )
        
        # Should automatically add the prefix
        assert constraint.table == "/Tables/doctor_table"
        assert constraint[0]["tablePath"] == "/Tables/doctor_table"

    def test_row_constraint_invalid_rls_syntax(self):
        """Test that RLS not starting with SELECT * FROM raises ValueError"""
        with pytest.raises(ValueError, match="rls_definition must start with SELECT \\* FROM"):
            RowConstraint(
                table="doctor_table",
                rls_definition="DELETE FROM doctor_table"
            )

    def test_row_constraint_is_list_subclass(self):
        """Test that RowConstraint is a proper list subclass"""
        constraint = RowConstraint(
            table="doctor_table",
            rls_definition="SELECT * FROM doctor_table"
        )
        
        # Should be able to use list methods
        assert len(constraint) == 1
        assert isinstance(constraint, list)
        
        # Should be indexable
        assert constraint[0]["tablePath"] == "/Tables/doctor_table"
        assert constraint[0]["value"] == "SELECT * FROM doctor_table"

    def test_row_constraint_json_serializable(self):
        """Test that RowConstraint is JSON serializable"""
        import json
        
        constraint = RowConstraint(
            table="doctor_table",
            rls_definition="SELECT * FROM doctor_table"
        )
        
        # Should be able to serialize without errors
        json_string = json.dumps(constraint)
        
        # Should be able to deserialize
        deserialized = json.loads(json_string)
        assert deserialized == list(constraint)


class TestColumnConstraint:
    """Test class for ColumnConstraint"""
    
    def test_column_constraint_creation_basic(self):
        """Test basic ColumnConstraint creation"""
        constraint = ColumnConstraint(
            table="doctor_table",
            column_names=["name", "department", "salary"],
            column_effect="Permit",
            column_action=["Read"]
        )
        
        # Check that it creates the expected structure
        assert len(constraint) == 1
        assert constraint[0]["tablePath"] == "/Tables/doctor_table"
        assert constraint[0]["columnNames"] == ["name", "department", "salary"]
        assert constraint[0]["columnEffect"] == "Permit"
        assert constraint[0]["columnAction"] == ["Read"]

    def test_column_constraint_table_prefix_auto_added(self):
        """Test that table automatically gets /Tables/ prefix when missing"""
        constraint = ColumnConstraint(
            table="doctor_table",  # Missing /Tables/ prefix
            column_names=["name"],
            column_effect="Permit",
            column_action=["Read"]
        )
        
        # Should automatically add the prefix
        assert constraint[0]["tablePath"] == "/Tables/doctor_table" 
