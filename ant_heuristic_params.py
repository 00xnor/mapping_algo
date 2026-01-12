from dataclasses import dataclass
from typing import ClassVar


#------------------------------------------------------------------------------
@dataclass(frozen=True)
class AntHeuristicParams:
  NUMBER_OF_ANTS_PER_ITERATION: ClassVar[int] = 8
  SHOW_PHEROMONE_EVERY_N_ITERATIONS: ClassVar[int] = 10
  MOVING_AVERAGE_WINDOW: ClassVar[int] = 50

  PHERONOME_DEPOSIT: ClassVar[float] = 1.0
  PHERONOME_DEPOSIT_UNIT: ClassVar[str] = 'unit(s)'
  PHERONOME_EVAPORATION_RATE: ClassVar[float] = 0.247 # 1=100%
  PHERONOME_EVAPORATION_UNIT: ClassVar[str] = '%'

  ENERGY_ROUTE_ONE_BYTE: ClassVar[float] = 1.0
  ENERGY_LINK_ONE_BYTE: ClassVar[float] = 1.0
  ENERGY_UNIT: ClassVar[str] = 'fJ'

  @classmethod
  def get_constants_dict(cls) -> dict:
    return {
      attr: getattr(cls, attr)
      for attr in dir(cls)
      if not attr.startswith('_') and not callable(getattr(cls, attr))
    }

