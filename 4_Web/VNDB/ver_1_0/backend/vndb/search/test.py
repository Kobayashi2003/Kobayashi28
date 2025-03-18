from remote.search import search

if __name__ == '__main__':
    print(search(
        resource_type='vn',
        params={
            'developer_id': 'p98'
        },
        sort='id',
        page=1,
        limit=10,
        response_size='small'
    ))