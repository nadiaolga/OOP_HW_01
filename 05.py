# Вычисляем среднюю оценку по словарю
# Формируем общий список оценок
def get_avg_grade(grades_dict):
    all_grades = []
    for subject_grades in grades_dict.values():
        all_grades.extend(subject_grades)

    if all_grades:
        return round(sum(all_grades) / len(all_grades), 1)
    return 0.0

# Вычисляем среднюю оценку по курсу
# Для списка студентов и для списка лекторов
def get_avg_grade_by_course(persons_list, course_name):
    all_grades = []
    for person in persons_list:
        # Проверяем, есть ли оценки по этому курсу у человека
        if course_name in person.grades:
            all_grades.extend(person.grades[course_name])

    if all_grades:
        return round(sum(all_grades) / len(all_grades), 1)
    return 0.0


# Класс студентов. Имя, фамилия, пол, законченные курсы, текущие курсы и оценки - словарь.
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    # Студент выставляет оценку лектору.
    def rate_lecture(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in lecturer.courses_attached and course in self.courses_in_progress:
            if isinstance(grade, int) and 0 <= grade <= 10:
                if course in lecturer.grades:
                    lecturer.grades[course] += [grade]
                else:
                    lecturer.grades[course] = [grade]
            else:
                return 'Оценка неправильная'
        else:
            return 'Ошибка'

    def avg_grade(self):
        return get_avg_grade(self.grades)

    def __str__(self):
        avg_grade = self.avg_grade()

        if self.courses_in_progress:
            in_progress = ", ".join(self.courses_in_progress)
        else:
            in_progress = "Нет"

        finished = ", ".join(self.finished_courses) if self.finished_courses else "Нет"

        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за домашние задания: {avg_grade}\n"
            f"Курсы в процессе изучения: {in_progress}\n"
            f"Завершенные курсы: {finished}"
        )

    # Сравнение студентов
    def __lt__(self, other):
        if not isinstance(other, Student): return NotImplemented
        return self.avg_grade() < other.avg_grade()

    def __gt__(self, other):
        if not isinstance(other, Student): return NotImplemented
        return self.avg_grade() > other.avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Student): return NotImplemented
        return self.avg_grade() == other.avg_grade()


# Класс преподавателей. Имя, фамилия и список закрепленных курсов.
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


# Дочерний класс Lecturer (лекторы).
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def avg_grade(self):
        return get_avg_grade(self.grades)

    def __str__(self):
        avg_grade = self.avg_grade()

        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}\n"
            f"Средняя оценка за лекции: {avg_grade}"
        )

    # Сравнение лекторов
    def __lt__(self, other):
        if not isinstance(other, Lecturer): return NotImplemented
        return self.avg_grade() < other.avg_grade()

    def __gt__(self, other):
        if not isinstance(other, Lecturer): return NotImplemented
        return self.avg_grade() > other.avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer): return NotImplemented
        return self.avg_grade() == other.avg_grade()

# Дочерний класс Reviewer (эксперты, проверяющие домашние задания).
class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(grade, int) and 0 <= grade <= 10:
            if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
                if course in student.grades:
                    student.grades[course] += [grade]
                else:
                    student.grades[course] = [grade]
            else:
                return 'Ошибка'
        else:
            return 'Оценка неправильная'

    def __str__(self):
        return (
            f"Имя: {self.name}\n"
            f"Фамилия: {self.surname}"
        )

# ========================================================
# БЛОК ТЕСТИРОВАНИЯ И ВЫЗОВА МЕТОДОВ
# ========================================================

# 1. Создаем по 2 экземпляра каждого класса
student_1 = Student('Ольга', 'Алёхина', 'Ж')
student_2 = Student('Иван', 'Петров', 'М')

lecturer_1 = Lecturer('Сергей', 'Дмитриев')
lecturer_2 = Lecturer('Елена', 'Иванова')

reviewer_1 = Reviewer('Пётр', 'Сидоров')
reviewer_2 = Reviewer('Анна', 'Кузнецова')

# 2. Наполняем курсы
student_1.courses_in_progress += ['Python', 'Git']
student_2.courses_in_progress += ['Python', 'Java']
student_1.finished_courses += ['Basic']

lecturer_1.courses_attached += ['Python', 'Git']
lecturer_2.courses_attached += ['Python', 'Java']

reviewer_1.courses_attached += ['Python', 'Git']
reviewer_2.courses_attached += ['Python', 'Java']

# 3. Вызываем методы (Проверяющие оценивают студентов)
reviewer_1.rate_hw(student_1, 'Python', 10)
reviewer_1.rate_hw(student_1, 'Python', 9)
reviewer_1.rate_hw(student_1, 'Git', 8)

reviewer_2.rate_hw(student_2, 'Python', 8)
reviewer_2.rate_hw(student_2, 'Python', 7)
reviewer_2.rate_hw(student_2, 'Java', 9)

# 4. Вызываем методы (Студенты оценивают лекторов)
student_1.rate_lecture(lecturer_1, 'Python', 10)
student_1.rate_lecture(lecturer_1, 'Git', 9)

student_2.rate_lecture(lecturer_2, 'Python', 7)
student_2.rate_lecture(lecturer_2, 'Python', 9)
student_2.rate_lecture(lecturer_2, 'Java', 9)

# 5. Выводим словари оценок
print(f"\nОценки Студента 1 ({student_1.surname}): {student_1.grades}")
print(f"Оценки Студента 2 ({student_2.surname}): {student_2.grades}")
print(f"Оценки Лектора 1 ({lecturer_1.surname}): {lecturer_1.grades}")
print(f"Оценки Лектора 2 ({lecturer_2.surname}): {lecturer_2.grades}")

# 6. Выводим информацию о каждом объекте (__str__)
print("\n--- СТУДЕНТЫ ---")
for student in [student_1, student_2]:
    print(student, end="\n\n")

print("--- ЛЕКТОРЫ ---")
for lecturer in [lecturer_1, lecturer_2]:
    print(lecturer, end="\n\n")

print("--- ПРОВЕРЯЮЩИЕ ---")
for reviewer in [reviewer_1, reviewer_2]:
    print(reviewer)
    print()  # Обычный пустой отступ

# 7. Проверяем магические методы сравнения
print("\n--- СРАВНЕНИЕ (Магические методы) ---")
print(f"Студент 1 учится лучше Студента 2? {student_1 > student_2}")
print(f"Студент 1 учится хуже Студента 2? {student_1 < student_2}")
print(f"Студенты равны? {student_1 == student_2}")
print(f"Лектор 1 читает лекции хуже Лектора 2? {lecturer_1 < lecturer_2}")
print(f"Лектор 1 читает лекции лучше Лектора 2? {lecturer_1 > lecturer_2}")
print(f"Лекторы равны? {lecturer_1 == lecturer_2}")

# 8. Вызов функций для подсчета средних по курсу
print("\n--- СРЕДНИЕ ОЦЕНКИ ПО КУРСАМ ---")

# Списки для передачи в функции
all_students = [student_1, student_2]
all_lecturers = [lecturer_1, lecturer_2]

avg_hw_python = get_avg_grade_by_course(all_students, 'Python')
print(f"Средняя оценка за ДЗ по курсу 'Python' среди всех студентов: {avg_hw_python}")

avg_lect_python = get_avg_grade_by_course(all_lecturers, 'Python')
print(f"Средняя оценка за лекции по курсу 'Python' среди всех лекторов: {avg_lect_python}")

# 9. Проверка промежуточных условий и ошибок
print("\n--- ПРОВЕРКА КОРРЕКТНОСТИ И ОШИБОК ---")

print(isinstance(student_1, Student))
print(isinstance(lecturer_1, Mentor))
print(isinstance(reviewer_2, Mentor))
print(lecturer_1.courses_attached)
print(reviewer_2.courses_attached)

# Проверяем возвращаемые значения методов при разных условиях
print(student_1.rate_lecture(lecturer_1, 'Python', 7))   # None
print(student_1.rate_lecture(lecturer_1, 'Java', 8))     # Ошибка
print(student_1.rate_lecture(lecturer_1, 'C++', 8))      # Ошибка
print(student_1.rate_lecture(reviewer_1, 'Python', 6))   # Ошибка
print(reviewer_1.rate_hw(student_1, 'Python', 10))  # None
print(reviewer_1.rate_hw(student_2, 'Git', 8))      # Ошибка
print(reviewer_2.rate_hw(student_1, 'Java', 9))     # Ошибка
print(reviewer_1.rate_hw(student_1, 'Python', 15))  # Оценка неправильная

print(get_avg_grade_by_course(all_students, 'C++'))
print(get_avg_grade_by_course([], 'Python'))


