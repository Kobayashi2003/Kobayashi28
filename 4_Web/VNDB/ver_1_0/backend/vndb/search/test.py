from remote.search import search

if __name__ == '__main__':
    print(search(
        resource_type='vn',
        params={
            'id':'v32132,v26180',
        },
        response_size='small'
    ))