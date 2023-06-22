from datetime import datetime

from data.contracts import price_aggregator
from data.utils.utils import await_awaitable, get_block_info


async def async_get_prices(start_block: int, number_of_points: int) -> (list[datetime], list[float]):
    start_block, start_block_time = get_block_info(start_block)
    end_block, end_block_time = get_block_info("latest")
    # This is to reduce number of web3 calls, approximate
    time_per_block = (end_block_time - start_block_time) / (end_block - start_block)

    points = list(range(start_block, end_block, (end_block - start_block) // number_of_points))

    times = []
    prices = []
    for point in points:
        price = await price_aggregator.async_price(point)

        times.append(datetime.fromtimestamp(start_block_time + (point - start_block) * time_per_block))
        prices.append(price)

    return times, prices


def get_prices(start_block: int, number_of_points: int) -> (list[datetime], list[float]):
    return await_awaitable(async_get_prices(start_block, number_of_points))
