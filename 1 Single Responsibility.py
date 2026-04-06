import json
from dataclasses import dataclass
from typing import List, Protocol, Optional
from pathlib import Path

# ========== DOMAIN MODEL ==========
@dataclass
class Order:
    id: str
    price: float
    qty: int
    customer_email: str
    
    @property
    def total(self) -> float:
        return self.price * self.qty


# ========== LOADER ==========
class OrderLoader:
    """Отвечает только за загрузку и валидацию"""
    
    def load(self, file_path: str) -> List[Order]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        orders = []
        for item in data:
            # Валидация
            if not all(k in item for k in ('id', 'price', 'qty', 'email')):
                raise ValueError(f"Missing required fields in {item}")
            if item['qty'] <= 0:
                raise ValueError(f"qty must be positive, got {item['qty']}")
            
            orders.append(Order(
                id=str(item['id']),
                price=float(item['price']),
                qty=int(item['qty']),
                customer_email=item['email']
            ))
        
        return orders


# ========== CALCULATOR ==========
class OrderCalculator:
    """Отвечает только за расчёты"""
    
    @staticmethod
    def total_amount(orders: List[Order]) -> float:
        return sum(o.total for o in orders)
    
    @staticmethod
    def summary(orders: List[Order]) -> dict:
        return {
            'count': len(orders),
            'total': sum(o.total for o in orders)
        }


# ========== FORMATTER ==========
class ReportFormatter:
    """Отвечает только за форматирование"""
    
    @staticmethod
    def format(orders: List[Order], stats: dict) -> str:
        """Меняй этот метод как хочешь — расчёты не пострадают"""
        lines = [
            f"Orders count: {stats['count']}",
            f"Total amount: ${stats['total']:.2f}",
            "-" * 30
        ]
        
        # Детали только если заказов мало
        if stats['count'] <= 10:
            for o in orders:
                lines.append(f"  {o.id}: {o.qty}x${o.price:.2f} = ${o.total:.2f}")
        
        return "\n".join(lines)


# ========== SENDER ==========
class EmailSender(Protocol):
    """Протокол для любого отправителя"""
    def send(self, to: str, subject: str, body: str) -> bool:
        ...


class ConsoleSender:
    """Отправка в консоль (для отладки)"""
    def send(self, to: str, subject: str, body: str) -> bool:
        print(f"\n📧 To: {to}")
        print(f"📌 Subject: {subject}")
        print(f"{body}\n")
        return True


class NoopSender:
    """Заглушка — ничего не отправляет"""
    def send(self, to: str, subject: str, body: str) -> bool:
        return True  # Имитируем успех


# ========== SERVICE ==========
class OrderReportService:
    """Оркестрирует всю работу"""
    
    def __init__(self, loader: OrderLoader, calculator: OrderCalculator, 
                 formatter: ReportFormatter, sender: Optional[EmailSender] = None):
        self.loader = loader
        self.calculator = calculator
        self.formatter = formatter
        self.sender = sender
    
    def generate(self, source: str) -> str:
        """Только генерация отчёта"""
        orders = self.loader.load(source)
        stats = self.calculator.summary(orders)
        return self.formatter.format(orders, stats)
    
    def generate_and_send(self, source: str) -> str:
        """Генерация + отправка (если sender настроен)"""
        report = self.generate(source)
        
        if self.sender:
            orders = self.loader.load(source)
            for order in orders:
                self.sender.send(
                    order.customer_email,
                    f"Order report #{order.id}",
                    report
                )
        
        return report


# ========== CONVENIENCE ==========
def create_service(with_email: bool = True) -> OrderReportService:
    """Фабрика для быстрого создания сервиса"""
    return OrderReportService(
        loader=OrderLoader(),
        calculator=OrderCalculator(),
        formatter=ReportFormatter(),
        sender=ConsoleSender() if with_email else None
    )


# ========== EXAMPLE ==========
if __name__ == "__main__":
    # Тестовые данные
    test_file = "test_orders.json"
    with open(test_file, 'w') as f:
        json.dump([
            {"id": "A1", "price": 100, "qty": 2, "email": "alice@test.com"},
            {"id": "B2", "price": 50.5, "qty": 1, "email": "bob@test.com"}
        ], f)
    
    # Использование 1: с отправкой
    print("=== WITH EMAIL ===")
    service = create_service(with_email=True)
    service.generate_and_send(test_file)
    
    # Использование 2: без отправки
    print("\n=== WITHOUT EMAIL ===")
    service = create_service(with_email=False)
    report = service.generate(test_file)
    print(report)
    
    # Использование 3: другой формат (меняем только форматтер)
    print("\n=== CUSTOM FORMAT ===")
    class UppercaseFormatter(ReportFormatter):
        @staticmethod
        def format(orders, stats):
            return super().format(orders, stats).upper()
    
    custom_service = OrderReportService(
        loader=OrderLoader(),
        calculator=OrderCalculator(),
        formatter=UppercaseFormatter(),
        sender=None
    )
    print(custom_service.generate(test_file))