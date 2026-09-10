#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School
from datetime import date

from daos.dao import Dao
from daos.teacher_dao import TeacherDao
from daos.course_dao import CourseDao
from daos.student_dao import StudentDao
from models.teacher import Teacher
from models.course import Course
from models.student import Student
from models.address import Address


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_static()

    #Test
    student_dao = StudentDao()
    student = student_dao.read(9)
    print("Etudiant récupéré")
    print(student)


    result = student_dao.delete(student)
    print("Suppression :", result)
    student_chek = student_dao.read(9)
    print("Après suppression :", student_chek)


    # affichage de la liste des cours, leur enseignant et leurs élèves
    print()
    school.display_courses_list()

    print(school.get_course_by_id(1))
    print(school.get_course_by_id(2))
    print(school.get_course_by_id(9))


if __name__ == '__main__':
    main()
