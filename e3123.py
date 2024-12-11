from datetime import datetime
from typing import List, Optional
from abc import ABC, abstractmethod


# Класс для представления местоположения
class Location:
    def __init__(self, latitude: float, longitude: float):
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"


# Абстрактный класс Наблюдателя
class Observer(ABC):
    """Наблюдатель, которого оповезают о выпуске новой серии сериала"""

    @abstractmethod
    def notify(self, message) -> None:
        pass


# Класс для представления клиента
class Customer(Observer):
    def __init__(self, customer_name: str, location: Location):
        self.customer_name = customer_name  # Имя клиента
        self.location = location  # Местоположение клиента

    def notify(self, message: str):
        print(f"Клиент {self.customer_name} получил сообщение: {message}")


# Абстрактный класс Издателя
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self) -> None:
        pass


# Класс для представления курьера
class Courier(Subject):
    def __init__(self, courier_name: str, location: Location):
        self.courier_name = courier_name  # Имя курьера
        self.location = location  # Местоположение курьера
        self._observers: List[Observer] = (
            []
        )  # Подписчики на уведомления о статусе доставки

    def attach(self, observer: Observer):
        self._observers.append(observer)  # Добавляем клиента в список наблюдателей

    def detach(self, observer: Observer):
        self._observers.remove(observer)  # Убираем клиента из списка наблюдателей

    def notify(self):
        for observer in self._observers:
            observer.notify(
                f"Курьер {self.courier_name} в точке: {self.location}"
            )  # Уведомляем клиентов

    def move(self, new_location: Location):
        self.location = new_location  # Курьер перемещается
        self.notify()  # Уведомляем клиентов о новом местоположении


# Класс для представления заказа
class Order:
    def __init__(
        self,
        order_id: int,
        customer: Customer,
        delivery_address: Location,
        order_date: datetime,
    ):
        self.order_id = order_id  # Идентификатор заказа
        self.customer = customer  # Клиент
        self.delivery_address = delivery_address  # Местоположение доставки
        self.order_date = order_date  # Дата заказа
        self.status = "Pending"  # Статус заказа (по умолчанию "В ожидании")

    def update_status(self, status: str):
        self.status = status  # Обновление статуса заказа

    def __str__(self):
        return (
            f"Заказ ID: {self.order_id}, Клиент: {self.customer.customer_name}, Статус: {self.status}, "
            f"Время заказа: {self.order_date.strftime('%Y-%m-%d %H:%M:%S')}, Адрес: {self.delivery_address}"
        )


# Фабрика для создания объектов заказов
class OrderFactory:
    @staticmethod
    def create_order(
        order_id: int,
        customer: Customer,
        delivery_address: Location,
        order_date: datetime,
    ) -> Order:
        return Order(order_id, customer, delivery_address, order_date)  # Создаем заказ


# Класс для представления системы доставки
class DeliverySystem:
    def __init__(self):
        self.orders: List[Order] = []  # Список заказов
        self.couriers: List[Courier] = []  # Список курьеров

    def add_order(self, order: Order):
        self.orders.append(order)  # Добавляем заказ в систему

    def add_courier(self, courier: Courier):
        self.couriers.append(courier)  # Добавляем курьера в систему

    def assign_order_to_courier(self, order: Order, courier: Courier):
        # Заказ можно назначить курьеру, и курьер начнет доставку
        courier.attach(order.customer)  # Клиент становится наблюдателем курьера
        order.update_status("Передан курьеру")
        print(f"Заказ {order.order_id} назначен курьеру {courier.courier_name}")

    def update_courier_location(self, courier: Courier, new_location: Location):
        courier.move(new_location)  # Обновляем местоположение курьера


# Реализация конкретного курьера
class FastCourier(Courier):
    def move(self, new_location: Location):
        super().move(new_location)  # Используем метод родительского класса


# Пример использования

if __name__ == "__main__":
    # Создаем клиентов
    customer1 = Customer("Петя", Location(39.747, -75.168))
    customer2 = Customer("Вова", Location(40.712, -74.006))

    # Создаем курьеров
    courier1 = Courier("Скуф", Location(39.747, -75.168))

    # Создаем систему доставки
    delivery_system = DeliverySystem()

    # Создаем заказ через фабрику
    order1 = OrderFactory.create_order(
        1, customer1, Location(40.712, -74.006), datetime.now()
    )

    # Добавляем заказ и курьера в систему
    delivery_system.add_order(order1)
    delivery_system.add_courier(courier1)

    # Назначаем заказ курьеру
    delivery_system.assign_order_to_courier(order1, courier1)

    # Обновляем местоположение курьера
    delivery_system.update_courier_location(courier1, Location(40.730, -73.935))
    delivery_system.update_courier_location(courier1, Location(40.742, -73.929))
