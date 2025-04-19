import multiprocessing
import traceback
import logging
from datetime import datetime
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('process_log.log'),
        logging.StreamHandler()
    ]
)


def run_in_subprocess(timeout=None, log_results=True, log_errors=True, use_tqdm=False):
    def decorator(func):
        def wrapper(*args, **kwargs):
            def target_func(queue, *args, **kwargs):
                try:
                    start_time = datetime.now()

                    # Если включен tqdm, оборачиваем аргументы, которые могут быть итерабельными
                    if use_tqdm and 'iterable' in kwargs:
                        kwargs['iterable'] = tqdm(kwargs['iterable'], desc=f"Processing {func.__name__}")

                    result = func(*args, **kwargs)
                    end_time = datetime.now()
                    execution_time = (end_time - start_time).total_seconds()

                    # Логируем успех
                    if log_results:
                        logging.info(
                            f"Function `{func.__name__}` completed in {execution_time:.2f} seconds. Result: {result}")
                    queue.put(('success', result, execution_time))
                except Exception as e:
                    error_msg = traceback.format_exc()
                    if log_errors:
                        logging.error(f"Error in function `{func.__name__}`: {error_msg}")
                    queue.put(('error', error_msg))

            queue = multiprocessing.Queue()
            process = multiprocessing.Process(target=target_func, args=(queue, *args), kwargs=kwargs)
            process.start()
            process.join(timeout)

            if process.is_alive():
                process.terminate()
                timeout_msg = f"Function `{func.__name__}` timed out after {timeout} seconds."
                logging.error(timeout_msg)
                raise TimeoutError(timeout_msg)

            status, result, exec_time = queue.get()
            if status == 'error':
                raise RuntimeError(f"Error in subprocess:\n{result}")
            return result

        return wrapper

    return decorator


# @run_in_subprocess(timeout=60, use_tqdm=True)
# def process_large_data(iterable):
#     import time
#     results = []
#     for item in iterable:
#         time.sleep(1)  # Имитируем долгую обработку
#         results.append(item * 10)
#     return results
#
# # Список данных
# large_data = range(100)  # 100 элементов
#
# try:
#     result = process_large_data(iterable=large_data)
#     print(f"Processed data: {result[:10]}...")  # Пример частичного вывода
# except Exception as e:
#     print(f"Caught an error: {e}")