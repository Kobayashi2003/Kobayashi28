import win32console
import win32con
import time
import multiprocessing
import random

def process_function(process_id, output_queue):
    log_types = ['INFO', 'WARNING', 'ERROR']
    for i in range(50):  # Generate 50 log entries
        log_type = random.choice(log_types)
        message = f"Process {process_id} [{log_type}]: Log entry {i}"
        output_queue.put((process_id, message))
        time.sleep(random.uniform(0.5, 2))  # Random delay between 0.5 and 2 seconds

def display_output(output_queues):
    screen_buffer = win32console.CreateConsoleScreenBuffer(
        DesiredAccess=win32con.GENERIC_READ | win32con.GENERIC_WRITE,
        ShareMode=0,
        SecurityAttributes=None,
        Flags=1
    )
    screen_buffer.SetConsoleActiveScreenBuffer()

    buffer_info = screen_buffer.GetConsoleScreenBufferInfo()
    width = buffer_info['Size'].X
    height = buffer_info['Size'].Y
    column_width = width // 3

    while True:
        for i, queue in enumerate(output_queues):
            if not queue.empty():
                process_id, message = queue.get()
                start_x = i * column_width
                coord = win32console.PyCOORDType(start_x, height - 1)

                scroll_rectangle = win32console.PySMALL_RECTType(
                    start_x, 0, start_x + column_width - 1, height - 1
                )
                clip_rectangle = win32console.PySMALL_RECTType(
                    start_x, 0, start_x + column_width - 1, height - 1
                )
                fill_char = ' '
                fill_attribute = 0
                screen_buffer.ScrollConsoleScreenBuffer(
                    scroll_rectangle, clip_rectangle, coord, fill_char, fill_attribute
                )

                # Truncate message if it's longer than the column width
                truncated_message = message[:column_width].ljust(column_width)
                screen_buffer.WriteConsoleOutputCharacter(truncated_message, coord)

        time.sleep(0.1)

if __name__ == "__main__":
    output_queues = [multiprocessing.Queue() for _ in range(3)]
    processes = [
        multiprocessing.Process(target=process_function, args=(i, output_queues[i]))
        for i in range(3)
    ]

    for process in processes:
        process.start()

    try:
        display_output(output_queues)
    except KeyboardInterrupt:
        pass

    for process in processes:
        process.join()