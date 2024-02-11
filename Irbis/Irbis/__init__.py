from django.conf import settings
import subprocess

# Подгрузка зависимостей в продакшене

if settings.DEBUG == False:
    subprocess.call(['pip', 'install', '-r', 'require.txt'])