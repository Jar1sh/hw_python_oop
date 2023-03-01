class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return f'''Тип тренировки: {self.training_type};
                Длительность: {self.duration:.3f} ч.;
                Дистанция: {self.distance:.3f} км;
                Ср. скорость: {self.speed:.3f};
                Потрачено ккал: {self.calories:.3f}.'''


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
        pass

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

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float
                 ):
        super().__init__(action,
                         duration,
                         weight
                         )

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * mean_speed + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    WEIGHT_K1 = 0.035
    WEIGHT_K2 = 0.029
    SPEED_K1 = 0.278
    CM_IN_M = 100

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
        return (self.WEIGHT_K1 * self.weight
                + (speed_in_ms**2 / self.height / self.CM_IN_M)
                * (self.WEIGHT_K2 * self.weight)
                * self.duration)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SPEED_K1 = 1.1
    SPEED_K2 = 2

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
                + self.SPEED_K1)
                * self.SPEED_K2
                * self.weight
                * self.duration)

    def get_mean_speed(self) -> float:
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)


training_codes: dict = {
    'RUN': Running,
    'WLK': SportsWalking,
    'SWM': Swimming,
}


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    class_type = training_codes[workout_type]
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
