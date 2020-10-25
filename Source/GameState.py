class BaseState:
    def constructor(self):
        pass

    def destructor(self):
        pass

    # Return False means no event will pass to the lower state
    def eventHandling(self, events) -> bool:
        print("Event handled")
        return True

    # Return True means to pop the state
    def requestPopState(self):
        return False

    # Return None to do nothing or an inheritance of BaseState to push
    def requestPushState(self):
        return None

    # Return False means not to update the lower state
    def update(self, deltaTime: float) -> bool:
        return True

    def lateUpdate(self, deltaTime: float):
        pass

    def render(self):
        pass