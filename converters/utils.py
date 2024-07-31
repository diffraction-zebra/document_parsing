import asyncio


async def run_with_timeout(coroutines, total_timeout):
    tasks = [asyncio.create_task(coro) for coro in coroutines]
    start_time = asyncio.get_running_loop().time()
    results = []

    while tasks and (asyncio.get_running_loop().time() - start_time) < total_timeout:
        elapsed = asyncio.get_running_loop().time() - start_time
        remaining_time = total_timeout - elapsed
        print(remaining_time)
        if remaining_time <= 0:
            break

        done, pending = await asyncio.wait(tasks, timeout=remaining_time, return_when=asyncio.FIRST_COMPLETED)

        print(len(done), len(pending))
        for task in done:
            if not task.cancelled() and task.exception() is None:
                results.append(task.result())

        tasks = list(pending)
        elapsed = asyncio.get_running_loop().time() - start_time
        remaining_time = total_timeout - elapsed
        print(remaining_time)

    for task in tasks:
        task.cancel()

    return results
