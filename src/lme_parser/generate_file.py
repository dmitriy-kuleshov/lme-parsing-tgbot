import openpyxl
from io import BytesIO

def generate_excel(historical_data, filename):
    workbook = openpyxl.Workbook()
    sheet = workbook.active

    # Заголовки таблицы
    sheet["B7"] = "Date"
    sheet["C7"] = "CASH"
    sheet["C8"] = "Buyer"
    sheet["D8"] = "Seller"
    sheet["E8"] = "Mean"

    sheet["F7"] = "3-month"
    sheet["F8"] = "Buyer"
    sheet["G8"] = "Seller"
    sheet["H8"] = "Mean"

    # Функция для безопасного преобразования в float
    def safe_float(value):
        try:
            return float(value)
        except (ValueError, TypeError):
            return value

    # Заполнение данными
    for row, (date, value) in enumerate(historical_data.get(0).items(), start=9):
        sheet[f"B{row}"] = date  # Дата (оставляем в текстовом формате)
        cell = sheet[f"C{row}"]
        cell.value = safe_float(value)  # Число
        cell.number_format = '0.00'  # Устанавливаем формат как числовой с 2 знаками после запятой

    for row, value in enumerate(historical_data.get(1).values(), start=9):
        cell = sheet[f"D{row}"]
        cell.value = safe_float(value)
        cell.number_format = '0.00'

    for row, value in enumerate(historical_data.get(2).values(), start=9):
        cell = sheet[f"F{row}"]
        cell.value = safe_float(value)
        cell.number_format = '0.00'

    for row, value in enumerate(historical_data.get(3).values(), start=9):
        cell = sheet[f"G{row}"]
        cell.value = safe_float(value)
        cell.number_format = '0.00'

    # Сохранение в BytesIO
    excel_file = BytesIO()
    workbook.save(excel_file)
    excel_file.seek(0)

    return excel_file


# if __name__ == "__main__":
#     # Генерация Excel-файлов
#     excel_file = generate_excel(aluminium_historical.historical_data, "aluminium_output.xlsx")
#     generate_excel(copper_historical.historical_data, "copper_output.xlsx")
#     generate_excel(nickel_historical.historical_data, "nickel_output.xlsx")
#     generate_excel(zinc_historical.historical_data, "zinc_output.xlsx")
#     generate_excel(tin_historical.historical_data, "tin_output.xlsx")
#     generate_excel(lead_historical.historical_data, "lead_output.xlsx")
#
# print("Файлы '.xlsx' успешно созданы и сохранены на диск.")
