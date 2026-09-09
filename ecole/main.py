#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School
from datetime import date

from daos.teacher_dao import TeacherDao
from daos.course_dao import CourseDao
from models.teacher import Teacher
from models.course import Course


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_static()

    """Test
    teacher = Teacher(
        "Victor", "Hugo", 23, date(2023, 9, 4)
    )
    teacher.id =1

    course = Course("Python", date(2024, 3, 18), date(2024, 3, 29))
    course.set_teacher(teacher)
    course_dao = CourseDao()
    id_course = course_dao.create(course)
    print(f"Course créé avec l'id : {id_course}")
    print(course)

    course_read = course_dao.read(id_course)
    print("Course lu depuis la BDD :")
    print(course_read)

    course_not_found = course_dao.read(9999)
    print(f"Course inexistant : {course_not_found}")

    course.name = "Python avancé"
    result = course_dao.update(course)
    print(f"Résultat de la mise à jour : {result}")
    course_update = course_dao.read(course.id)
    print("Course après mise à jour :")
    print(course_update)

    result = course_dao.delete(course)
    print(f"Résultat de la suppression : {result}")
    course_deleted = course_dao.read(course.id)
    print(f"Course après suppression : {course_deleted}")"""


    # affichage de la liste des cours, leur enseignant et leurs élèves
    print()
    school.display_courses_list()

    print(school.get_course_by_id(1))
    print(school.get_course_by_id(2))
    print(school.get_course_by_id(9))


if __name__ == '__main__':
    main()
