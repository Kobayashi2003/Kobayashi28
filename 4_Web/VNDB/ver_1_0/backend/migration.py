import argparse
import subprocess
import sys

COMMANDS = ['init', 'migrate', 'upgrade', 'downgrade']

def run_migration(app, command):
    full_command = ['flask', '--app', app, 'db', command, '--directory', f"{app}/migrations"]
    result = subprocess.run(full_command, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    parser = argparse.ArgumentParser(description="Manage database migrations for a Flask app.")
    parser.add_argument('command', choices=COMMANDS, help='The command to run (init, migrate, upgrade, or downgrade)')
    parser.add_argument('app', help='The app to run the command for')
    args = parser.parse_args()
    run_migration(args.app, args.command)

if __name__ == '__main__':
    main()