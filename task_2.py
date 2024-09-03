import csv

from django.db import models


class Player(models.Model):
    player_id = models.CharField(max_length=100)


class Level(models.Model):
    title = models.CharField(max_length=100)
    order = models.IntegerField(default=0)


class Prize(models.Model):
    title = models.CharField(max_length=100)  # Добавил max_length, без него будет ошибка


class PlayerLevel(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    completed = models.DateField()
    is_completed = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE, null=True, blank=True)  # Добавил поле prize для учета полученного приза за уровень

    def assign_level_prize(self):
        if not self.is_completed:  # Проверка на то, что уровень был пройден
            return "Level not completed yet."

        if self.prize:  # Проверка на то, что приз еще не был назначен
            return "Prize was already assigned to the player."

        try:
            level_prize = LevelPrize.objects.get(level=self.level)
            self.prize = level_prize.prize
            self.save()
        except LevelPrize.DoesNotExist:   # Проверка на то, что уровень не предполагает приза
            return "No prize for this level."

    @staticmethod
    def create_csv_player_level(filename: str):
        with open(filename, mode='w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['player_id', 'level_title', 'is_completed', 'prize_title'])  # Первая строка - заголовки столбцов

            player_levels = PlayerLevel.objects.all().iterator()  # Все записи в модели

            for player_level in player_levels:
                writer.writerow([
                    player_level.player.player_id,
                    player_level.level.title,
                    "Yes" if player_level.is_completed else "No",
                    player_level.prize.title if player_level.prize else 'No prize'
                ])
        print(f"Данные успешно сохранены в файл {filename}")


class LevelPrize(models.Model):
    level = models.ForeignKey(Level, on_delete=models.CASCADE)
    prize = models.ForeignKey(Prize, on_delete=models.CASCADE)
    received = models.DateField()
