# Вычисляем среднюю оценку по словарю
# Формируем общий список оценок
def get_avg_grade(grades_dict):
    all_grades = []
    for subject_grades in grades_dict.values():
        all_grades.extend(subject_grades)

    if all_grades:
        avg_grade = round(sum(all_grades) / len(all_grades), 1)
    else:
        avg_grade = 0.0

    return avg_grade

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

best_student = Student('Ruoy', 'Eman', 'your_gender')
best_student.courses_in_progress += ['Python']

cool_mentor = Mentor('Some', 'Buddy')
cool_mentor.courses_attached += ['Python']

# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)
# cool_mentor.rate_hw(best_student, 'Python', 10)

# print(best_student.grades)

lecturer = Lecturer('Иван', 'Иванов')
reviewer = Reviewer('Пётр', 'Петров')
# print(isinstance(lecturer, Mentor)) # True
# print(isinstance(reviewer, Mentor)) # True
# print(lecturer.courses_attached)    # []
# print(reviewer.courses_attached)    # []

student = Student('Алёхина', 'Ольга', 'Ж')

student.courses_in_progress += ['Python', 'Java']
lecturer.courses_attached += ['Python', 'C++']
reviewer.courses_attached += ['Python', 'C++']

# print(student.rate_lecture(lecturer, 'Python', 7))  # None
# print(student.rate_lecture(lecturer, 'Java', 8))  # Ошибка
# print(student.rate_lecture(lecturer, 'C++', 8))  # Ошибка
# print(student.rate_lecture(reviewer, 'Python', 6))  # Ошибка
#
# print(lecturer.grades)  # {'Python': [7]}
