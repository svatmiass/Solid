from abc import ABC, abstractmethod

class Notifier(ABC):
    @abstractmethod
    def send(self, to: str, text: str) -> None:
        pass

class EmailClient(Notifier):
    def send(self, to: str, text: str) -> None:
        print(f"[EMAIL to={to}] {text}")

class SmsClient(Notifier):
    def send(self, to: str, text: str) -> None:
        print(f"[SMS to={to}] {text}")

class PushNotifier(Notifier):
    def send(self, to: str, text: str) -> None:
        print(f"[PUSH to={to}] {text}")

class FakeNotifier(Notifier):
    def send(self, to: str, text: str) -> None:
        pass

class NotificationService:
    def __init__(self, email_notifier: Notifier, sms_notifier: Notifier):
        self.email_notifier = email_notifier
        self.sms_notifier = sms_notifier
    
    def notify(self, user_email: str, user_phone: str, text: str) -> None:
        self.email_notifier.send(user_email, text)
        self.sms_notifier.send(user_phone, text)