"""Прежде чем работать с пакетом, интерпретатор считывает содержимое файла __init__.py. Этим можно воспользоваться: 
в файле __init__.py «сообщим» интерпретатору о модели Reservation до того, как он приступит к выполнению кода."""
from .meeting_room import MeetingRoom
from .reservation import Reservation 