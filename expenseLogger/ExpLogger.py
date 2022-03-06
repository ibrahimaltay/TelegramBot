import datetime
import csv
import os

class ExpLogger:

    def write_expense_row(ExpenseString):

        ExpLogger.create_expense_sheet_if_not_exists()

        expense_array = ExpenseString.split(',')
        tarih = ExpLogger.get_current_date()
        cins = expense_array[0]
        kdv1= ""
        kdv8 = ""
        kdv18 = ""
        toplam = expense_array[2]

        if expense_array[1] == '1':
            kdv1 = "1"
        elif expense_array[1] == '8':
            kdv8 = "8"
        elif expense_array[1] == "18":
            kdv18 = "18"
        else:
            raise ValueError('Vergi miktari 1, 8 veya 18 olmali.')
            

        rowToAppend = [tarih, cins, kdv1, kdv8, kdv18, toplam]

        filename = ExpLogger.get_expense_sheet_name()
        with open(filename, 'a', encoding='UTF8') as f:
            writer = csv.writer(f)

             # write the header
            writer.writerow(rowToAppend)


        expense_dict = {
        "tarih": ExpLogger.get_current_date(), 
        "cinsi": "",
        "%1 kdv": "",
        "%8 kdv" : "",
        "%18 kdv": "",
        "toplam": ""
        }
        
    def get_current_date():
        return datetime.datetime.today().strftime('%d.%m.%Y')

    def get_current_month():
        return datetime.datetime.now().month

    def get_current_year():
        return datetime.datetime.now().year   

    def create_expense_sheet_if_not_exists():
        if not ExpLogger.expense_sheet_exists():
            ExpLogger.create_expense_sheet()

    def expense_sheet_exists():
        expected_filename = ExpLogger.get_expense_sheet_name()
        return expected_filename in os.listdir()

    def get_expense_sheet_name():
        return f"{ExpLogger.get_current_month()}_{ExpLogger.get_current_year()}_expenses.csv"

    def create_expense_sheet():
        filename = ExpLogger.get_expense_sheet_name()
        header = [
        "tarih", 
        "cinsi",
        "%1 kdv",
        "%8 kdv" ,
        "%18 kdv",
        "toplam"
        ]

        with open(filename, 'w', encoding='UTF8') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)


if __name__ == "__main__":
    exp = "yiyecek,18,240"
    ExpLogger.write_expense_row(exp)
    print('done')
    