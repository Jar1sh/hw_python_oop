from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    TEXT_MESSAGE = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.'
                    )

    def get_message(self) -> str:
        """Текст сообщения, выводимый на дисплей"""
        return self.TEXT_MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        distance = self.get_distance()
        speed = self.get_mean_speed()
        calories = self.get_spent_calories()
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           distance,
                           speed,
                           calories
                           )


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SPEED_MULTIPLIER_1: float = 0.035
    SPEED_MULTIPLIER_2: float = 0.029
    SPEED_K1: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action,
                         duration,
                         weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()
        speed_in_ms = mean_speed * self.SPEED_K1
        height_in_m = self.height / self.CM_IN_M
        duration_in_min = self.duration * self.MIN_IN_HOUR
        return ((self.SPEED_MULTIPLIER_1 * self.weight
                + ((speed_in_ms**2 / height_in_m))
                * (self.SPEED_MULTIPLIER_2 * self.weight))
                * (duration_in_min))


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    SPEED_MULTIPLIER_K1: float = 1.1
    SPEED_MULTIPLIER_K2: int = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ):
        super().__init__(action,
                         duration,
                         weight
                         )
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_spent_calories(self) -> float:
        mean_speed = self.get_mean_speed()
        return ((mean_speed
                + self.SPEED_MULTIPLIER_K1)
                * self.SPEED_MULTIPLIER_K2
                * self.weight
                * self.duration)

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)


workout_type_traning = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_type = workout_type_traning[workout_type]
    if workout_type not in workout_type_traning:
        raise Exception('Неизвестный тип')
    return class_type(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
