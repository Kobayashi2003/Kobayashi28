if __name__ == '__main__':
    import jmcomic
    import argparse
    import os
    import yaml

    parser = argparse.ArgumentParser(description='Jmcomic download')
    parser.add_argument('id', type=int, nargs='+', default=None, help='the id of the comic')
    parser.add_argument('-c', '--config-path', type=str, default='option.yml', help='the path of the config file')
    parser.add_argument('-d', '--directory', type=str, default=None, help='the dirctory path to save the comic')

    args = parser.parse_args()

    if not os.path.exists(args.config_path) or os.path.getsize(args.config_path) == 0:
        jmcomic.JmOption.default().to_file(args.config_path)

    directory_save = None

    if args.directory:
        option_data = yaml.load(open(args.config_path, 'r', encoding='utf-8'), Loader=yaml.Loader)

        if not option_data.get('dir_rule'):
            option_data['dir_rule'] = {}
        dir_rule = option_data['dir_rule']

        if dir_rule.get('base_dir'):
            directory_save = dir_rule['base_dir']
        dir_rule['base_dir'] = args.directory

        yaml.dump(option_data, open(args.config_path, 'w', encoding='utf-8'), Dumper=yaml.Dumper, encoding='utf-8')

    option = jmcomic.create_option_by_file(args.config_path)

    if directory_save:
        option_data = yaml.load(open(args.config_path, 'r', encoding='utf-8'), Loader=yaml.Loader)
        option_data['dir_rule']['base_dir'] = directory_save
        yaml.dump(option_data, open(args.config_path, 'w', encoding='utf-8'), Dumper=yaml.Dumper, encoding='utf-8')

    jmcomic.download_album(args.id, option)
