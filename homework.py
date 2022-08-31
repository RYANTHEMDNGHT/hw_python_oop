# прошу прощения
# случайно  не то отправил ))


from dataclasses import dataclass, asdict
from statistics import mean
from typing import Sequence, Tuple, List, ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = ('Тип тренировки: {}; '
                              'Длительность: {:.3f} ч.; '
                              'Дистанция: {:.3f} км; '
                              'Ср. скорость: {:.3f} км/ч; '
                              'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:

        return self.MESSAGE.format(*asdict(self).values())


class Training:
    """Базовый класс тренировки."""

    M_IN_KM = 1000
    MIN_IN_HOUR = 60
    LEN_STEP = 0.65

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ):
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self):
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определить get_spent_calories')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories(),
        )


class Running(Training):
    """Тренировка: бег."""

    RUN_MULTIPLY = 18
    RUN_MINUS = 20

    def get_spent_calories(self):
        INTRMDTE_DATA_CCAL = (self.RUN_MULTIPLY
                              * self.get_mean_speed()
                              - self.RUN_MINUS) * self.weight
        duration_in_minutes = self.duration * self.MIN_IN_HOUR

        return INTRMDTE_DATA_CCAL / self.M_IN_KM * duration_in_minutes


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    WEIGH_MULTIPLIER_1 = 0.035
    WEIGH_MULTIPLIER_2 = 0.029

    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self):
        weight_and_coeff_1 = self.WEIGH_MULTIPLIER_1 * self.weight
        weight_and_coeff_2 = self.WEIGH_MULTIPLIER_2 * self.weight
        mean_speed_and_weight = (self.get_mean_speed() ** 2) // self.height
        duration_in_minutes = self.duration * self.MIN_IN_HOUR

        return (weight_and_coeff_1 + mean_speed_and_weight
                * weight_and_coeff_2) * duration_in_minutes


class Swimming(Training):
    """Тренировка: плавание."""

    SWIM_FIRST_COEFF = 1.1
    SWIM_SECOND_COEFF = 2
    LEN_STEP = 1.38

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.cnt_pool = count_pool

    def get_distance(self):
        """расстояние в бассейне."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self):
        """ср. скорость в бассейне."""
        return self.length_pool * self.cnt_pool / self.M_IN_KM / self.duration

    def get_spent_calories(self):
        mean.intrmdteDataCcal = self.get_mean_speed() + self.SWIM_FIRST_COEFF

        return mean.intrmdteDataCcal * self.SWIM_SECOND_COEFF * self.weight


def read_package(workout_type: str, data: Sequence[int]):
    """Прочитать данные полученные от датчиков."""
    TRAINING_PARAMS = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    if workout_type not in TRAINING_PARAMS:
        raise NotImplementedError('Тренировка не найдена')

    return TRAINING_PARAMS[workout_type](*data)


def main(training: Training):
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Sequence[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180])
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
