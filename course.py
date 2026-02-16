from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from survey import Answer, Survey, Question


# Provided helper function
def sort_students(lst: list[Student], attribute: str) -> list[Student]:
    """Return a shallow copy of <lst> sorted by <attribute> in non-decreasing
    order.

    Being a shallow copy means that a new list is returned, but it contains
    ids of the same Student objects as in <lst>; no new Student objects are
    created. The consequence of this is that aliasing exists. Suggestion: draw
    a memory model diagram to ensure that you understand this.

    Precondition:
    - <attribute> is an attribute name for the Student class

    >>> s1 = Student(1, 'Marcello')
    >>> s2 = Student(2, 'Diane')
    >>> s3 = Student(3, 'Mario')
    >>> sort_students([s1, s3, s2], 'id') == [s1, s2, s3]
    True
    >>> sort_students([s1, s2, s3], 'name') == [s2, s3, s1]
    True
    """
    return sorted(lst, key=lambda student: getattr(student, attribute))


class Student:
    """A Student who can be enrolled in a university course.

    Public Attributes:
    - id: the id of the student
    - name: the name of the student

    Representation Invariants:
    - len(self.name) > 0

    Private Attributes:
    - _answers: the mapping from question id to the student's recorded Answer
    """

    id: int
    name: str
    _answers: dict

    def __init__(self, id_: int, name: str) -> None:
        """Initialize a student with name <name> and id <id>"""
        self.id = id_
        self.name = name
        self._answers = {}
        assert len(self.name) > 0

    def __str__(self) -> str:
        """Return the name of this student"""
        return self.name

    def has_answer(self, question: Question) -> bool:
        """Return True iff this student has an answer for a question with the
        same id as <question> and that answer is a valid answer for <question>.
        """
        return question.id in self._answers

    def set_answer(self, question: Question, answer: Answer) -> None:
        """Record this student's answer <answer> to the question <question>.

        If this student already has an answer recorded for the question, then
        replace it with <answer>.
        """
        self._answers[question.id] = answer

    def get_answer(self, question: Question) -> Answer | None:
        """Return this student's answer to the question <question>.
        Return None if this student does not have an answer to <question>
        """
        return self._answers.get(question.id)


class Course:
    """A University Course

    Public Attributes:
    - name: the name of the course
    - students: a list of students enrolled in the course

    Representation Invariants:
    - len(self.name) > 0
    - No two students in this course have the same id
    """
    name: str
    students: list[Student]

    def __init__(self, name: str) -> None:
        """Initialize a course with the name of <name>.
        """
        self.name = name
        self.students = []
        assert len(self.name) > 0

    def enroll_students(self, students: list[Student]) -> None:
        """Enroll all students in <students> in this course.

        If adding any student would violate a representation invariant,
        do not add any of the students in <students> to the course.

        Preconditions:
        - No two students have the same id in <students>.
        """
        existing_ids = {s.id for s in self.students}
        for student in students:
            if student.id in existing_ids:
                return
        self.students.extend(students)

    def all_answered(self, survey: Survey) -> bool:
        """Return True iff all the students enrolled in this course have a
        valid answer for every question in <survey>.
        """
        for student in self.students:
            for question in survey.get_questions():
                if not student.has_answer(question):
                    return False
                answer = student.get_answer(question)
                if not question.validate_answer(answer):
                    return False
        return True

    def get_students(self) -> tuple[Student, ...]:
        """Return a tuple of all students enrolled in this course.

        The students in this tuple should be in order according to their id
        from the lowest id to the highest id.

        Hint: the sort_students function might be useful
        """
        return tuple(sort_students(self.students, 'id'))


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing', 'survey']})
