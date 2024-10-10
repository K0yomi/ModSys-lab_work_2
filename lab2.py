import matplotlib.pyplot as plt # Библиотека для построения графиков
import random # Библиотека для сравнения с готовым генератором
from scipy.stats import kstest # Импорт функции для теста Колмогорова-Смирнова
import numpy as np  # Библиотека для работы с массивами

"""
matplotlib.pyplot позволяет строить графики и диаграммы. Мы будем использовать его, чтобы построить гистограмму и увидеть, как распределяются сгенерированные числа.
random — это стандартная библиотека Python для генерации случайных чисел. Мы будем использовать ее для сравнения с нашим собственным генератором, чтобы убедиться, что всё работает правильно.
kstest — это функция, которая проверяет гипотезу, что числа распределены равномерно. Она возвращает два значения:
    statistic — величина, показывающая, насколько сильно данные отличаются от равномерного распределения.
    p_value — если это значение больше 0.05, то мы не можем отвергнуть гипотезу, что числа равномерно распределены.
"""

# ЛК-генератор
def lcg(seed, a, c, m, n):
    x = seed # Начальное значение (seed)
    results = [] # Список для сохранения сгенерированных чисел
    for _ in range(n):
        x = (a * x + c) % m # Формула ЛК-генератора
        results.append(x / m)  # нормализация к диапазону [0, 1)
    return results

"""
Функция lcg: реализует линейно-конгруэнтный генератор, который генерирует псевдослучайные числа.
Аргументы функции:
    seed — начальное число, с которого начинается генерация.
    a, c, m — параметры, которые задают поведение генератора (выбор этих параметров важен для качества генератора).
    n — количество чисел, которые мы хотим сгенерировать.

Что делает функция?:
    Создается список results, в который мы будем сохранять сгенерированные числа.
    Цикл for повторяется n раз. Каждый раз мы вычисляем новое число x по формуле, затем нормализуем его (делим на m, чтобы число было в пределах от 0 до 1).
    После этого сохраняем результат в список results и возвращаем его после завершения работы цикла.
"""

# Выбор параметров ЛК-генератора для генерации чисел
seed = 1  # начальное значение (seed)
a = 1664525  # множитель
c = 1013904223  # приращение
m = 2**32  # модуль (часто берут 2 в степени, оставаясь в пределах 32-битного целого числа)
n = 10000  # количество чисел

"""
seed можно взять любое число как начальное значение, оно определяет начальную точку генерации. Выбор seed влияет на последовательность генерируемых чисел. Если одно и то же значение seed используется многократно, то последовательность псевдослучайных чисел будет одинаковой.
a = 1664525 и c = 1013904223 — это параметры, которые были предложены в научных статьях для хорошего качества генерации. Эти числа уже доказали свою эффективность для линейных генераторов.
m = 2**32 — модуль задаёт предел для чисел.
n = 10000 — это количество чисел, которые мы хотим сгенерировать для тестов.
"""

# Генерация псевдослучайных чисел
lcg_values = lcg(seed, a, c, m, n)
"""
Здесь мы вызываем нашу функцию и передаем параметры. В результате в переменной lcg_values будет храниться список из 10,000 сгенерированных чисел.
"""

# Построение гистограммы для визуализации равномерности распределения
plt.hist(lcg_values, bins=50, density=True, alpha=0.7, color='blue')
plt.title('LCG Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

"""
Зачем это нужно?
    Гистограмма покажет, как распределены сгенерированные числа. В идеале они должны равномерно покрывать весь диапазон от 0 до 1.

Параметры гистограммы:
    bins=50 — гистограмма будет разбита на 50 "корзинок" (интервалов).
    density=True — нормализуем высоту столбиков, чтобы они представляли вероятности.
    alpha=0.7 — делает столбики немного прозрачными.
    color='blue' — цвет гистограммы.
"""

# Проверка равномерности распределения с помощью теста Колмогорова-Смирнова (K-S тест)
"""
Проверим, насколько хорошо наши числа распределены по диапазону от 0 до 1 с помощью теста Колмогорова-Смирнова (K-S тест). 
Этот тест проверяет, насколько сильно полученная последовательность отклоняется от равномерного распределения.
"""
statistic, p_value = kstest(lcg_values, 'uniform')
print(f"KS-statistic: {statistic}, p-value: {p_value}")

# Генерация случайных чисел с использованием встроенного генератора Python
"""
Теперь мы сравним полученные результаты с результатами стандартного генератора случайных чисел в Python (random).
Это позволит убедиться, что написанный генератор работает так же хорошо, как стандартный генератор в Python.
"""
random_values = [random.random() for _ in range(n)]

# Построение гистограммы для встроенного генератора
plt.hist(random_values, bins=50, density=True, alpha=0.7, color='orange')
plt.title('Random Generator Distribution')
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.show()

statistic, p_value = kstest(random_values, 'uniform')
print(f"KS-statistic (random): {statistic}, p-value: {p_value}")

# 3.1 Тестирование на независимость (Автокорреляционный тест)
"""
Проверка независимости последовательных чисел с использованием автокорреляционного теста.
Автокорреляционный тест проверяет, есть ли корреляция между последовательными числами.
"""

def autocorrelation_test(values, lag=1): # функция,что рассчитывает автокорреляцию для последовательности чисел
    n = len(values)
    mean = np.mean(values)
    autocov = np.sum((values[:n - lag] - mean) * (values[lag:] - mean))
    return autocov / np.var(values)

# Автокорреляция для ЛКГ
autocorr_lcg = autocorrelation_test(lcg_values)
print(f"Autocorrelation (LCG): {autocorr_lcg}")

# Автокорреляция для встроенного генератора
autocorr_random = autocorrelation_test(random_values)
print(f"Autocorrelation (random): {autocorr_random}")

# 3.2 Период ГПСЧ
"""
Определение периода генератора псевдослучайных чисел.
Период — это длина последовательности чисел, после которой генератор начинает повторять значения.
"""

def find_period(values):
    seen = {}
    for i, v in enumerate(values):
        if v in seen:
            return i - seen[v]
        seen[v] = i
    return None

# Поиск периода для ЛКГ
period_lcg = find_period(lcg_values)
print(f"Period (LCG): {period_lcg}")

# Поиск периода для встроенного генератора
period_random = find_period(random_values)
print(f"Period (random): {period_random}")