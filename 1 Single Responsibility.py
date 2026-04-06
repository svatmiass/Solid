import json
from dataclasses import dataclass
from typing import List, Protocol, Optional
from pathlib import Path

@dataclass
class Order:
    id: str
    price: float
    qty: int
    customer_email: str

    @property
    def total(self) -> float:
        return self.price * self.qty

class OrderLoader:
    def load(self, file_path: str) -> List[Order]:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        orders = []
        for item in data:
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

class OrderCalculator:
    @staticmethod
    def total_amount(orders: List[Order]) -> float:
        return sum(o.total for o in orders)
    
    @staticmethod
    def summary(orders: List[Order]) -> dict:
        return {
            'count': len(orders),
            'total': sum(o.total for o in orders)
        }

class ReportFormatter:
    @staticmethod
    def format(orders: List[Order], stats: dict) -> str:
        lines = [
            f"Orders count: {stats['count']}",
            f"Total amount: ${stats['total']:.2f}",
            "-" * 30
        ]
        
        if stats['count'] <= 10:
            for o in orders:
                lines.append(f"  {o.id}: {o.qty}x${o.price:.2f} = ${o.total:.2f}")
        
        return "\n".join(lines)

class EmailSender(Protocol):
    def send(self, to: str, subject: str, body: str) -> bool:
        ...

class ConsoleSender:
    def send(self, to: str, subject: str, body: str) -> bool:
        print(f"\n📧 To: {to}")
        print(f"📌 Subject: {subject}")
        print(f"{body}\n")
        return True

class NoopSender:
    def send(self, to: str, subject: str, body: str) -> bool:
        return True

class OrderReportService:
    def __init__(self, loader: OrderLoader, calculator: OrderCalculator, 
                 formatter: ReportFormatter, sender: Optional[EmailSender] = None):
        self.loader = loader
        self.calculator = calculator
        self.formatter = formatter
        self.sender = sender
    
    def generate(self, source: str) -> str:
        orders = self.loader.load(source)
        stats = self.calculator.summary(orders)
        return self.formatter.format(orders, stats)
    
    def generate_and_send(self, source: str) -> str:
        orders = self.loader.load(source)
        stats = self.calculator.summary(orders)
        report = self.formatter.format(orders, stats)
        
        if self.sender:
            for order in orders:
                self.sender.send(
                    order.customer_email,
                    f"Order report #{order.id}",
                    report
                )
        
        return report

def create_service(with_email: bool = True) -> OrderReportService:
    return OrderReportService(
        loader=OrderLoader(),
        calculator=OrderCalculator(),
        formatter=ReportFormatter(),
        sender=ConsoleSender() if with_email else None
    )