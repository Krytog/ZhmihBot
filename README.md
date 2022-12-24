# ZhmihBot
Зачем по-умному не быть вторым, если безумно можно быть первым?


The best ZhmihBot in history of this world! You can zhmih faces on your photos right in your telegram without any registrations and sms!

# Установка
Для работы бота необходимы open cv, ImageMagick и aiogram.
Необходим файл bot_config.py, в котором будут определены key, содержащий http api бота, а также memory_mode, о котором будет ниже.


Временные файлы хранятся в ./files/inputs и  ./files/outpts.

# Работа с памятью
Поддерживается два варианта хранения файлов:
1) memory_mode == "discard", вариант для релиза, в нём все файлы будут удаляться автоматически, как только закончится их обработка.
2) memory_mod != "discard", вариант для дебага, в нём все файлы будут сохраняться, удалять их нужно будет вручную. Осторожно, при использовании этого варианта в релизе на сервере может закончиться память.
