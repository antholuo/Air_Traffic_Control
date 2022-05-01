import math                         # needed for lat/lon calculations
from __future__ import annotations  # allows forward declarations
from abc import ABC, abstractmethod # not sure what this does

class Plane:
    _state = None
    AIRSPEED = 100 # 100m/s CONST
    def __init__(self, state: State, lat = float, lon = float, debug_outputs:bool=False) -> None:
        self.setState(state)
        self.heading = self.getHeadingToCenter(loc)
        self.lat = lat
        self.lon = lon

    def setState(self, state: State) -> None:
        self._state = state
        self._state.plane = self

    def getState(self) -> str:
        print(f"Elevator is in {type(self._state).__name__}")
        return self._state

    def getHeadingToCenter(self, loc: (float, float)) -> float:
        return #heading to center after we figure out lat/lon

    # ------------------------------
    # interface methods begin here
    # ------------------------------
    def updateHeading(self, heading: float) -> None: # not sure how to get return values
        pass

    def hold(self, center: (float, float), radius: int) -> None: # not sure how to get return values
        pass

    def updatePosition(self, delta_seconds: float) -> (float, float, float):
        pass

class State(ABC):
    @property
    def plane(self) -> Plane:
        return self._plane

    @plane.setter
    def plane(self, plane: Plane) -> None:
        self._plane = plane

    @abstractmethod
    def updateHeading(self, heading: float) -> None:
        pass

    @abstractmethod
    def hold(self, center: (float, float), radius: int) -> None:
        pass

    @abstractmethod
    def updatePosition(self, delta_seconds: float) -> (float, float, float):
        pass