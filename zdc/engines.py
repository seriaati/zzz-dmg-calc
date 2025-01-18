from __future__ import annotations

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from zdc.agents import Agent


class Engine:
    def __init__(self, agent: Agent) -> None:
        self.agent = agent
        self.conds: dict[str, bool] = {}
        self.stacks: dict[str, int] = {}

    def effect(self) -> None:
        pass


class HailstormShrine(Engine):
    def __init__(self, agent: Agent) -> None:
        super().__init__(agent)
        self.stacks = {
            "hailstorm_shrine_stacks": 0,
        }

    def effect(self) -> None:
        """
        CRIT DMG increases by 50%.
        When using an EX Special Attack or when any squad member applies an Attribute Anomaly to an enemy,
        the equipper's Ice DMG increases by 20%, stacking up to 2 times and lasting 15s.
        The duration of each stack is calculated separately.
        """

        self.agent.cd += 0.5
        if self.stacks["hailstorm_shrine_stacks"] > 0:
            self.agent.ice_bonus += 0.2 * self.stacks["hailstorm_shrine_stacks"]


ENGINES: Final[dict[int, type[Engine]]] = {
    14109: HailstormShrine,
}
