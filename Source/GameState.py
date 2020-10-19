class BaseState:
    def constructor(self):
        pass

    def destructor(self):
        pass

    # Return False means no event will pass to the lower state
    def eventHandling(self, events) -> bool:
        return True

    # Return False means to end the state
    def update(self, deltaTime: float) -> bool:
        return True

    def lateUpdate(self, deltaTime: float):
        pass

    # Return False means not to render the lower state
    def draw(self) -> bool:
        return True