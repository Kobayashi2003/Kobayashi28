import os
import sys

# Get the absolute path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the 'backend' directory
backend_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
# Add the 'backend' directory to the Python path
sys.path.insert(0, backend_dir)

from api.search.remote.search import *
from api.search.remote.fields import * 
from api.search.remote.filters import *

def test_search():
    api = VNDBAPIWrapper()
    
    # Example: Get VN information
    vn_filters = {"search": "Steins;Gate"}
    vn_fields = [
        *VNDBFields.VN.IMAGE.ALL,
        VNDBFields.VN.ID,
        VNDBFields.VN.TITLE,
        VNDBFields.VN.RELEASED,
        VNDBFields.VN.DESCRIPTION,
        VNDBFields.VN.IMAGE.URL,
        VNDBFields.VN.SCREENSHOTS.URL,
        VNDBFields.VN.TAGS.ID,
        VNDBFields.VN.TAGS.RATING
    ]
    vn_result = api.get_vn(vn_filters, vn_fields)
    print("VN Result:", vn_result)

    # Example: Get Character information
    character_filters = {"vn": {"id": "v11"}}
    character_fields = [
        VNDBFields.Character.ID,
        VNDBFields.Character.NAME,
        VNDBFields.Character.DESCRIPTION,
        VNDBFields.Character.IMAGE.URL,
        VNDBFields.Character.TRAITS.ID,
        VNDBFields.Character.TRAITS.NAME
    ]
    character_result = api.get_character(character_filters, character_fields)
    print("Character Result:", character_result)

    # Example: Get User List Labels
    user_labels = api.get_user_list_labels(user="u2")
    print("User Labels:", user_labels)

def test_fields():

    # Test all_fields method
    print("\nAll VN Fields:", VNDBFields.VN.ALL)
    print("All Character Fields:", VNDBFields.Character.ALL)

    # Test string representation of nested FieldGroups
    print("\nVN IMAGE fields:", VNDBFields.VN.IMAGE.ALL)
    print("Character IMAGE fields:", VNDBFields.Character.IMAGE.ALL)

    # Test accessing individual fields in nested FieldGroups
    print("\nVN IMAGE URL:", VNDBFields.VN.IMAGE.URL)
    print("VN SCREENSHOTS URL:", VNDBFields.VN.SCREENSHOTS.URL)
    print("Character TRAITS NAME:", VNDBFields.Character.TRAITS.NAME)

def test_filters():
    # Test VN filters
    print("Testing VN filters:")
    vn_filter = VNDBFilters.VN["search"]
    print(f"Search filter - Name: {vn_filter.name}, Type: {vn_filter.filter_type}, Flags: {vn_filter.flags}")
    
    vn_filter = VNDBFilters.VN["released"]
    print(f"Released filter - Name: {vn_filter.name}, Type: {vn_filter.filter_type}, Flags: {vn_filter.flags}")

    # Test CHARACTER filters
    print("\nTesting CHARACTER filters:")
    char_filter = VNDBFilters.CHARACTER["height"]
    print(f"Height filter - Name: {char_filter.name}, Type: {char_filter.filter_type}, Flags: {char_filter.flags}")

    # Test PRODUCER filters
    print("\nTesting PRODUCER filters:")
    producer_filter = VNDBFilters.PRODUCER["lang"]
    print(f"Lang filter - Name: {producer_filter.name}, Type: {producer_filter.filter_type}, Flags: {producer_filter.flags}")

    # Test STAFF filters
    print("\nTesting STAFF filters:")
    staff_filter = VNDBFilters.STAFF["gender"]
    print(f"Gender filter - Name: {staff_filter.name}, Type: {staff_filter.filter_type}, Flags: {staff_filter.flags}")

    # Test TAG filters
    print("\nTesting TAG filters:")
    tag_filter = VNDBFilters.TAG["category"]
    print(f"Category filter - Name: {tag_filter.name}, Type: {tag_filter.filter_type}, Flags: {tag_filter.flags}")

    # Test TRAIT filters
    print("\nTesting TRAIT filters:")
    trait_filter = VNDBFilters.TRAIT["search"]
    print(f"Search filter - Name: {trait_filter.name}, Type: {trait_filter.filter_type}, Flags: {trait_filter.flags}")

    # Test FilterOperator
    print("\nTesting FilterOperator:")
    print(f"EQUAL: {FilterOperator.EQUAL.value}")
    print(f"GREATER_THAN: {FilterOperator.GREATER_THAN.value}")

    # Test FilterType
    print("\nTesting FilterType:")
    print(f"STRING: {FilterType.STRING}")
    print(f"INTEGER: {FilterType.INTEGER}")

    # Test creating a custom VNDBFilter
    print("\nTesting custom VNDBFilter:")
    custom_filter = VNDBFilter("custom", FilterType.FLOAT, "o,i")
    print(f"Custom filter - Name: {custom_filter.name}, Type: {custom_filter.filter_type}, Flags: {custom_filter.flags}")

if __name__ == "__main__":
    test_search()
    test_fields()
    test_filters()

