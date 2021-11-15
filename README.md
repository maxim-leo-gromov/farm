# farm
Итак, что нужно сделать.

1. Для начала, на всякий случай, установить pip, пригодится:

sudo apt-get install python3-pip

2. В рабочей директории пользователя по умолчанию (pi) создать директорию farm и туда скачать три файла farm_management.py, farm_config.ini, farm.service

3. Перейти в папочку farm и запустить прогу:

python3 farm_management.py

Никаких ошибок быть не должно. Чуток подождать и прервать программу (ctrl+c). Проверить файл /var/log/system.log В нём должны появиться записи от нашей проги (они помечены словом FARM)

4. Скопировать файл farm.service в папку системных сервисов:

sudo cp farm.service /etc/systemd/system/farm.service

5. Обновить информацию у системного демона (чтобы он увидел наш сервис):

sudo systemctl daemon-reload

6. Пописать наш сервис в автозагрузку:

sudo systemctl enable myscript.service

7. Перезагрузить устройство и убедиться, что наш сервис стартанул (должны появиться свежие записи в system.log)
