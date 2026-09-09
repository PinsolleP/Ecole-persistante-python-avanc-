#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School
from datetime import date

from daos.teacher_dao import TeacherDao
from models.teacher import Teacher


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    school.init_static()

    """ Test
    teacher = Teacher("Jean", "Dupont", 40, date(2024, 1, 15))
    teacher_dao = TeacherDao()
    id_teacher = teacher_dao.create(teacher)
    print(f"Teacher créé avec l'id : {id_teacher}")
    print(teacher)

    teacher_read = teacher_dao.read(id_teacher)
    print("Teacher lu depuis la BDD :")
    print(teacher_read)

    teacher.first_name = "Jean-Pierre"
    teacher.age = 41
    teacher.hiring_date = date(2024, 2, 1)
    print(teacher)

    teacher_dao.update(teacher)
    teacher_updated = teacher_dao.read(id_teacher)
    print(teacher_updated)

    print("Suppression du teacher...")
    result = teacher_dao.delete(teacher)
    print(f"Suppression réussie : {result}")
    teacher_deleted = teacher_dao.read(teacher.id)
    print(teacher_deleted)"""


    # affichage de la liste des cours, leur enseignant et leurs élèves
    school.display_courses_list()

    print(school.get_course_by_id(1))
    print(school.get_course_by_id(2))
    print(school.get_course_by_id(9))


if __name__ == '__main__':
    main()
