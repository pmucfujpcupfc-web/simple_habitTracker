from datetime import datetime
import os
import shutil
import sys
import json
def save_habits():
    """
    Сохраняет текущие привычки в формате .JSON
    """
    with open("habits.json", "w", encoding="utf-8") as file:
        json.dump(habits, file, ensure_ascii=False, indent=4)
if os.name == 'nt':
    """
    Получает ввод клавиш от пользователся без подтверждения
    при помощи ENTER,если пользователь использует WINDOWS
    """
    import msvcrt
    def get_key():
        return msvcrt.getch().decode('utf-8').lower()
else:
    """
    Получает ввод клавиш от пользователся без подтверждения
    при помощи ENTER,если пользователь использует UNIX-подобные системы
    """
    import tty
    import termios
    def get_key():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return key.lower()
    
if getattr(sys, 'frozen', False):
    """
    Строит путь к файлу
    если это .exe файл
    """
    base_path = os.path.dirname(sys.executable)
else:
    """
    Строит путь к файлу
    если это .py файл
    """
    base_path = os.path.dirname(__file__)

filename = os.path.join(base_path, "habits.json") #путь к файлу в формате .json с привычками с зависимостью от ОС 
habits = [] #глобальная переменная для хранения всех привычек

def load_habits():
    """
    Загружает данные из JSON 
    Если сталкивается с ошибкой или с отсутвием файла,то пересоздает файл
    """
    global habits
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        try:
            with open(filename, "r", encoding="utf-8") as f:
                habits = json.load(f)
        except json.JSONDecodeError:
            print("Ошибка при чтении данных.Создан новый файл.")
            habits = []
    else:
        print("Файл не найден. Создан новый.")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(habits, f, ensure_ascii=False, indent=4)

def print_centered_title(title: str):
    """
    Функция для центрирования текста в терминале в зависимости от размера окна
    TITLE - является текстом заголовка передаваемым в функцию
    """
    columns = shutil.get_terminal_size().columns
    print(title.center(columns))
def clear_console():
    """
    Очищает консоль в зависимости от ОС пользователя
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def add_new_habbit():
    """
    Добавляет новыу привычку в формате: "text":"Привычка","created": "дата создания"
    """
    clear_console()
    print_centered_title("РЕЖИМ ДОБАВЛЕНИЯ")
    s = input("Введите новую привычку: \n")
    habits.append({
        'text':s,
        'created':datetime.now().strftime("%Y-%m-%d %H:%M")

    })
    save_habits()
    clear_console()
    main_menu()

def main_menu():
    """
    Показывает текущее состояние списка привычек и
    предлагает пользователю действия (добавить, удалить, редактировать).
    """
    print_centered_title("HABIT TRACKER v1.0.0") 
    print("\n Привычки сейчас:")
    if not habits:
        print("<Сейчас тут пусто,добавьте вашу привычку>")
    else:
        for i, habit in enumerate(habits, 1):
                print(f"{i}. {habit['text']} (добавлено: {habit['created']})")
        print()
    
    print("\n Нажмите 'r' чтобы добавить новую привычку,нажмите 's' для удаления или 'd' для редактирования: ")

    while True:
        key = get_key()
        if key == 's':
            delete_habit()
            break
        elif key == 'd':
            edit_habit()
            break
        elif key == 'r':
            add_new_habbit()
        else:
            print(f"Игнорируется: {key}")
    
def delete_habit():
    """
    Удаления привычки из списка и файла при помощи ввода номера привычки,
    так же перед удалениием от пользователся запрашивается подтверждение
    """
    clear_console()
    print_centered_title("РЕЖИМ УДАЛЕНИЯ")
    for i,habit in enumerate(habits, 1):
                print(f"{i}. {habit['text']} (добавлено: {habit['created']})")
    print()
    try:
        num = int(input("Введите номер для удаления: "))
        if 1<= num <= len(habits):
            clear_console()
            selected = habits[num-1]
            no_or_yes = input(f"Вы точно желаете удалить привычку: {selected['text']}?\n(Введите 'n' чтобы отменить и 'y' для потверждения) ")
            if no_or_yes == "y":
                habits.pop(num-1)
                save_habits()
                print("\n Изменение созраненно!")
            if no_or_yes == "n":
                delete_habit()
            user_choise = input("Чтобы вернуться в главное меню введите 'end',чтобы продолжить редактирование введите 'edit': ")
            if user_choise == 'end':
                clear_console()
                main_menu()
            if user_choise == 'edit':
                delete_habit()
        else:
            input("Введено несуществующие значение.Нажмите ENTER для продолжения...")
            delete_habit()
    except (ValueError,IndexError):
        input("Некорректный ввод! Пожалуйста, введите правильный номер. Нажмите ENTER для повтора...")
        delete_habit()

def edit_habit():
    """
    Позволяет пользователю изменить текст существующей привычки 
    при помощи выбора номера привычки
    """
    clear_console()
    print_centered_title("РЕЖИМ ИЗМЕНЕНИЯ")
    for i, habit in enumerate(habits, 1):
                print(f"{i}. {habit['text']} (добавлено: {habit['created']})")
    print()
    try:
        num = int(input("Введите номер для изменения: "))
        if 1<= num <= len(habits):
            clear_console()
            edited_habit = input(f"Введите новое значение для {habits[num - 1]['text']} \n")
            habits[num - 1]['text'] = edited_habit
            save_habits()
            print("\n Изменение созраненно!")
            user_choise = input("Чтобы вернуться в главное меню введите 'end',чтобы продолжить редактирование введите 'edit': ")
            if user_choise == 'end':
                clear_console()
                main_menu()
            if user_choise == 'edit':
                edit_habit()
        else:
            input("Введено несуществующие значение.Нажмите ENTER для продолжения...")
            edit_habit()
    except (ValueError,IndexError):
        input("Ошибка ввода. Нажмите ENTER для повтора...")
        edit_habit()
    
     

if __name__ == "__main__":
    """
    Первая используется load_habits() для правильного отображения всего списка превычек
    а так же проверки целостности json формата
    """
    load_habits()
    main_menu()





