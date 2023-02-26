import random
import matplotlib.pyplot as plt

dict_ru = {}
dict_en = {}
dict_ru_verbs = {}
dict_en_verbs = {}
ru = []
en = []
ru_verbs = []
en_verbs = []


def proverka(d, num, znach):
    global variants
    if variants[num] == d[znach]:
        print("Ответ верен!\n")
        global counter
        counter += 1
    else:
        print("Ответ НЕверен!")
        print("Правильный ответ:", d[znach], "\n")


def isVerb(w):
    if w.find("to ", 0, 3) != -1:
        return True


def generate(d1, en_or_ru1, d2, en_or_ru2):
    global test
    global test_verbs
    global variants
    for i in range(length):
        if random.randint(1, 2) == 1:
            list1 = list(en_or_ru1)
            for j in range(5):
                if j == 0:
                    variants[j] = d1[test[i]]
                    list1.remove(variants[j])
                else:
                    variants[j] = random.choice(list1)
                    list1.remove(variants[j])
            random.shuffle(variants)
            print("Слово:", test[i], "\n1.", variants[0], "\n2.", variants[1], "\n3.", variants[2],
                  "\n4.", variants[3], "\n5.", variants[4], "\n")
            answer = input("Ваш ответ: ")
            if answer == "1":
                proverka(d1, 0, test[i])
            elif answer == "2":
                proverka(d1, 1, test[i])
            elif answer == "3":
                proverka(d1, 2, test[i])
            elif answer == "4":
                proverka(d1, 3, test[i])
            elif answer == "5":
                proverka(d1, 4, test[i])
            else:
                print("Вы указали несуществующий вариант ответа. Ответ не засчитан.")
        else:
            list2 = list(en_or_ru2)
            for j in range(5):
                if j == 0:
                    variants[j] = d2[test_verbs[i]]
                    list2.remove(variants[j])
                else:
                    variants[j] = random.choice(list2)
                    list2.remove(variants[j])
            random.shuffle(variants)
            print("Слово:", test_verbs[i], "\n1.", variants[0], "\n2.", variants[1], "\n3.", variants[2],
                  "\n4.", variants[3], "\n5.", variants[4], "\n")
            answer = input("Ваш ответ: ")
            if answer == "1":
                proverka(d2, 0, test_verbs[i])
            elif answer == "2":
                proverka(d2, 1, test_verbs[i])
            elif answer == "3":
                proverka(d2, 2, test_verbs[i])
            elif answer == "4":
                proverka(d2, 3, test_verbs[i])
            elif answer == "5":
                proverka(d2, 4, test_verbs[i])
            else:
                print("Вы указали несуществующий вариант ответа. Ответ не засчитан.")


# Чтение из файла, заполнение списков и словаря
with open("dictionary.txt", "r") as file:
    for line in file:
        if line != "\n":
            split = line.split(" - ")
            split[1] = split[1].replace("\n", "")
            if isVerb(split[0]):
                en_verbs.append(split[0])
                ru_verbs.append(split[1])
                dict_en_verbs[split[0]] = split[1]
                dict_ru_verbs[split[1]] = split[0]
            else:
                en.append(split[0])
                ru.append(split[1])
                dict_en[split[0]] = split[1]
                dict_ru[split[1]] = split[0]

stats = 0
sessions = 0
length = 25

isOn = True
print("Добро пожаловать в консольную версию программы 'Vocabulary'!\n")

while isOn:
    test = []
    test_verbs = []
    variants = ["", "", "", "", ""]
    mode = input(
        "Пожалуйста, укажите режим (1.Русско-английский 2.Англо-русский 3.Добавить слово 4.Выход из программы): ")
    if mode == "1":
        sessions += 1
        random.shuffle(ru)
        random.shuffle(ru_verbs)
        for i in range(length):
            test.append(ru[i])
            test_verbs.append(ru_verbs[i])
        counter = 0
        generate(dict_ru, en, dict_ru_verbs, en_verbs)
        print("Количество правильных ответов:", counter, "из", length)
        stats += counter
    elif mode == "2":
        sessions += 1
        random.shuffle(en)
        random.shuffle(en_verbs)
        for i in range(length):
            test.append(en[i])
            test_verbs.append(en_verbs[i])
        counter = 0
        generate(dict_en, ru, dict_en_verbs, ru_verbs)
        print("Количество правильных ответов:", counter, "из", length)
        stats += counter
    elif mode == "3":
        new_word = input("Введите новое слово на ангийском: ")
        translate = input("Введите перевод на русском: ")
        if new_word in dict_en or new_word in dict_en_verbs:
            print("Такой элемент уже существует в словаре")
        else:
            with open("dictionary.txt", "a", newline='') as file:
                file.write(f"{new_word} - {translate}\n")
            print("Запись элемента прошла успешно!")
    elif mode == "4":
        print("Работа программы завершена")
        isOn = False
    else:
        print("Режим указан не верно, попробуйте ещё раз")

# Запись процента правильности
if sessions != 0:
    stats = str(((stats / sessions) / length) * 100)
    sample = "Процент правильности ответов: " + stats + "%"
    with open("stats.txt", "a") as stats:
        stats.write(sample + "\n")
    y_axis = []
    x_axis = []
    count = 0
    with open("stats.txt", "r") as stats:
        for line in stats:
            if line == "Статистика:\n":
                continue
            count += 1
            x_axis.append(count)
            split = line.split(": ")
            y_axis.append(float(split[1].replace("%\n", "")))
    plt.bar(x_axis, y_axis, width=0.8, edgecolor='darkblue', linewidth=1)
    plt.xlabel("Кол-во тестов")
    plt.ylabel("Процент верных ответов")
    plt.show()

