from flask_restx import reqparse

pagination_parser = reqparse.RequestParser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Page number')
pagination_parser.add_argument('per_page', type=int, required=False, default=10, help='Number of items per page')
pagination_parser.add_argument('sort', type=str, required=False, default='id', help='Field to sort by')
pagination_parser.add_argument('reverse', type=bool, required=False, default=False, help='Sort in reverse order')

search_pagination_parser = pagination_parser.copy().add_argument(
    'query', type=str, required=True, help='Search query')