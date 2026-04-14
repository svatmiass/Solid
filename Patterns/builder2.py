class Pizza:
    def __init__(self):
        self.size: str = ""
        self.dough: str = ""
        self.sauce: str = ""
        self.cheese: str = ""
        self.toppings: list[str] = []

    def __str__(self) -> str:
        toppings = ', '.join(self.toppings) if self.toppings else 'без топпингов'
        return (
            f"Пицца {self.size} на {self.dough} тесте\n"
            f"Соус: {self.sauce}, Сыр: {self.cheese}\n"
            f"Топпинги: {toppings}"
        )


class PizzaBuilder:
    def __init__(self):
        self._pizza = Pizza()

    def set_size(self, size: str):
        self._pizza.size = size
        return self

    def set_dough(self, dough: str):
        self._pizza.dough = dough
        return self

    def set_sauce(self, sauce: str):
        self._pizza.sauce = sauce
        return self

    def set_cheese(self, cheese: str):
        self._pizza.cheese = cheese
        return self

    def add_topping(self, topping: str):
        self._pizza.toppings.append(topping)
        return self

    def build(self) -> Pizza:
        if not self._pizza.size:
            raise ValueError("Размер пиццы не указан")
        if not self._pizza.dough:
            raise ValueError("Тип теста не указан")
        return self._pizza


class Director:
    def __init__(self, builder: PizzaBuilder):
        self._builder = builder

    def build_margherita(self) -> Pizza:
        return (
            self._builder
            .set_size("L")
            .set_dough("традиционное")
            .set_sauce("томатный")
            .set_cheese("моцарелла")
            .build()
        )

    def build_pepperoni(self) -> Pizza:
        return (
            self._builder
            .set_size("XL")
            .set_dough("тонкое")
            .set_sauce("томатный")
            .set_cheese("моцарелла")
            .add_topping("пепперони")
            .build()
        )

    def build_vegetarian(self) -> Pizza:
        return (
            self._builder
            .set_size("M")
            .set_dough("пышное")
            .set_sauce("песто")
            .set_cheese("пармезан")
            .add_topping("грибы")
            .add_topping("перец")
            .add_topping("оливки")
            .build()
        )