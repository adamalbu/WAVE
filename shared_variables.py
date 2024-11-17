class SharedVariables:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SharedVariables, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.warnEnemies = None
        self.enemies = None
        self.allEnemies = None
        self.gametime = 0
        self.forceMoveTimer = 2000
        self.controls = "WASD"
        self.screen = None
        self.currentScreen = None
        self.dt = 0
        self.isPlayerMoving = False
