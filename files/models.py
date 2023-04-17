from django.db import models


def report_file_directory_path(instance, filename):
    return f"reports/report_{filename}"


class Report(models.Model):
    """ Модель отчета/выгрузки файлов
    """
    file_url = models.URLField("URL", max_length=500)
    params = models.CharField(
        "Доп параметры", max_length=500, null=True, blank=True
    )
    create_at = models.DateField("Создано", null=True, blank=True)

    def __str__(self):
        return f"{self.file_url}"

    class Meta:
        verbose_name = "Отчет"
        verbose_name_plural = "Отчеты"
        db_table = "reports"
