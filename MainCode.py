import GeneratePDF
import GenerateTable


def main():
    report = input("Введите команду (Вакансии или Статистика): ")
    if report == "Вакансии":
        GenerateTable.generate_table()
    elif report == "Статистика":
        GeneratePDF.generate_pdf()
    else:
        raise NameError('Неизвестная команда')

# first
main()
