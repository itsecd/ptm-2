import argparse
import json
import re
import tqdm as t


class Person(object):
    """
        Класс для одной записи с информацией с полями:
        Attributes
        --------
            telephone : string
                Поле для номера телефона
            height : str
                Поле роста
            snils: string
                Снилс
            passport_number : int
                Серия паспорта
            university : str
                Университет
            academic_degree : str
                 Академическая степень
            worldview : str
                Мировоззрение
            address : str
                Адресс
    """
    telephone: str
    height: str
    snils: str
    passport_number: int
    university: str
    age: int
    academic_degree: str
    worldview: str
    address: str

    def __init__(
            self,
            telephone: str = '+7-(000)-000-00-00',
            height: str = "0.00",
            snils: str = '00000000000',
            passport_number: int = 0,
            university: str = 'None',
            age: int = 0,
            academic_degree: str = 'None',
            worldview: str = 'None',
            address: str = 'None') -> None:
        self.telephone = str(telephone)
        self.height = str(height)
        self.snils = str(snils)
        self.passport_number = passport_number
        self.university = str(university)
        self.age = age
        self.academic_degree = str(academic_degree)
        self.worldview = str(worldview)
        self.address = str(address)


class Validator(object):
    collection: list
    valid: int
    invalid: int
    ph_error: int
    ht_error: int
    sn_error: int
    pn_error: int
    un_error: int
    ag_error: int
    ac_error: int
    wv_error: int
    ad_error: int
    """
        Класс-валидатор списка записей,
        который считывает записи из файла и
        проводит их валидацию
        Attributes
        --------
            collection: list
                Контейнер записей типа Person
            valid: int
                Кол-во валидных записей
            invalid: int
                Кол-во невалидных записей
            ph_error: int 
                Кол-во записей с невалидным номером телефона
            ht_error: int
                Кол-во записей с невалидным ростом
            sn_error: int
                Кол-во записей с невалидным снилсом
            pn_error: int
                Кол-во записей с невалидной номером паспорта
            un_error: int
                Кол-во записей с невалидным университетом
            ag_error: int
                Кол-во записей с невалидным возрастом
            ac_error: int
                Кол-во записей с невалидной академической степенью
            wv_error: int
                Кол-во записей с невалидным мировоззрением
            ad_error: int
                Кол-во записей с невалидным адресом

    """

    def __init__(self, collection: list = None) -> None:
        """
        Конструктор класса-валидатора
        Создает контейнер записей
        """
        if not collection:
            self.collection = []
        else:
            self.collection = collection

    def __len__(self) -> int:
        """
        Функция получения размера списка записей
        :return: int - размер списка записей
        """
        return len(self.collection)

    def load(self, path: str = None) -> None:
        """
        Загружает список записей из файла
        :param path: str - путь к файлу
        :return: None
        """
        self.collection = []
        data = json.load(open(path, encoding='windows-1251'))
        progressbar = t.tqdm(range(len(data)))
        progressbar.set_description('Loading Person\'s data from file')
        for i in progressbar:
            temp = Person(
                data[i]['telephone'],
                data[i]['height'],
                data[i]['snils'],
                data[i]['passport_number'],
                data[i]['university'],
                data[i]['age'],
                data[i]['academic_degree'],
                data[i]['worldview'],
                data[i]['address'])
            self.collection.append(temp)
        print('Done')

    def validate(self) -> list:
        self.ph_error = 0
        self.ht_error = 0
        self.sn_error = 0
        self.pn_error = 0
        self.un_error = 0
        self.ag_error = 0
        self.ac_error = 0
        self.wv_error = 0
        self.ad_error = 0
        self.invalid = 0
        self.valid = len(self)
        valid_list = []

        progressbar = t.tqdm(range(len(self)))
        for i in progressbar:
            ph_match = re.match(
                r'\+7-\(9\d{2}\)-\d{3}-\d{2}-\d{2}',
                self.collection[i].telephone)

            correct_height = re.match(r'([0-2].\d{2})', self.collection[i].height)
            sn_match = re.match(r'^(\d{11})$', self.collection[i].snils)
            if not isinstance(self.collection[i].passport_number, str):
                pn_match = (len(str(self.collection[i].passport_number)) == 6)
            else:
                pn_match = False
            un_match = re.match(
                r'([Уу]ниверситет|[Аа]кадем|[Ии]нститут|им.|[Пп]олитех|([А-Я]{3,}))+(\s|[а-я])',self.collection[i].university)
                # r'^([а-яА-Я]|-| ){3,}$', self.collection[i].university)
            if not isinstance(self.collection[i].age, str):
                correct_age = (self.collection[i].age > 16) and (self.collection[i].age < 100)
            else:
                correct_age = False
            ac_match = re.match(r'(^Кандидат наук$)|(^Доктор наук$)|(^Бакалавр$)|(^Специалист$)|(^Магистр$)', self.collection[i].academic_degree)
            wv_match = re.match(r'^([А-Яа-я]+$)|(^Секулярный гуманизм$)', self.collection[i].worldview)
            ad_match = re.match(r'(^ул\. [А-Яа-я, \s]+ \d+$)|(^ул\. [А-Яа-я, \s]+ \d-[а-я] \d+$)|(Аллея [А-Яа-я, \s]+ \d+$)', self.collection[i].address)
            if ph_match is None:
                self.ph_error += 1
            if correct_height is None:
                self.ht_error += 1
            if sn_match is None:
                self.sn_error += 1
            if pn_match is False:
                self.pn_error += 1
            if un_match is None:
                self.un_error += 1
            if correct_age is False:
                self.ag_error += 1
            if ac_match is None:
                self.ac_error += 1
            if wv_match is None:
                self.wv_error += 1
            if ad_match is None:
                self.ad_error += 1

            if (
                    ph_match is None) or (
                    correct_height is None) or (
                    sn_match is None) or (
                    pn_match is False) or (
                    un_match is None) or (
                    correct_age is False) or (
                    ac_match is None) or (
                    wv_match is None) or (
                    ad_match is None
            ):
                self.invalid += 1
                self.valid -= 1
            else:
                valid_list.append(self.collection[i])

        print('Кол-во невалидных записей: ', self.invalid)
        print('Кол-во валидных записей: ', self.valid)
        print()
        print('Кол-во записей с невалидным номером телефона: ', self.ph_error)
        print('Кол-во записей с невалидным ростом: ', self.ht_error)
        print('Кол-во записей с невалидным снилсом: ', self.sn_error)
        print('Кол-во записей с невалидной номером паспорта: ', self.pn_error)
        print('Кол-во записей с невалидным университетом: ', self.un_error)
        print('Кол-во записей с невалидным возрастом: ', self.ag_error)
        print('Кол-во записей с невалидной академической степенью: ', self.ac_error)
        print('Кол-во записей с невалидным мировоззрением: ', self.wv_error)
        print('Кол-во записей с невалидным адресом: ', self.ad_error)
        return valid_list

def write(path: str, valid_list: list) -> None:

    result_list = []
    result_progressbar = t.tqdm(range(len(valid_list)))
    result_progressbar.set_description('Сохраняем валидные записи')
    for item in result_progressbar:
        temp_dict = {'telephone': valid_list[item].telephone,
                     'height': valid_list[item].height,
                     'snils': valid_list[item].snils,
                     'passport_number': valid_list[item].passport_number,
                     'university': valid_list[item].university,
                     'age': valid_list[item].age,
                     'academic_degree': valid_list[item].academic_degree,
                     'worldview': valid_list[item].worldview,
                     'address': valid_list[item].address}
        result_list.append(temp_dict)

    with open(path, 'w') as v_file:
        json.dump(result_list, v_file, ensure_ascii=False)

parser = argparse.ArgumentParser(description='Paths to input and output files')
parser.add_argument('-i', '--input', type=str, help='Path to the input file')
parser.add_argument('-o', '--output', type=str, help='Path to the output file')

if __name__ == '__main__':
    input_path = 'C:/Users/Admin/Downloads/12.txt'
    output_path = 'valid.txt'
    args = parser.parse_args()
    if args.input is not None:
        input_path = args.input
    if args.output is not None:
        output_path = args.output

    validator = Validator()
    validator.load(input_path)
    valid = validator.validate()
    write(output_path, valid)