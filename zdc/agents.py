from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from zdc.drive_discs import DRIVE_DISCS
from zdc.engines import ENGINES, Engine

if TYPE_CHECKING:
    from collections.abc import Sequence


class Agent:
    def __init__(
        self,
        *,
        hp: float,
        defense: float,
        atk: float,
        impact: float,
        er: float,
        am: float,
        ap: float,
        cr: float,
        cd: float,
        pen: float,
        pen_ratio: float,
        ice_bonus: float = 0.0,
        fire_bonus: float = 0.0,
        ether_bonus: float = 0.0,
        physical_bonus: float = 0.0,
        electric_bonus: float = 0.0,
    ) -> None:
        self.hp = hp
        self.defense = defense
        self.atk = atk
        self.impact = impact
        self.er = er
        self.am = am
        self.ap = ap
        self.cr = cr
        self.cd = cd
        self.pen = pen
        self.pen_ratio = pen_ratio

        self.ice_bonus = ice_bonus
        self.fire_bonus = fire_bonus
        self.ether_bonus = ether_bonus
        self.physical_bonus = physical_bonus
        self.electric_bonus = electric_bonus

        self.basic_atk_dmg = 1.0
        """Basic attack damage multiplier."""
        self.dash_atk_dmg = 1.0
        """Dash attack damage multiplier."""

        self.disc_set_counts: defaultdict[int, int] = defaultdict(int)
        self.engine: Engine | None = None

    def __str__(self) -> str:
        return (
            f"HP: {self.hp}\n"
            f"DEF: {self.defense}\n"
            f"ATK: {self.atk}\n"
            f"Impact: {self.impact}\n"
            f"ER: {self.er}\n"
            f"AM: {self.am}\n"
            f"AP: {self.ap}\n"
            f"Crit Rate: {self.cr*100:.1f}%\n"
            f"Crit DMG: {self.cd*100:.1f}%\n"
            f"PEN: {self.pen}\n"
            f"PEN Ratio: {self.pen_ratio*100:.1f}%\n"
            f"Ice Bonus: {self.ice_bonus*100:.1f}%\n"
            f"Fire Bonus: {self.fire_bonus*100:.1f}%\n"
            f"Ether Bonus: {self.ether_bonus*100:.1f}%\n"
            f"Physical Bonus: {self.physical_bonus*100:.1f}%\n"
            f"Electric Bonus: {self.electric_bonus*100:.1f}%"
        )

    def equip_discs(self, disc_ids: Sequence[int]) -> None:
        for disc_id in disc_ids:
            set_id = disc_id // 100
            self.disc_set_counts[set_id] += 1

    def equip_engine(self, engine_id: int) -> None:
        engine = ENGINES.get(engine_id)
        if engine is None:
            raise ValueError(f"Invalid w-engine ID: {engine_id}")
        self.engine = engine(self)

    def compute_stats(self) -> None:
        for set_id, count in self.disc_set_counts.items():
            if count >= 4:
                disc_cls = DRIVE_DISCS.get(set_id)
                if disc_cls is None:
                    raise ValueError(f"Invalid drive disc set ID: {set_id}")
                disc_cls(self).four_piece()

        if self.engine is not None:
            self.engine.effect()
