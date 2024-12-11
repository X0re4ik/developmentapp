from datetime import datetime
from abc import ABC, abstractmethod
from typing import List, Literal


class Content:
    def __init__(self, name: str, date_reliase: datetime):
        self.name = name
        self.date_reliase = date_reliase


class Series(Content):
    pass


class Movie(Content):
    pass


CONTENT_TYPES = Literal["Series", "Movie"]


class ContentFactory:

    @staticmethod
    def create_content(
        content_type: CONTENT_TYPES, name: str, date_reliase: datetime
    ) -> Content:
        if content_type == "Movie":
            return Movie(name, date_reliase)
        elif content_type == "Series":
            return Series(name, date_reliase)
        else:
            raise ValueError("Ну ты даешь дядь, прям так промазать.....")


class TVSeries:
    def __init__(self, title: str, description: str, rating: int | None = None):
        self.title = title
        self.description = description
        self.rating = rating

        self._series: List[Series] = []

    def add_new_series(self, series: Series) -> None:
        self._series.append(series)

    def update_rating(self, new_value: int):
        self.rating = new_value

    @property
    def count_series(self) -> int:
        return len(self._series)


# Абстрактный класс Наблюдателя
class Observer(ABC):
    """Наблюдатель, которого оповезают о выпуске новой серии сериала"""

    @abstractmethod
    def update(self, tv_series: TVSeries, series: Series) -> None:
        pass


# Абстрактный класс Издателя
class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, tv_series: TVSeries, subject: Series) -> None:
        pass


# Издатель, который управляет подписками
class TVSeriesObserver(Subject):
    def __init__(self, tv_series):
        self.tv_series: TVSeries = tv_series
        self._observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, series: Series) -> None:
        for observer in self._observers:
            observer.update(self.tv_series, series)  # Передаем новый сериал наблюдателю

    def add_new_series(self, series: Series):
        self.tv_series.add_new_series(series)
        self.notify(series)  # Уведомляем наблюдателей о новом сериале


class UserObserver(Observer):

    def __init__(self, first_name: str, age: int):
        self.first_name = first_name
        self.age = age

    def update(self, tv_series: TVSeries, series: Series) -> None:
        print(
            f"{self.first_name}, поздрравляю! У вашего любимого сериала '{tv_series.title}' вышла новая серия {series.name}"
        )


if __name__ == "__main__":

    s1 = ContentFactory.create_content("Series", "Серия 1", datetime.now())
    s2 = ContentFactory.create_content("Series", "Серия 2", datetime.now())
    s3 = ContentFactory.create_content("Series", "Серия 1", datetime.now())

    try:
        ContentFactory.create_content("OnlyFans", "18+", datetime.now())
    except Exception as e:
        print(e)

    user_1 = UserObserver("Антон", 40)
    user_2 = UserObserver("Дима", 26)
    user_3 = UserObserver("Петя", 25)

    tv_series_1 = TVSeries("Папины дочки", "О папах и дочках")
    tv_series_2 = TVSeries("Воронины", "Трешачок")

    tv_series_observer1 = TVSeriesObserver(tv_series_1)
    tv_series_observer2 = TVSeriesObserver(tv_series_2)

    tv_series_observer1.attach(user_1)
    tv_series_observer1.attach(user_2)
    tv_series_observer2.attach(user_3)

    tv_series_observer1.add_new_series(s1)
    tv_series_observer1.add_new_series(s2)
    tv_series_observer2.add_new_series(s3)
