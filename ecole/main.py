#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Application de gestion d'une école
"""

from business.school import School


def main() -> None:
    """Programme principal."""
    print("""\
--------------------------
Bienvenue dans notre école
--------------------------""")

    school: School = School()

    # Test readall teacher
    #teacher_dao = TeacherDao()
    #teachers = teacher_dao.read_all()
    #for teacher in teachers:
        #print(teacher)

    # Test readall course
    #course_dao = CourseDao()
    #courses = course_dao.read_all()
    #for course in courses:
        #print(course)

    #Test readall student
    #student_dao = StudentDao()
    #students = student_dao.read_all()
    #for student in students:
        #print(student)
        #for course in student.courses_taken:
            #print(f" - {course}")
        #print()


    # initialisation d'un ensemble de cours, enseignants et élèves composant l'école
    school.load_from_database()

    # affichage de la liste des cours, leur enseignant et leurs élèves
    print()
    school.display_courses_list()

    #print(school.get_course_by_id(1))
    #print(school.get_course_by_id(2))
    #print(school.get_course_by_id(9))


if __name__ == '__main__':
    main()
