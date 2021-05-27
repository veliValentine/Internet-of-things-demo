from logger import Logger


class Personel_Counter:
    def __init__(self):
        self.__person_count = 0

    def __log_person_count(self, description):
        Logger.log(description, self.__str__())

    def enter(self):
        self.__person_count += 1
        print("Person entered the building")
        self.__log_person_count("Person entered")

    def exit(self):
        if self.__person_count > 1:
            self.__person_count -= 1
            print("Person left the building")
            self.__log_person_count("Person left")

    def emergency(self):
        self.__person_count = 0
        print("Emergency")
        self.__log_person_count("Emergency")

    def __str__(self) -> str:
        return f"Persons in building: {self.__person_count}"
