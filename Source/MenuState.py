from GameState import *
from PlayGround import *
import pygame
from OpenGL.GL import *
import configuration as cfg
import enum
import PlayState
from Controller import HumanController, MinMaxController

class MenuState(BaseState):
    def __init__(self):
        super().__init__()
        self.screen = None
        self.buttons = None

        self.pushState = None
        self.selfDestroy = False

    def constructor(self):
        self.screen =  pygame.display.set_mode(cfg.displaySize)
        self.constructButtons()

    def requestPushState(self):
        pushState = self.pushState
        self.pushState = None
        return pushState

    def requestPopState(self):
        return self.selfDestroy

    def eventHandling(self, events) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selfDestroy = True

        for button in self.buttons:
            button.eventHandling(events)

        return False

    def update(self, deltaTime: float) -> bool:
        for button in self.buttons:
            button.update(deltaTime)

        return False

    def render(self):
        self.screen.fill(cfg.backgroundColor)

        for button in self.buttons:
            button.draw()

        pygame.display.update()

    def constructButtons(self):
        posX = cfg.displaySize[0] / 2
        posY = cfg.displaySize[1] / 2
        play = Button(self.screen, "Play", (posX, posY - 100), 60)
        guide = Button(self.screen, "Guide", (posX, posY), 60)
        exit = Button(self.screen, "Exit", (posX, posY + 100), 60)

        play.setOnClickedCallback(target=self.playCallback)
        guide.setOnClickedCallback(target=self.guideCallback)
        exit.setOnClickedCallback(target=self.exitCallback)

        self.buttons = [play, guide, exit]

    def buttonClickedCallback(self, playstate):
        self.playState = playstate
        self.pushState = self.playState

    def playCallback(self):
        self.pushState = ModeSelectionState()
        self.selfDestroy = True

    def guideCallback(self):
        self.pushState = GuideState()

    def exitCallback(self):
        self.selfDestroy = True

class ModeSelectionState(BaseState):
    def __init__(self):
        super().__init__()
        self.screen = None
        self.buttons = None

        self.playState = None
        self.pushState = None
        self.selfDestroy = False

    def constructor(self):
        self.screen =  pygame.display.set_mode(cfg.displaySize)
        self.constructButtons()

    def requestPushState(self):
        pushState = self.pushState
        self.pushState = None
        return pushState

    def requestPopState(self):
        return self.selfDestroy

    def eventHandling(self, events) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selfDestroy = True
                    self.pushState = MenuState()

        for button in self.buttons:
            button.eventHandling(events)

        return False

    def update(self, deltaTime: float) -> bool:
        for button in self.buttons:
            button.update(deltaTime)

        return False

    def render(self):
        self.screen.fill(cfg.backgroundColor)

        for button in self.buttons:
            button.draw()

        pygame.display.update()

    def constructButtons(self):
        posX = cfg.displaySize[0] / 2
        posY = cfg.displaySize[1] / 2
        pvp = Button(self.screen, "Person VS Person", (posX, posY - 150), 60)
        pvm = Button(self.screen, "Person VS Machine", (posX, posY - 50), 60)
        mvp = Button(self.screen, "Machine VS Person", (posX, posY + 50), 60)
        mvm = Button(self.screen, "Machine VS Machine", (posX, posY + 150), 60)

        human = HumanController()
        minmax = MinMaxController()
        pvp.setOnClickedCallback(target=self.buttonClickedCallback, args=(PlayState.PlayState(human, human),))
        pvm.setOnClickedCallback(target=self.buttonClickedCallback, args=(PlayState.PlayState(human, minmax),))
        mvp.setOnClickedCallback(target=self.buttonClickedCallback, args=(PlayState.PlayState(minmax, human),))
        mvm.setOnClickedCallback(target=self.buttonClickedCallback, args=(PlayState.PlayState(minmax, minmax),))

        self.buttons = [pvp, pvm, mvp, mvm]


    def buttonClickedCallback(self, playstate):
        self.playState = playstate
        self.pushState = self.playState
        self.selfDestroy = True

class GuideState(BaseState):
    def __init__(self):
        super().__init__()
        self.screen = None
        self.playState = None
        self.selfDestroy = False

        self.guideImage = None
        self.guideImagePos = [0, 0]

    def constructor(self):
        self.screen = pygame.display.set_mode(cfg.displaySize)
        self.guideImage = pygame.image.load(cfg.guideImageFilename)

    def requestPushState(self):
        return None

    def requestPopState(self):
        return self.selfDestroy

    def eventHandling(self, events) -> bool:
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selfDestroy = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: self.guideImagePos[1] += cfg.guideScrollAmount
                elif event.button == 5: self.guideImagePos[1] -= cfg.guideScrollAmount

        return False

    def update(self, deltaTime: float) -> bool:
        if self.guideImage:
            self.guideImagePos[1] = min(0, self.guideImagePos[1])
            self.guideImagePos[1] = max(cfg.displaySize[1] - self.guideImage.get_size()[1], self.guideImagePos[1])

        return False

    def render(self):
        self.screen.fill(cfg.backgroundColor)

        if self.guideImage:
            self.screen.blit(self.guideImage, self.guideImagePos)

        pygame.display.update()

class Button:
    def __init__(self, screen, text, pos, fontSize,
                 color=cfg.mainmenuTextColor,
                 hoveredColor=cfg.mainmenuTextColorHovered,
                 clickedColor=cfg.mainmenuTextColorClicked):
        self.screen = screen
        self.font = pygame.font.SysFont('Corbel', fontSize)
        self.textNormal = self.font.render(text, True, color)
        self.textHovered = self.font.render(text, True, hoveredColor)
        self.textClicked = self.font.render(text, True, clickedColor)
        self.text = self.textNormal
        self.rect = self.text.get_rect()
        self.pos = [pos[0] - self.rect[2] / 2, pos[1] - self.rect[3] / 2]

        self.isClicked = False
        self.isHovered = False

        self.onClickedCallback = None
        self.onClickedArgs = tuple()

    def setOnClickedCallback(self, target, args = tuple()):
        self.onClickedCallback = target
        self.onClickedArgs = args

    def eventHandling(self, events):
        self.isClicked = False

        for event in events:
            if event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.isHovered = self.pos[0] <= pos[0] <= self.pos[0] + self.rect[2] and self.pos[1] <= pos[1] <= self.pos[1] + self.rect[3]
                if self.isHovered:
                    self.text = self.textHovered
                else:
                    self.text = self.textNormal
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.isHovered and event.button == 1:
                    self.text = self.textClicked
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.isClicked = self.isHovered
                    if self.isClicked and self.onClickedCallback:
                        self.onClickedCallback(*self.onClickedArgs)

    def update(self, deltaTime: float):
        pass

    def draw(self):
        self.screen.blit(self.text, self.pos)