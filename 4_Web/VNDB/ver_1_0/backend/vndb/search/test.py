from remote.search import search

if __name__ == '__main__':
    print(search(
        resource_type='character',
        params={
            'id':'c113836',
        },
        response_size='large'
    ))