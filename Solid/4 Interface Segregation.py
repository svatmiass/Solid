from abc import ABC, abstractmethod

class Printable(ABC):
    @abstractmethod
    def print(self, text: str) -> None: ...

class Scannable(ABC):
    @abstractmethod
    def scan(self) -> str: ...

class Faxable(ABC):
    @abstractmethod
    def fax(self, number: str) -> None: ...

class Copiable(ABC):
    @abstractmethod
    def copy(self) -> None: ...

class SimplePrinter(Printable):
    def print(self, text: str) -> None:
        print(text)

class MultiFunctionMachine(Printable, Scannable, Faxable, Copiable):
    def print(self, text: str) -> None:
        print(text)

    def scan(self) -> str:
        return "Scanned content"

    def fax(self, number: str) -> None:
        print(f"Faxing to {number}")

    def copy(self) -> None:
        print("Copying")

def print_document(printer: Printable, text: str) -> None:
    printer.print(text)