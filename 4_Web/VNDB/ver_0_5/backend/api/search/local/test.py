import os
import sys

# Get the absolute path of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the 'backend' directory
backend_dir = os.path.abspath(os.path.join(current_dir, '..', '..', '..'))
# Add the 'backend' directory to the Python path
sys.path.insert(0, backend_dir)

from flask import Flask

from api import db
from api.search.local.search import search
from api.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

def test_search():
    with app.app_context():
        # Test VN search
        print("Testing VN search:")
        vn_params = {
            'search': 'test',
            'olang': 'en',
            'length_minutes': '>1000',
            'tag': 'romance,action+adventure',
            'developer': 'key'
        }
        vn_results = search('vn', vn_params)
        print(f"Found {len(vn_results)} VNs")
        for vn in vn_results[:5]:  # Print first 5 results
            print(vn)
        print()

        # Test Character search
        print("Testing Character search:")
        char_params = {
            'search': 'test',
            'height': '>160',
            'age': '<20',
            'trait': 'hair:blonde,eyes:green',
            'vns': 'v1'
        }
        char_results = search('character', char_params)
        print(f"Found {len(char_results)} Characters")
        for char in char_results[:5]:  # Print first 5 results
            print(char)
        print()

        # Test Tag search
        print("Testing Tag search:")
        tag_params = {
            'search': 'romance',
            'category': 'cont',
            'searchable': 'true'
        }
        tag_results = search('tag', tag_params)
        print(f"Found {len(tag_results)} Tags")
        for tag in tag_results[:5]:  # Print first 5 results
            print(tag)
        print()

        # Test Producer search
        print("Testing Producer search:")
        producer_params = {
            'search': 'studio',
            'type': 'co',
            'lang': 'ja'
        }
        producer_results = search('producer', producer_params)
        print(f"Found {len(producer_results)} Producers")
        for producer in producer_results[:5]:  # Print first 5 results
            print(producer)
        print()

        # Test Staff search
        print("Testing Staff search:")
        staff_params = {
            'search': 'writer',
            'gender': 'f',
            'lang': 'en',
            'ismain': 'true'
        }
        staff_results = search('staff', staff_params)
        print(f"Found {len(staff_results)} Staff members")
        for staff in staff_results[:5]:  # Print first 5 results
            print(staff)
        print()

        # Test Trait search
        print("Testing Trait search:")
        trait_params = {
            'search': 'hair',
            'searchable': 'true',
            'group_name': 'physical',
            'char_count': '>100'
        }
        trait_results = search('trait', trait_params)
        print(f"Found {len(trait_results)} Traits")
        for trait in trait_results[:5]:  # Print first 5 results
            print(trait)

if __name__ == "__main__":
    test_search()