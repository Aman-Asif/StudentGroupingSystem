from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from survey import Question, Answer


class InvalidAnswerError(Exception):
    """Error that should be raised when an answer is invalid for a given
    question.
    """


class Criterion:
    """An abstract class representing a criterion used to evaluate the quality
    of a group based on the group members' answers for a given question.

    This class should not be instantiated directly.
    """

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return score between 0.0 and 1.0 indicating how well the group
        of <answers> to the question <question> satisfy this Criterion.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Each implementation of this abstract class will measure satisfaction of
        a criterion differently.

        Preconditions:
        - len(answers) > 0
        """
        raise NotImplementedError


class HomogeneousCriterion(Criterion):
    """A criterion used to evaluate the quality of a group based on the group
    members' answers for a given question.

    This criterion gives a higher score to answers that are more similar.
    """

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return a score between 0.0 and 1.0 indicating how similar the
        answers in <answers> are.

        This score is calculated by finding the similarity of every combination
        of two answers in <answers> and taking the average of all of these
        similarity scores.
            * Don't include a pair of answers twice while finding the
              similarity scores. For example, don't compare answers[1] and
              answers[2], then later compare answers[2] and answers[1].
            * Don't compare an answer with itself while computing the similarity
              scores. For example, don't compare answers[1] and answers[1].
            * Don't do any rounding.
        If there is only one answer in <answers> and it is valid, return 1.0
        since a single answer is always identical to itself.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Precondition:
        - len(answers) > 0
        """
        for ans in answers:
            if not ans.is_valid(question):
                raise InvalidAnswerError

        if len(answers) == 1:
            return 1.0
        total = 0.0
        count = 0
        # Compute similarity for every unique pair of answers
        for i in range(len(answers)):
            for j in range(i + 1, len(answers)):
                total += question.get_similarity(answers[i], answers[j])
                count += 1
        return total / count


class HeterogeneousCriterion(HomogeneousCriterion):
    """A criterion used to evaluate the quality of a group based on the group
    members' answers for a given question.

    This criterion gives a higher score to answers that are more different.
    """

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return a score between 0.0 and 1.0 indicating how different the
        answers in <answers> are.

        This score is calculated by finding the similarity of every
        combination of two answers in <answers>, finding the average of all
        of these similarity scores, and then subtracting this average from 1.0
            * Don't include a pair of answers twice while finding the
              similarity scores.  For example, don't compare answer 1 and
              answer 2, then later compare answer 2 and answer 1.
            * Don't compare an answer with itself while computing the similarity
              scores.
            * Don't do any rounding.
        If there is only one answer in <answers> and it is valid, return 0.0
        since a single answer is never different from itself.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Precondition:
        - len(answers) > 0
        """
        return 1.0 - super().score_answers(question, answers)


class LonelyMemberCriterion(Criterion):
    """A criterion used to measure the quality of a group of students
    according to the group members' answers to a question.

    This criterion gives a higher score to a group if no member of the group
    gives a unique answer to a question, that is, an answer that no other
    member gave.

    This criterion could be used, for example, to avoid putting a student into
    a group where they are the only one from their college.
    """

    def score_answers(self, question: Question, answers: list[Answer]) -> float:
        """Return score between 0.0 and 1.0 indicating the quality of the group
        of <answers> to the question <question>.

        The score returned will be 0.0 iff there are any unique answers in
        <answers> and will be 1.0 otherwise. An answer is unique if there is
        no other answer in <answers> with identical content. If there is only
        one answer in <answers> and it is valid, return 0.0 since the student
        with that answer is by definition the only one with that answer in the
        group.

        Raise InvalidAnswerError if any answer in <answers> is not a valid
        answer to <question>.

        Precondition:
        - len(answers) > 0
        """
        for ans in answers:
            if not ans.is_valid(question):
                raise InvalidAnswerError

        if len(answers) == 1:
            return 0.0
        counts: dict[object, int] = {}
        for ans in answers:
            counts[ans.content] = counts.get(ans.content, 0) + 1
        for freq in counts.values():
            if freq == 1:
                return 0.0
        return 1.0


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['survey']})
