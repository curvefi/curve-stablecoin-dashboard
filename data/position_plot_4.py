from datetime import datetime

from .contracts import amms, collaterals, controllers
from .utils import get_block_info


def get_collaterals() -> dict:
    return {col.symbol: col_addr for col_addr, col in collaterals.items()}


def get_position_plot(col_addr: str, user: str, start_block: int, number_of_points: int) -> (list, list):
    amm = amms[col_addr]
    controller = controllers[col_addr]
    start_block, start_block_time = get_block_info(start_block)
    end_block, end_block_time = get_block_info("latest")
    time_per_block = (end_block_time - start_block_time) / (end_block - start_block)

    points = list(range(start_block, end_block, (end_block - start_block) // number_of_points))

    position_change_events = controller.get_position_change_evens(start_block, end_block)
    points.extend([e["blockNumber"] for e in position_change_events])
    points.extend([e["blockNumber"] - 1 for e in position_change_events])
    points = sorted(set(points))

    times = []
    losses = []

    debt = 0
    old_h = 0
    nh = 0
    old_n1 = 2**256 - 1
    old_n2 = 2**256 - 1

    for point in points:
        h = controller.user_health(user, False, block_identifier=point)
        new_debt = controller.user_debt(user, block_identifier=point)
        n1, n2 = amm.read_user_tick_numbers(user)

        if debt == 0 or abs(new_debt - debt) / debt > 0.001 or n1 != old_n1 or n2 != old_n2:
            # If we repaid here - don't include this step (whether it's up or down) in the loss
            old_h = h
            old_n1 = n1
            old_n2 = n2

        debt = new_debt
        nh += old_h - h
        old_h = h
        times.append(datetime.fromtimestamp(start_block_time + (point - start_block) * time_per_block))
        losses.append(nh)

    return times, losses
