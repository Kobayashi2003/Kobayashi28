from search import search

if __name__ == '__main__':
    print(search(
        resource_type='tag',
        params={'id':'g1'},
        response_size='large',
    ))