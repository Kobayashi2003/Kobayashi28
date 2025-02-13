from remote.search import search

if __name__ == '__main__':
    print(search(
        resource_type='character',
        params={
            'sex':'m',
            'sex_spoil':'f'
        },
        page=1,
        limit=10,
        response_size='small'
    ))