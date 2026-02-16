from __future__ import annotations
from typing import Any, TYPE_CHECKING
from criterion import InvalidAnswerError, HomogeneousCriterion
if TYPE_CHECKING:
    from criterion import Criterion
    from grouper import Grouping
    from course import Student


class Question:
    """An abstract class representing a question used in a survey

    This class should not be instantiated directly.

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Representation Invariants:
    - len(self.text) > 0
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize this question with the text <text>.

        Preconditions:
        - len(text) > 0
        """
        self.id = id_
        self.text = text

    def __str__(self) -> str:
        """Return a string representation of this question that contains both
        the text of this question and a description of all possible answers
        to this question.

        You can choose the precise format of this string.
        """
        raise NotImplementedError

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.
        """
        raise NotImplementedError

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return a float between 0.0 and 1.0 indicating how similar two
        answers are.

        Precondition:
        - <answer1> and <answer2> are both valid answers to this question
        """
        raise NotImplementedError


class MultipleChoiceQuestion(Question):
    """A question whose answers can be one of several options

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Private Attributes:
    - _options: possible answer choices for this question

    Representation Invariants:
    - len(self.text) > 0
    """
    id: int
    text: str
    _options: list

    def __init__(self, id_: int, text: str, options: list) -> None:
        """Initialize a question with the text <text> and id <id> and
        possible answers given in <options>.

        Preconditions:
        - len(text) > 0
        - len(options) >= 2
        - len(set(options)) == len(options)
        """
        super().__init__(id_, text)
        self._options = options

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return f"{self.text}\nOptions: {self._options}"

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid if its content is one of the answer options for this
        question.
        """
        return answer.content in self._options

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return 1.0 iff <answer1>.content and <answer2>.content are equal and
        0.0 otherwise.

        Precondition:
        - <answer1> and <answer2> are both valid answers to this question.
        """
        if answer1.content == answer2.content:
            return 1.0
        return 0.0


class NumericQuestion(Question):
    """A question whose answer can be an integer between some minimum and
    maximum value (inclusive).

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Private Attributes:
    - _min: minimum valid integer answer
    - _max: maximum valid integer answer

    Representation Invariants:
    - len(self.text) > 0
    """
    id: int
    text: str
    _min: int
    _max: int

    def __init__(self, id_: int, text: str, min_: int, max_: int) -> None:
        """Initialize a question with id <id_> and text <text> whose possible
        answers can be any integer between <min_> and <max_> (inclusive)

        Precondition:
        - len(text) > 0
        - min_ < max_
        """
        super().__init__(id_, text)
        self._min = min_
        self._max = max_

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return f"{self.text}\nRange: {self._min} to {self._max}"

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff the content of <answer> is an integer between the
        minimum and maximum (inclusive) possible answers to this question.
        """
        content = answer.content
        return isinstance(content, int) and not isinstance(content, bool) and \
            self._min <= content <= self._max

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2> over the range
        of possible answers to this question.

        Similarity is calculated as follows:
        1. first find the absolute difference between <answer1>.content and
           <answer2>.content.
        2. divide the value from step 1 by the difference between the maximum
           and minimum possible answers.
        3. subtract the value of step 2 from 1.0

        For example:
        - Maximum similarity is 1.0 and occurs when <answer1> == <answer2>
        - Minimum similarity is 0.0 and occurs when <answer1> is the minimum
            possible answer and <answer2> is the maximum possible answer
            (or vice versa).

        Precondition:
        - <answer1> and <answer2> are both valid answers to this question
        """
        diff = abs(answer1.content - answer2.content)
        num_range = self._max - self._min
        return 1.0 - (diff / num_range)


class YesNoQuestion(MultipleChoiceQuestion):
    """A question whose answer is either yes (represented by True) or
    no (represented by False).

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Representation Invariants:
     - len(self.text) > 0
    """
    id: int
    text: str

    def __init__(self, id_: int, text: str) -> None:
        """Initialize a question with the text <text> and id <id>.
        """
        super().__init__(id_, text, [True, False])

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.
        """
        return isinstance(answer.content, bool)


class CheckboxQuestion(Question):
    """A question whose answers can be one or more of several options

    Public Attributes:
    - id: the id of this question
    - text: the text of this question

    Private Attributes:
    - _options: allowed strings in checkbox answers

    Representation Invariants:
    - len(self.text) > 0
    """
    id: int
    text: str
    _options: list[str]

    def __init__(self, id_: int, text: str, options: list[str]) -> None:
        """Initialize a question with the text <text> and id <id> and
        possible answers given in <options>.
        """
        super().__init__(id_, text)
        self._options = options

    def __str__(self) -> str:
        """Return a string representation of this question including the
        text of the question and a description of the possible answers.

        You can choose the precise format of this string.
        """
        return f"{self.text}\nOptions: {self._options}"

    def validate_answer(self, answer: Answer) -> bool:
        """Return True iff <answer> is a valid answer to this question.

        An answer is valid iff:
            * It is a non-empty list.
            * It has no duplicate entries.
            * Every item in it is one of the answer options for this question.
        """
        content = answer.content
        if not isinstance(content, list) or len(content) == 0:
            return False
        if len(content) != len(set(content)):
            return False
        for item in content:
            if not isinstance(item, str) or item not in self._options:
                return False
        return True

    def get_similarity(self, answer1: Answer, answer2: Answer) -> float:
        """Return the similarity between <answer1> and <answer2>.

        Similarity is defined as the ratio between the number of strings that
        are common to both <answer1>.content and <answer2>.content over the
        total number of unique strings that appear in both <answer1>.content and
        <answer2>.content.
        If there are zero unique strings in <answer1>.content and
        <answer2>.content combined, return 1.0

        For example, if <answer1>.content == ['a', 'b', 'c'] and
        <answer2>.content == ['c', 'b', 'd'], there are 2 strings common to
        both: 'c' and 'b'; and there are 4 unique strings that appear in both:
        'a', 'b', 'c', and 'd'. Therefore, the similarity between these two
        answers is 2/4 = 0.5.

        Precondition:
        - <answer1> and <answer2> are both valid answers to this question
        """
        set1 = set(answer1.content)
        set2 = set(answer2.content)
        union = set1 | set2
        if len(union) == 0:
            return 1.0
        inter = set1 & set2
        return len(inter) / len(union)


class Answer:
    """An answer to a question used in a survey

    Public Attributes:
    - content: an answer to a single question
    """
    content: Any

    def __init__(self, content: Any) -> None:
        """Initialize this answer with content <content>"""
        self.content = content

    def is_valid(self, question: Question) -> bool:
        """Return True iff this answer is a valid answer to <question>"""
        return question.validate_answer(self)


class Survey:
    """A survey containing questions as well as criteria and weights used to
    evaluate the quality of a group based on their answers to the survey
    questions.

    Representation Invariants:
    - No two questions on this survey have the same id

    NOTE: The weights associated with the questions in a survey do NOT have to
          sum up to any particular amount.
    """
    # Private Attributes:
    # - _questions: a dictionary mapping a question's id to the question itself
    # - _criteria: a dictionary mapping a question's id to its associated
    #   criterion
    # - _weights: a dictionary mapping a question's id to a weight -- an integer
    # representing the importance of these criteria.
    #
    # Representation Invariants - for Private Attributes:
    # - Each key in _questions equals the id attribute of its value
    # - The dictionaries _questions, _criteria, and _weights all have the same
    #   keys
    # - Each value in _weights is greater than 0
    _questions: dict[int, Question]
    _criteria: dict[int, Criterion]
    _weights: dict[int, int]

    def __init__(self, questions: list[Question]) -> None:
        """Initialize a new survey that contains every question in <questions>.

        This new survey should use a HomogeneousCriterion as a default criterion
        and should use 1 as a default weight.
        """
        self._questions = {}
        self._criteria = {}
        self._weights = {}
        default_criterion = HomogeneousCriterion()
        for q in questions:
            self._questions[q.id] = q
            self._criteria[q.id] = default_criterion
            self._weights[q.id] = 1

    def __len__(self) -> int:
        """Return the number of questions in this survey"""
        return len(self._questions)

    def __contains__(self, question: Question) -> bool:
        """Return True iff there is a question in this survey with the same
        id as <question>.
        """
        return question.id in self._questions

    def __str__(self) -> str:
        """Return a string containing the string representation of all
        questions in this survey.

        You can choose the precise format of this string.
        """
        return '\n'.join(str(q) for q in self.get_questions())

    def get_questions(self) -> list[Question]:
        """Return a list of all questions in this survey"""
        return [self._questions[qid] for qid in sorted(self._questions)]

    def _get_criterion(self, question: Question) -> Criterion:
        """Return the criterion associated with <question> in this survey.

        Precondition:
        - <question>.id occurs in this survey
        """
        return self._criteria[question.id]

    def _get_weight(self, question: Question) -> int:
        """Return the weight associated with <question> in this survey.

        Precondition:
        - <question>.id occurs in this survey
        """
        return self._weights[question.id]

    def set_weight(self, weight: int, question: Question) -> bool:
        """Set the weight associated with <question> to <weight> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.

        Precondition:
        - weight > 0
        """
        if question.id not in self._weights:
            return False
        self._weights[question.id] = weight
        return True

    def set_criterion(self, criterion: Criterion, question: Question) -> bool:
        """Set the criterion associated with <question> to <criterion> and
        return True.

        If <question>.id does not occur in this survey, do not set the <weight>
        and return False instead.
        """
        if question.id not in self._criteria:
            return False
        self._criteria[question.id] = criterion
        return True

    def _get_ans(self, sts: list[Student], q: Question) -> list[Answer] | None:
        answers = []
        for s in sts:
            ans = s.get_answer(q)
            if ans is None:
                return None
            answers.append(ans)
        return answers

    def score_students(self, students: list[Student]) -> float:
        """Return a quality score for <students> calculated based on their
        answers to the questions in this survey, and the associated criterion
        and weight for each question.

        The score is determined using the following algorithm:
        1. For each question in this survey, find the question's associated
           criterion (do we want homogeneous answers, for instance), weight,
           and <students> answers to the question. Use the score_answers method
           for its criterion to calculate how well the <students> answers
           satisfy the criterion. Multiply this quality score by the question's
           weight.
        2. Find the average of all quality scores from step 1.

        This method should NOT throw an InvalidAnswerError. If one occurs
        during the execution of this method or if there are no questions in
        <self>, return zero.

        Precondition:
        - All students in <students> have an answer to all questions in this
            survey
        - len(students) > 0
        """
        if len(self._questions) == 0:
            return 0.0
        total = 0.0
        try:
            for q in self.get_questions():
                answers = self._get_ans(students, q)
                if answers is None:
                    return 0.0
                ans_scores = self._get_criterion(q).score_answers(q, answers)
                total += ans_scores * self._get_weight(q)
            return total / len(self._questions)
        except InvalidAnswerError:
            return 0.0

    def score_grouping(self, grouping: Grouping) -> float:
        """Return a score for <grouping> calculated based on the answers of
        each student in each group in <grouping> to the questions in <self>.

        If there are no groups in <grouping> return 0.0. Otherwise, the score
        is determined using the following algorithm:
        1. For each group in <grouping>, calculate the score for the members of
           this group based on their answers to the questions in this survey.
        2. Return the average of all the scores calculated in step 1.

        Precondition:
        - All students in the groups in <grouping> have an answer to all
        questions in this survey
        """
        groups = grouping.get_groups()
        if len(groups) == 0:
            return 0.0
        total = 0.0
        for g in groups:
            total += self.score_students(g.get_members())
        return total / len(groups)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing',
                                                  'criterion',
                                                  'course',
                                                  'grouper'],
                                'disable': ['E9992']})
