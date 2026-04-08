from dataclasses import dataclass
from abc import ABC, abstractmethod

# ========== STRATEGY PATTERN ==========

class DiscountStrategy(ABC):
    """Протокол для всех стратегий скидок"""
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


# ========== DOMAIN MODEL ==========

@dataclass
class Order:
    total: float


@dataclass
class Customer:
    discount_strategy: DiscountStrategy


# ========== CALCULATOR ==========

def apply_discount(order: Order, customer: Customer) -> float:
    """Центральный расчёт не меняется при добавлении новых скидок"""
    return customer.discount_strategy.apply(order.total)


# ========== EXAMPLE OF EXTENSION ==========
# Новый тип скидки добавляется отдельным классом без изменения apply_discount

class BlackFridayDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total * 0.5


# ========== USAGE ==========
if __name__ == "__main__":
    order = Order(total=100.0)
    
    regular_customer = Customer(discount_strategy=RegularDiscount())
    vip_customer = Customer(discount_strategy=VipDiscount())
    employee_customer = Customer(discount_strategy=EmployeeDiscount())
    black_friday_customer = Customer(discount_strategy=BlackFridayDiscount())
    
    print(apply_discount(order, regular_customer))      # 100.0
    print(apply_discount(order, vip_customer))          # 90.0
    print(apply_discount(order, employee_customer))     # 80.0
    print(apply_discount(order, black_friday_customer)) # 50.0