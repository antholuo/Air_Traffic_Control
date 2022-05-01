import math                         # needed for lat/lon calculations
from __future__ import annotations  # allows forward declarations
from abc import ABC, abstractmethod # not sure what this does

class Plane:
    _state = None

    def __init__(self, state: State) -> None:
        self.setState(state)

    def setState(self, state: State) -> None:
        self._state = state
        self._state.plane = self

    def getState(self) -> str:
        print(f"Elevator is in {type(self._state).__name__}")
        return self._state
    # ------------------------------
    # interface methods begin here
    # ------------------------------
    def updateHeading(self, heading: float) -> None: # not sure how to get return values
        pass

    def hold(self, center: (float, float), radius: int) -> None: # not sure how to get return values
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