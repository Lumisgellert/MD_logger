class SimpleKalman:
    def __init__(self, q=0.01, r=0.1):
        self.Q = q  # Prozessrauschen
        self.R = r  # Messrauschen
        self.x = 0.0
        self.P = 1.0

    def update(self, measurement):
        self.P += self.Q
        K = self.P / (self.P + self.R)
        self.x += K * (measurement - self.x)
        self.P *= (1 - K)
        return self.x
