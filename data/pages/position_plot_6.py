from datetime import datetime

from pydantic import BaseModel

from data.contracts import amms, collaterals, controllers
from data.utils.utils import await_awaitable, get_block_info


class EventList(BaseModel):
    x: list[datetime]
    y: list[float]
    text: list[str]


class Position(BaseModel):
    times: list[datetime]
    losses: list[float]
    prices: list[float]
    healths: list[float]
    events: EventList

    soft_liquidation: list[list[datetime]]  # points of soft liquidation
    hard_liquidation: list[list[datetime]]  # points of hard liquidation


async def async_get_position_plot(col_addr: str, user: str, start_block: int, number_of_points: int) -> Position:
    amm = amms[col_addr]
    controller = controllers[col_addr]
    collateral = collaterals[col_addr]

    start_block, start_block_time = get_block_info(start_block)
    end_block, end_block_time = get_block_info("latest")
    # This is to reduce number of web3 calls, approximate
    time_per_block = (end_block_time - start_block_time) / (end_block - start_block)

    points = list(range(start_block, end_block, (end_block - start_block) // number_of_points))

    borrow_events_bns = [e["blockNumber"] for e in controller.get_borrow_events(start_block, end_block, user)]
    repay_events_bns = [e["blockNumber"] for e in controller.get_repay_events(start_block, end_block, user)]
    remove_collateral_events_bns = [
        e["blockNumber"] for e in controller.get_remove_collateral_events(start_block, end_block, user)
    ]
    liquidate_events_bns = [e["blockNumber"] for e in controller.get_liquidate_events(start_block, end_block, user)]

    position_change_events = [*borrow_events_bns, *repay_events_bns, *remove_collateral_events_bns]
    points.extend(position_change_events)
    points.extend([e - 1 for e in position_change_events])
    points = sorted(set(points))

    times = []
    losses = []
    prices = []
    healths = []
    soft_liquidation = []
    hard_liquidation = []
    current_soft_start = None
    current_hard_start = None
    borrow_events = EventList(x=[], y=[], text=[])
    repay_events = EventList(x=[], y=[], text=[])
    remove_collateral_events = EventList(x=[], y=[], text=[])
    liquidate_events = EventList(x=[], y=[], text=[])

    debt = 0
    old_h = 0
    nh = 0
    old_n1 = 2**256 - 1
    old_n2 = 2**256 - 1

    for point in points:
        h = await controller.async_user_health(user, False, block_identifier=point)
        user_state = await controller.async_user_state(user, block_identifier=point)
        n1, n2 = await amm.async_read_user_tick_numbers(user, block_identifier=point)
        price = (await amm.async_price_oracle(block_identifier=point)) / collateral.precision

        prices.append(price)
        healths.append(h)

        if debt == 0 or abs(user_state[2] - debt) / debt > 0.001 or n1 != old_n1 or n2 != old_n2:
            # If we repaid here - don't include this step (whether it's up or down) in the loss
            old_h = h
            old_n1 = n1
            old_n2 = n2

        debt = user_state[2]
        nh += old_h - h
        old_h = h
        time = datetime.fromtimestamp(start_block_time + (point - start_block) * time_per_block)
        times.append(time)
        losses.append(nh)

        if user_state[1] > 0:
            if not current_soft_start:
                current_soft_start = time
        else:
            if current_soft_start:
                soft_liquidation.append([current_soft_start, time])
                current_soft_start = None

        if h < 0:
            if not current_hard_start:
                current_hard_start = time
        else:
            if current_hard_start:
                hard_liquidation.append([current_hard_start, time])
                current_hard_start = None

        if point in borrow_events_bns:
            borrow_events.x.append(time)
            borrow_events.y.append(nh)
            borrow_events.text.append("Borrow")
        if point in remove_collateral_events_bns:
            remove_collateral_events.x.append(time)
            remove_collateral_events.y.append(nh)
            remove_collateral_events.text.append("Remove Collateral")
        if point in liquidate_events_bns:
            liquidate_events.x.append(time)
            liquidate_events.y.append(nh)
            liquidate_events.text.append("Liquidate")
        # if it's not Liquidate, add Repay - Liquidate is emitted with Repay
        elif point in repay_events_bns:
            repay_events.x.append(time)
            repay_events.y.append(nh)
            repay_events.text.append("Repay")

    if current_soft_start:
        soft_liquidation.append([current_soft_start, time])
    if current_hard_start:
        hard_liquidation.append([current_hard_start, time])

    return Position(
        times=times,
        losses=losses,
        prices=prices,
        healths=healths,
        soft_liquidation=soft_liquidation,
        hard_liquidation=hard_liquidation,
        events=EventList(
            x=[*borrow_events.x, *repay_events.x, *remove_collateral_events.x, *liquidate_events.x],
            y=[*borrow_events.y, *repay_events.y, *remove_collateral_events.y, *liquidate_events.y],
            text=[*borrow_events.text, *repay_events.text, *remove_collateral_events.text, *liquidate_events.text],
        ),
    )


def get_position_plot(col_addr: str, user: str, start_block: int, number_of_points: int) -> Position:
    return await_awaitable(async_get_position_plot(col_addr, user, start_block, number_of_points))
