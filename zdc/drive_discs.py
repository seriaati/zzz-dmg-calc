from __future__ import annotations

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from zdc.agents import Agent


class DriveDisc:
    def __init__(self, agent: Agent) -> None:
        self.agent = agent
        self.conds: dict[str, bool] = {}
        self.stacks: dict[str, int] = {}

    @property
    def set_id(self) -> int:
        raise NotImplementedError

    def four_piece(self) -> None:
        pass


class WoodPeckerElectro(DriveDisc):
    """Woodpecker Electro."""

    def __init__(self, agent: Agent) -> None:
        super().__init__(agent)
        self.conds = {
            "woodpecker_atk_increase": False,
        }

    @property
    def set_id(self) -> int:
        return 310

    def four_piece(self) -> None:
        """
        Landing a critical hit on an enemy with a Basic Attack, Dodge Counter,
        or EX Special Attack increases the equipper's ATK by 9% for 6s.
        The buff duration for different skills are calculated separately.
        """

        if self.conds["woodpecker_atk_increase"]:
            self.agent.atk *= 1.09


class PolarMetal(DriveDisc):
    """Polar Metal."""

    def __init__(self, agent: Agent) -> None:
        super().__init__(agent)
        self.conds = {
            "polar_metal_freeze_or_shatter": False,
        }

    @property
    def set_id(self) -> int:
        return 325

    def four_piece(self) -> None:
        """
        Increase the DMG of Basic Attack and Dash Attack by 20%.
        When any squad member inflicts Freeze or Shatter,
        this effect increases by an additional 20% for 12s.
        """

        self.agent.basic_atk_dmg += 0.2
        self.agent.dash_atk_dmg += 0.2
        if self.conds["polar_metal_freeze_or_shatter"]:
            self.agent.basic_atk_dmg += 0.2
            self.agent.dash_atk_dmg += 0.2


class BranchBladeSong(DriveDisc):
    """Branch & Blade Song."""

    def __init__(self, agent: Agent) -> None:
        super().__init__(agent)
        self.conds = {
            "branch_blade_song_cr_increase": False,
        }

    @property
    def set_id(self) -> int:
        return 327

    def four_piece(self) -> None:
        """
        When Anomaly Mastery exceeds or equals 115 points, the equipper's CRIT DMG increases by 30%.
        When any squad member applies Freeze or triggers the Shatter effect on an enemy,
        the equipper's CRIT Rate increases by 12%, lasting 15s.
        """

        if self.agent.am >= 115:
            self.agent.cd += 0.3
        if self.conds["branch_blade_song_cr_increase"]:
            self.agent.cr += 0.12


DRIVE_DISCS: Final[dict[int, type[DriveDisc]]] = {
    310: WoodPeckerElectro,
    325: PolarMetal,
    327: BranchBladeSong,
}
