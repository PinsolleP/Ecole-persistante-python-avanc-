# -*- coding: utf-8 -*-

"""
Classe Dao[Student]
"""
from models.course import Course
from models.student import Student
from models.address import Address
from models.teacher import Teacher
from daos.dao import Dao
from dataclasses import dataclass
from typing import Optional

@dataclass
class StudentDao(Dao[Student]):
    def create(self, student: Student) -> int:
        """Crée en BD l'entité Student correspondant à student.

        :param student: élève à créer en BD
        :return: le numéro de l'élève créé
        """
        with Dao.connection.cursor() as cursor:
            id_address = None
            if student.address is not None:
                sql = """INSERT INTO address (street, city, postal_code) 
                        VALUES (%s, %s, %s)"""
                cursor.execute(sql, (
                    student.address.street,
                    student.address.city,
                    student.address.postal_code
                ))
                id_address = cursor.lastrowid
                student.address.id = id_address

            sql = "INSERT INTO person (first_name, last_name, age, id_address) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (student.first_name, student.last_name, student.age, id_address))
            id_person = cursor.lastrowid

            sql = "INSERT INTO student (student_nbr, id_person) VALUES (%s, %s)"
            cursor.execute(sql, (student.student_nbr, id_person))
            Dao.connection.commit()
            return student.student_nbr

    def read(self, student_nbr: int) -> Optional[Student]:
        """Renvoie l'élève correspondant au numéro fourni.

        :param student_nbr: numéro de l'élève à rechercher
        :return: l'élève trouvé ou None s'il n'existe pas"""

        student: Optional[Student]

        with Dao.connection.cursor() as cursor:
            sql = """SELECT student.student_nbr, person.first_name, person.last_name, person.age,
                    address.id_address, address.street, address.city, address.postal_code,
                    course.id_course, course.name, course.start_date, course.end_date,
                    teacher.id_teacher, teacher.hiring_date, 
                    teacher_person.first_name AS teacher_first_name,
                    teacher_person.last_name AS teacher_last_name,
                    teacher_person.age AS teacher_age
                    FROM student 
                    JOIN person ON student.id_person = person.id_person
                    LEFT JOIN address ON person.id_address = address.id_address
                    LEFT JOIN takes ON student.student_nbr = takes.student_nbr
                    LEFT JOIN course ON takes.id_course = course.id_course
                    LEFT JOIN teacher ON course.id_teacher = teacher.id_teacher
                    LEFT JOIN person AS teacher_person ON teacher.id_person = teacher_person.id_person
                    WHERE student.student_nbr = %s"""
            cursor.execute(sql, (student_nbr,))
            records = cursor.fetchall()
            if records:
                record = records[0]
                student = Student(
                    record['first_name'],
                    record['last_name'],
                    record['age']
                )
                student.student_nbr = record['student_nbr']
                if record['id_address'] is not None:
                    student.address = Address(
                        record['street'],
                        record['city'],
                        record['postal_code']
                    )
                    student.address.id = record['id_address']
                for record in records:
                    if record['id_course'] is not None:
                        teacher = Teacher(
                            record['teacher_first_name'],
                            record['teacher_last_name'],
                            record['teacher_age'],
                            record['hiring_date']
                        )
                        teacher.id = record['id_teacher']

                        course = Course(
                            record['name'],
                            record['start_date'],
                            record['end_date']
                        )
                        course.id = record['id_course']
                        course.set_teacher(teacher)
                        student.courses_taken.append(course)
            else:
                student = None
            return student

    def update(self, student: Student) -> bool:
        """Met à jour en BD l'élève correspondant à student.

        :param student: élève déjà mis à jour en mémoire
        :return: True si la mise à jour a pu être réalisée"""

        with Dao.connection.cursor() as cursor:
            sql = ("""UPDATE person 
                    JOIN student ON person.id_person = student.id_person
                    SET person.first_name = %s, person.last_name = %s, person.age = %s
                    WHERE student.student_nbr = %s""")

            cursor.execute(sql, (student.first_name, student.last_name, student.age, student.student_nbr))
            Dao.connection.commit()
            return True

    def delete(self, student: Student) -> bool:
        """Supprime en BD l'élève correspondant à student.

        :param student: élève dont l'entité correspondante est à supprimer
        :return: True si la suppression a pu être réalisée"""
        with Dao.connection.cursor() as cursor:
            sql = """SELECT student.id_person, person.id_address 
                    FROM student
                    JOIN person ON student.id_person = person.id_person
                    WHERE student_nbr = %s"""
            cursor.execute(sql, (student.student_nbr,))
            record = cursor.fetchone()
            if record is None:
                return False
            id_person = record['id_person']
            id_address = record['id_address']

            sql = """DELETE FROM takes
                    WHERE student_nbr = %s"""
            cursor.execute(sql, (student.student_nbr,))

            sql = """DELETE FROM student 
                    WHERE student_nbr = %s"""
            cursor.execute(sql, (student.student_nbr,))

            sql = """DELETE FROM person 
                    WHERE id_person = %s"""
            cursor.execute(sql, (id_person,))

            if id_address is not None:
                sql = """DELETE FROM address
                        WHERE id_address = %s"""
                cursor.execute(sql, (id_address,))
            Dao.connection.commit()

        return True