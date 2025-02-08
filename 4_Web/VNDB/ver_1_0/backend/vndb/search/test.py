from remote.search import search

if __name__ == '__main__':
    print(search(
        resource_type='vn',
        params={
            'id':'v32132',
        },
        response_size='large'
    )['results'][0]['va'])