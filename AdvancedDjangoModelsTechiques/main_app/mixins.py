class RechargeEnergyMixin:
    MAX_ENERGY: int = 100

    def recharge_energy(self: 'Hero', amount: int) -> None:
        self.energy = min(self.energy + amount, 100)
