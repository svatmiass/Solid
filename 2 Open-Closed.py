from dataclasses import dataclass
from abc import ABC, abstractmethod

class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass

class RegularDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total

class VipDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.9

class EmployeeDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.8

@dataclass
class Order:
    total: float

@dataclass
class Customer:
    discount_strategy: DiscountStrategy

def apply_discount(order: Order, customer: Customer) -> float:
    return customer.discount_strategy.apply(order.total)

class BlackFridayDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.5