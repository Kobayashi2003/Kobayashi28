from search import search

if __name__ == '__main__':
    print(search(
        resource_type='vn',
        params={
            'search':'缘之空',
            'has_anime':True
        },
        response_size='small',
    ))