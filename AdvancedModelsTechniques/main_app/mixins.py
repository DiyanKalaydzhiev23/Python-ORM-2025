class RechargeEnergyMixin:
    MAX_ENERGY_AMOUNT: int = 100

    def recharge_energy(self, amount: int) -> None:
        self.energy += amount

        if self.energy > self.MAX_ENERGY_AMOUNT:
            self.energy = self.MAX_ENERGY_AMOUNT

        self.save()
