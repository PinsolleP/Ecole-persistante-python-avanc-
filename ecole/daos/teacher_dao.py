# -*- coding: utf-8 -*-

"""
Classe Dao[Teacher]
"""
from models import person
from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional
from datetime import date


@dataclass
class TeacherDao(Dao[Teacher]):
    def create(self, teacher: Teacher) -> int:
        """Crée en BD l'entité Teacher correspondant à teacher.

        :param teacher: enseignant à créer en BD
        :return: l'id de l'enseignant créé
        """
        with Dao.connection.cursor() as cursor:
            sql = "INSERT INTO person (first_name, last_name, age) VALUES (%s, %s, %s)"
            cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age))
            id_person = cursor.lastrowid
            sql = "INSERT INTO teacher (hiring_date, id_person) VALUES (%s, %s)"
            cursor.execute(sql, (teacher.hiring_date, id_person))
            id_teacher = cursor.lastrowid
            teacher.id = id_teacher
            Dao.connection.commit()
            return id_teacher

    def read(self, id_teacher: int) -> Optional[Teacher]:
        """Renvoit le Teacher correspondant à l'identifiant fourni

            :param id_teacher: identifiant du professeur à rechercher
            :return: le professeur trouvé ou None s'il n'existe pas"""

        teacher: Optional[Teacher]

        with Dao.connection.cursor() as cursor:
            sql = """SELECT * FROM teacher 
                     JOIN person ON teacher.id_person = person.id_person
                     WHERE teacher.id_teacher = %s"""
            cursor.execute(sql, (id_teacher,))
            record = cursor.fetchone()
        if record is not None:
            teacher = Teacher(
                record['first_name'],
                record['last_name'],
                record['age'],
                record['hiring_date']
            )
            teacher.id = record['id_teacher']
            return teacher
        return None

    def update(self, teacher: Teacher) -> bool:
        """Met à jour en BD l'entité teacher correspondant à teacher, pour y correspondre

        :param teacher: teacher déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée
        """
        with Dao.connection.cursor() as cursor:
            sql = ("""UPDATE person 
                    JOIN teacher ON person.id_person = teacher.id_person
                    SET person.first_name = %s, person.last_name = %s, person.age = %s
                    WHERE teacher.id_teacher = %s""")

            cursor.execute(sql, (teacher.first_name, teacher.last_name, teacher.age, teacher.id))

            sql = ("""UPDATE teacher 
                    SET hiring_date = %s
                    WHERE id_teacher = %s""")

            cursor.execute(sql, (teacher.hiring_date, teacher.id))
            Dao.connection.commit()
        return True

    def delete(self, teacher: Teacher) -> bool:
        """Supprime en BD l'entité Teacher correspondant à teacher.

          :param teacher: enseignant dont l'entité doit être supprimée
          :return: True si la suppression a pu être réalisée
         """

        with Dao.connection.cursor() as cursor:
            sql = """SELECT id_person 
                            FROM teacher
                            WHERE id_teacher = %s"""
            cursor.execute(sql, (teacher.id,))
            record = cursor.fetchone()
            if record is None:
                return False
            id_person = record['id_person']

            sql = """DELETE FROM teacher 
                    WHERE id_teacher = %s"""
            cursor.execute(sql, (teacher.id,))

            sql = """DELETE FROM person 
                    WHERE id_person = %s"""
            cursor.execute(sql, (id_person,))
            Dao.connection.commit()

        return True


