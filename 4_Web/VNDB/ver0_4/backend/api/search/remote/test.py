import os
import sys

# Get the absolute path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the 'backend' directory
backend_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
# Add the 'backend' directory to the Python path
sys.path.insert(0, backend_dir)

from api.search.remote.search import search
from api.search.remote.fields import VNDBFields
from api.search.remote.filters import VNDBFilters

def test_search():
    # Example: Get VN information
    vn_filters = {
        "and": [
            # Filter for developers of type "company"
            {"developer": {"type": "co"}},
            # Nested OR condition for specific developers
            {"or": [
                {"developer": {"search": "hooksoft"}},
                {"developer": {"search": "smee"}}
            ]}
        ]
    }

    vn_result = search('vn', vn_filters)
    print("VN Result:")
    print(f"Total results: {vn_result['count']}")
    print(f"First 5 results: {vn_result['results'][:5]}")

    # Example: Get Character information
    character_filters = {"vn": {"id": "v11"}}
    character_result = search('character', character_filters)
    print("\nCharacter Result:")
    print(f"Total results: {character_result['count']}")
    print(f"First 5 results: {character_result['results'][:5]}")

if __name__ == "__main__":
    test_search()