# -*- coding: utf-8 -*-

"""
Classe Dao[Course]
"""
from dataclasses import dataclass
from typing import Optional

from daos.dao import Dao
from models.course import Course
from models.teacher import Teacher


@dataclass
class CourseDao(Dao[Course]):
    def create(self, course: Course) -> int:
        """Crée en BD l'entité Course correspondant au cours course

        :param course: à créer sous forme d'entité Course en BD
        :return: l'id de l'entité insérée en BD (0 si la création a échoué)
        """
        if course.teacher is None:
            return 0

        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO course (name, start_date, end_date, id_teacher) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (course.name, course.start_date,course.end_date, course.teacher.id))
            id_course = cursor.lastrowid
            course.id = id_course
            Dao.connection.commit()
        return id_course

    def read(self, id_course: int) -> Optional[Course]:
        """Renvoit le cours correspondant à l'entité dont l'id est id_course
           (ou None s'il n'a pu être trouvé)"""
        course: Optional[Course]
        
        with Dao.connection.cursor() as cursor:
            sql = """SELECT course.*, teacher.hiring_date, person.first_name, person.last_name, person.age 
                    FROM course 
                    JOIN teacher ON course.id_teacher = teacher.id_teacher
                    JOIN person ON teacher.id_person = person.id_person
                    WHERE course.id_course=%s"""
            cursor.execute(sql, (id_course,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(record['first_name'], record['last_name'], record['age'], record['hiring_date'])
            teacher.id = record['id_teacher']
            course = Course(record['name'], record['start_date'], record['end_date'])
            course.id = record['id_course']
            course.set_teacher(teacher)
        else:
            course = None

        return course

    def update(self, course: Course) -> bool:
        """Met à jour en BD l'entité Course correspondant à course, pour y correspondre

        :param course: cours déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        if course.teacher is None:
            return False

        with Dao.connection.cursor() as cursor:
            sql = """UPDATE course 
                    SET name = %s, start_date = %s, end_date = %s, id_teacher = %s
                    WHERE id_course = %s"""
            cursor.execute(sql,(course.name, course.start_date, course.end_date,course.teacher.id, course.id))
            Dao.connection.commit()
        return True

    def delete(self, course: Course) -> bool:
        """Supprime en BD l'entité Course correspondant à course

        :param course: cours dont l'entité Course correspondante est à supprimer
        :return: True si la suppression a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = "DELETE FROM course WHERE id_course = %s"
            cursor.execute(sql, (course.id,))
            Dao.connection.commit()

        return True
