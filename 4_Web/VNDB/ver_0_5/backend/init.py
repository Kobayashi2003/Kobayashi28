import asyncio
import aiohttp
import time
import logging
from logging.handlers import RotatingFileHandler
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

STAGES = ['updateVN', 'updateProducers', 'updateTags', 'updateStaff', 'updateCharacters', 'updateReleases', 'downloadImages']
MAX_REQUESTS = 150
REQUEST_WINDOW = 120  # seconds
MAX_RETRIES = 3

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
    def __init__(self, start_vn: int, end_vn: int):
        self.start_vn = start_vn
        self.end_vn = end_vn
        self.rate_limiter = RateLimiter(MAX_REQUESTS, REQUEST_WINDOW)
        self.session = None
        self.current_vn = start_vn
        self.current_stage = STAGES[0]
        self.consecutive_not_found = 0

    async def _make_request(self, method: str, url: str, **kwargs):
        await self.rate_limiter.wait()
        logger.debug(f"Sending {method} request to {url}")
        async with self.session.request(method, url, **kwargs) as response:
            return await response.json()

    async def _process_update(self, vnid: str, update_type: str) -> bool:
        logger.info(f"Starting to update {update_type} for VN: {vnid}")

        response = await self._make_request('PUT', f"http://localhost:5000/vns/{vnid}/{update_type}")
        status = response.get('status')
        results = response.get('results')
        if not status:
            logger.error('Invalid response from server')
            return False
        if status == 'ERROR':
            logger.error(results)
            return False
        if status == 'NOT_FOUND':
            logger.warning(f'{update_type.capitalize()} for VN {vnid} NOT FOUND')
            self.consecutive_not_found += 1
            return False
        if status != 'SUCCESS':
            logger.error(f'Unknown status: {status}')
            return False

        self.consecutive_not_found = 0  # Reset counter on success

        for key, value in results.items():
            if not value:
                logger.error(f'Error in key {key}, value {value}')

        if all(results.values()):
            logger.info(f"ALL SUCCESS")
        elif any(results.values()):
            logger.warning(f"Some ERRORs")
        else:
            logger.error(f"ALL FAILED")
            return False

        return True

    async def update_vn(self, vnid: str) -> bool:
        logger.info(f"Starting to update VN: {vnid}")

        response = await self._make_request('PUT', f"http://localhost:5000/vns/{vnid}")
        status = response.get('status')
        results = response.get('results')
        if not status:
            logger.error('Invalid response from server')
            return False
        if status == 'ERROR':
            logger.error(results)
            return False
        if status == 'NOT_FOUND':
            logger.warning(f'VN {vnid} NOT FOUND')
            self.consecutive_not_found += 1
            return False
        if status != 'SUCCESS':
            logger.error(f'Unknown status: {status}')
            return False

        self.consecutive_not_found = 0  # Reset counter on success
        logger.info(f"Successfully updated VN: {vnid}")
        return True

    async def update_producers(self, vnid: str) -> bool:
        return await self._process_update(vnid, 'producers')

    async def update_tags(self, vnid: str) -> bool:
        return await self._process_update(vnid, 'tags')

    async def update_staff(self, vnid: str) -> bool:
        return await self._process_update(vnid, 'staff')

    async def update_characters(self, vnid: str) -> bool:
        return await self._process_update(vnid, 'characters')

    async def update_releases(self, vnid: str) -> bool:
        return await self._process_update(vnid, 'releases')

    async def download_images(self, vnid: str) -> bool:
        logger.info(f"Starting to download images for VN: {vnid}")

        response = await self._make_request('GET', f"http://localhost:5000/vns/{vnid}")
        status = response.get('status')
        results = response.get('results')
        if not status:
            logger.error('Invalid response from server')
            return False
        if status == 'ERROR':
            logger.error(results)
            return False
        if status == 'NOT_FOUND':
            logger.error(f'VN {vnid} NOT FOUND')
            self.consecutive_not_found += 1
            return False
        if status != 'SUCCESS':
            logger.error(f'Unknown status: {status}')
            return False

        self.consecutive_not_found = 0  # Reset counter on success

        vn_image = results.get('image', {})
        vn_screenshots = results.get('screenshots', [])
        urls = [
            vn_image.get('url'),
            vn_image.get('thumbnail'),
            *[screenshot.get('url') for screenshot in vn_screenshots],
        ]
        urls = [url for url in urls if url]
        if not urls:
            logger.warning(f'No valid URLs found for VN: {vnid}')
            return True

        response = await self._make_request('POST', 'http://localhost:5001', json={'urls': urls})
        status = response.get('status')
        results = response.get('results')
        if not status:
            logger.error('Invalid response from server')
            return False
        if status == 'ERROR':
            logger.error(results)
            return False
        if status != 'SUCCESS':
            logger.error(f'Unknown status: {status}')
            return False

        for key, value in results.items():
            if not key:
                logger.error(f'Error in key {key}, value {value}')

        if all(results.values()):
            logger.info(f"ALL SUCCESS")
        elif any(results.values()):
            logger.warning(f"Some SUCCESS")
        else:
            logger.error(f"ALL FAILED")
            return False

        return True

    async def process_vn(self, vn_number: int):
        vnid = f"v{vn_number}"
        logger.info(f"Starting to process VN: {vnid}")
        self.consecutive_not_found = 0  # Reset counter at the start of each VN

        for stage in STAGES:
            self.current_stage = stage
            stage_not_found_count = 0
            for attempt in range(MAX_RETRIES):
                try:
                    if stage == 'updateVN':
                        result = await self.update_vn(vnid)
                        if not result and self.consecutive_not_found >= 3:
                            logger.warning(f"Skipping VN {vnid} due to 3 consecutive NOT_FOUND responses in updateVN")
                            return False
                    elif stage == 'updateProducers':
                        result = await self.update_producers(vnid)
                    elif stage == 'updateTags':
                        result = await self.update_tags(vnid)
                    elif stage == 'updateStaff':
                        result = await self.update_staff(vnid)
                    elif stage == 'updateCharacters':
                        result = await self.update_characters(vnid)
                    elif stage == 'updateReleases':
                        result = await self.update_releases(vnid)
                    elif stage == 'downloadImages':
                        # result = await self.download_images(vnid)
                        result = True
                    
                    if result:
                        logger.info(f"Successfully completed {stage} for {vnid}")
                        break
                    else:
                        logger.error(f"Error in {stage} for {vnid} (Attempt {attempt + 1}/{MAX_RETRIES})")
                        if stage != 'updateVN' and self.consecutive_not_found >= 3:
                            stage_not_found_count += 1
                            if stage_not_found_count >= 3:
                                logger.warning(f"Skipping stage {stage} for VN {vnid} due to 3 consecutive NOT_FOUND responses")
                                break

                except Exception as e:
                    logger.exception(f"Error in {stage} for {vnid}: {str(e)} (Attempt {attempt + 1}/{MAX_RETRIES})")
                
                if attempt == MAX_RETRIES - 1 and stage == 'updateVN':
                    return False
                
                await asyncio.sleep(0.5)

        return True

    async def run(self):
        logger.info(f"Starting VN processing from {self.start_vn} to {self.end_vn}")
        async with aiohttp.ClientSession() as self.session:
            self.current_vn = self.start_vn
            while self.current_vn <= self.end_vn:
                success = await self.process_vn(self.current_vn)
                if not success:
                    if self.consecutive_not_found >= 3:
                        logger.warning(f"Skipping VN {self.current_vn} due to 3 consecutive NOT_FOUND responses")
                        self.current_vn += 1
                        self.current_stage = STAGES[0]
                        self.consecutive_not_found = 0
                        continue

                    logger.error(f"Error occurred while processing VN {self.current_vn}. Pausing execution.")
                    print(Fore.RED + f"Error occurred while processing VN {self.current_vn}. Press Enter to retry this VN, or type 'skip' to move to the next VN." + Style.RESET_ALL)
                    user_input = input().strip().lower()
                    if user_input == 'skip':
                        self.current_vn += 1
                        self.current_stage = STAGES[0]
                    # If not 'skip', we'll retry the current VN
                else:
                    self.current_vn += 1
                    self.current_stage = STAGES[0]
        logger.info("VN processing completed")

async def main():
    start_vn = 2271
    end_vn = 30000
    logger.info(f"Initializing VN processor for VNs {start_vn} to {end_vn}")
    processor = VNProcessor(start_vn, end_vn)
    await processor.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        logger.exception("An unexpected error occurred in the main program")

