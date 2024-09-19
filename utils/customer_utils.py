import random
import string

def generate_post_code():
    """
    Генерирует Post Code из 10 цифр.
    """
    return ''.join(random.choices(string.digits, k=10))

def generate_first_name(post_code):
    """
    Генерирует First Name на основе Post Code. Каждые две цифры преобразуются в буквы алфавита.
    """
    first_name = ''
    for i in range(0, len(post_code), 2):
        # Берем две цифры и преобразуем их в число
        num = int(post_code[i:i+2])
        # Преобразуем это число в букву (0 = a, 25 = z, и т.д.)
        letter = chr((num % 26) + ord('a'))
        first_name += letter
    return first_name
