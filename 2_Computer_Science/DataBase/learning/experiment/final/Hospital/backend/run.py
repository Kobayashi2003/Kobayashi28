if __name__ == '__main__':
    import sys
    import signal
    from app import create_app
    from clean import delete_pycache_folders

    def signal_handler(signum, frame):
        print("\nReceived interrupt signal. Terminating processes...")
        delete_pycache_folders()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    app = create_app()
    app.run(debug=False,  host='0.0.0.0', port=5000)