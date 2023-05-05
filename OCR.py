import pytesseract

from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def text_recognition_tesseract(file_path, text_file_name="result.txt", language="eng"):
    img = Image.open(file_path)

    custom_config = r'--oem 3 --psm 6'
    # модификатор r - означает, что в строке спец. символы по типу \n надо воспринимать просто как символы
    # psm - флаг, означающий как мы будем распозновать текст (режим фрагментации страницы). В данном случае, я поставил блок текста. Можно поставить: картинка как символ, строка, блок текста и тд
    # oem - режим работы, 3 - что доступно, то и используется; 2 - с использованием рекуррентных сетей + legacy

    text = pytesseract.image_to_string(img, config=custom_config, lang=language)
    print(text)

    with open(text_file_name, "w") as file:
        file.write(f"{text}")

    return f"Result wrote into {text_file_name}"
