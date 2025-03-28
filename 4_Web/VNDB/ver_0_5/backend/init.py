import asyncio
import aiohttp
import time
import logging
import argparse
from logging.handlers import RotatingFileHandler
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

MAX_REQUESTS = 150
REQUEST_WINDOW = 120  # seconds

# Set up logging
logger = logging.getLogger('init')
logger.setLevel(logging.DEBUG)
file_handler = RotatingFileHandler('logs/init.log', maxBytes=10*1024*1024, backupCount=5)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

class ColoredConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        color = {
            logging.DEBUG: Fore.CYAN,
            logging.INFO: Fore.GREEN,
            logging.WARNING: Fore.YELLOW,
            logging.ERROR: Fore.RED,
            logging.CRITICAL: Fore.MAGENTA
        }.get(record.levelno, Fore.WHITE)
        self.stream.write(color + self.format(record) + Style.RESET_ALL + '\n')

console_handler = ColoredConsoleHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)

class RateLimiter:
    def __init__(self, max_requests: int, window: int):
        self.max_requests = max_requests
        self.window = window
        self.requests = []

    async def wait(self):
        now = time.time()
        self.requests = [t for t in self.requests if now - t < self.window]
        if len(self.requests) >= self.max_requests:
            sleep_time = self.window - (now - self.requests[0])
            if sleep_time > 0:
                logger.debug(f"Rate limit reached. Sleeping for {sleep_time:.2f} seconds")
                await asyncio.sleep(sleep_time)
        self.requests.append(time.time())

class VNProcessor:
    def __init__(self, start_vn: int, end_vn: int, max_retries: int = 10, error_action: str = 'stop', retry_delay: int = 0):
        self.start_vn = start_vn
        self.end_vn = end_vn
        self.max_retries = max_retries
        self.error_action = error_action
        self.retry_delay = retry_delay

        self.rate_limiter = RateLimiter(MAX_REQUESTS, REQUEST_WINDOW)

        self.session = None
        self.current_vn = start_vn
        self.consecutive_not_found = 0

    async def _make_request(self, method: str, url: str, **kwargs):
        await self.rate_limiter.wait()
        logger.debug(f"Sending {method} request to {url}")
        async with self.session.request(method, url, **kwargs) as response:
            return await response.json()

    async def download_vn_images(self, vnid, urls) -> bool:
        response = await self._make_request('GET', f'http://localhost:5000/vns/{vnid}')
        status = response.get('status')
        vn = response.get('results')

        if status != 'SUCCESS':
            logger.error(f'Failed to get vn {vnid} from API')
            return False

        image = vn.get('image', {})
        screenshots = vn.get('screenshots', [])
        urls = [
            image.get('url'),
            image.get('thumbnail'),
            *[screenshot.get('url') for screenshot in screenshots]
            *[screenshot.get('thumbnail') for screenshot in screenshots]
        ]
        urls = [url for url in urls if url]
        urls = list(set(urls))
        if not urls:
            logger.warning(f'No image URLs found for VN {vnid}')
            return True

        retry = 1
        status = None
        while retry < self.max_retries and status != 'SUCCESS':
            logger.debug(f"Downloading images for VN {vnid}, attempt {retry}")
            response = await self._make_request('POST', 'http://localhost:5001', json={'urls': urls})
            status = response['status']
            if status == 'SUCCESS':
                results = response['results']
                status = 'SUCCESS' if all(results.values()) else 'ERROR'

        if status == 'SUCCESS':
            logger.info(f'Successfully downloaded images for VN {vnid}')
            return True
        else: # ERROR
            logger.error(f'Failed to download images for VN {vnid}')
            if self.error_action == 'stop':
                print(Fore.RED + f"Error occurred while downloading images for VN {vnid}. Press Enter to retry this step, or type 'skip' to move to the next step." + Style.RESET_ALL)
                user_input = input().strip().lower()
                if user_input == 'skip':
                    return  True
                return False
            elif self.error_action == 'skip':
                print(Fore.RED + f"Error occurred while downloading images for VN {vnid}. Skipping to next VN." + Style.RESET_ALL)
                return True
            else: # retry
                print(Fore.RED + f"Error occurred while downloading images for VN {vnid}. Retrying in {self.retry_delay} seconds." + Style.RESET_ALL)
                await asyncio.sleep(self.retry_delay)
                return False

    async def update_vn(self, vnid: str) -> bool:
        retry = 1
        status = None
        while retry < self.max_retries and status not in ['SUCCESS', 'NOT_FOUND']:
            logger.debug(f"Processing VN {vnid}, attempt {retry}")
            response = await self._make_request('PUT', f"http://localhost:5000/vns/{vnid}")
            status = response['status']
            retry += 1

        if status == 'SUCCESS':
            logger.info(f'Successfully updated VN: {vnid}')
            self.current_vn += 1
            return True
        elif status == 'NOT_FOUND':
            logger.warning(f'VN {vnid} NOT FOUND')
            self.current_vn += 1
            return False
        else:
            logger.error(f'Error occurred while processing VN {vnid}.')
            if self.error_action == 'stop':
                print(Fore.RED + f"Error occurred while processing VN {self.current_vn}. Press Enter to retry this VN, or type 'skip' to move to the next VN." + Style.RESET_ALL)
                user_input = input().strip().lower()
                if user_input == 'skip':
                    self.current_vn += 1
            elif self.error_action == 'skip':
                print(Fore.RED + f"Error occurred while processing VN {self.current_vn}. Skipping to next VN." + Style.RESET_ALL)
                self.current_vn += 1
            else: # retry
                print(Fore.RED + f"Error occurred while processing VN {self.current_vn}. Retrying in {self.retry_delay} seconds." + Style.RESET_ALL)
                await asyncio.sleep(self.retry_delay)
            return False

    async def update_vn_related_resources(self, vnid: str, resource_type: str) -> bool:
        retry = 1
        status = None
        while retry < self.max_retries and status not in ['SUCCESS', 'NOT_FOUND']:
            logger.debug(f"Processing {resource_type} for VN {vnid}, attempt {retry}")
            response = await self._make_request('PUT', f"http://localhost:5000/vns/{vnid}/{resource_type}")
            status = response['status']
            if status == 'SUCCESS':
                results = response['results']
                status = 'SUCCESS' if all(results.values()) else 'ERROR'

        if status == 'SUCCESS':
            logger.info(f'Successfully updated {resource_type} for VN: {vnid}')
            return True
        elif status == 'NOT_FOUND':
            logger.warning(f'{resource_type.capitalize()} for VN {vnid} NOT FOUND')
            return True
        else: # ERROR
            logger.error(f'Error occurred while processing {resource_type} for VN {vnid}. Skipping to next VN.')
            if self.error_action == 'stop':
                print(Fore.RED + f"Error occurred while processing {resource_type} for VN {vnid}. Press Enter to retry this step, or type 'skip' to move to the next step." + Style.RESET_ALL)
                user_input = input().strip().lower()
                if user_input == 'skip':
                    return  True
                return False
            elif self.error_action == 'skip':
                print(f'Error occurred while processing {resource_type} for VN {vnid}. Skipping to next VN.')
                return True
            else: # retry
                print(Fore.RED + f"Error occurred while processing {resource_type} for VN {vnid}. Retrying in {self.retry_delay} seconds." + Style.RESET_ALL)
                await asyncio.sleep(self.retry_delay)
                return False

    async def run(self):
        logger.info(f"Starting VN processing from {self.start_vn} to {self.end_vn}")
        async with aiohttp.ClientSession() as self.session:
            self.current_vn = self.start_vn
            while self.current_vn <= self.end_vn:

                vnid = f'v{self.current_vn}'

                if not await self.update_vn(vnid):
                    continue

                for update_type in ['producers', 'tags', 'staff', 'characters', 'releases']:
                    while not await self.update_vn_related_resources(vnid, update_type):
                        ... # NO ACTION

                # while not await self.download_vn_images(vnid):
                #     ... # NO ACTION

                # await asyncio.sleep(1)

        logger.info("VN processing completed")

async def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Process VNs within a specified range.")
    parser.add_argument("-s", "--start_vn", type=int, default=1, help="Starting VN number (default: 1)")
    parser.add_argument("-e", "--end_vn", type=int, default=60000, help="Ending VN number (default: 60000)")
    parser.add_argument("-r", "--max_retries", type=int, default=10, help="Max Retries (default: 10)")
    parser.add_argument("--error_action", choices=['stop', 'skip', 'retry'], default='retry', 
                        help="Action to take on error: stop, skip, or retry (default: retry)")
    parser.add_argument("--retry_delay", type=int, default=0, 
                        help="Delay in seconds before retrying after an error (default: 0)")
    
    # Parse arguments
    args = parser.parse_args()
    
    start_vn = args.start_vn
    end_vn = args.end_vn
    max_retries = args.max_retries
    error_action = args.error_action
    retry_delay = args.retry_delay

    
    logger.info(f"Initializing VN processor for VNs {start_vn} to {end_vn}")
    processor = VNProcessor(start_vn, end_vn, max_retries, error_action, retry_delay)
    await processor.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("An unexpected error occurred in the main program")