from course import Student, Course
from survey import (
    Survey,
    MultipleChoiceQuestion,
    NumericQuestion,
    YesNoQuestion,
    Answer
)
from criterion import HomogeneousCriterion, HeterogeneousCriterion
from grouper import Group, Grouping, AlphaGrouper, GreedyGrouper


def test_student_set_get() -> None:
    """Setting then getting an answer returns it."""
    s = Student(1, "Aman")
    q = YesNoQuestion(10, "Agree?")
    a = Answer(True)
    s.set_answer(q, a)
    assert s.get_answer(q) == a


def test_student_replace_answer() -> None:
    """New answer replaces existing answer."""
    s = Student(1, "Aman")
    q = YesNoQuestion(10, "Agree?")
    s.set_answer(q, Answer(True))
    s.set_answer(q, Answer(False))
    assert s.get_answer(q).content is False


def test_student_get_none() -> None:
    """Missing answer returns None."""
    s = Student(1, "Aman")
    q = YesNoQuestion(99, "Answered?")
    assert s.get_answer(q) is None


def test_student_has_answer_toggle() -> None:
    """has_answer changes after setting."""
    s = Student(1, "Aman")
    q = YesNoQuestion(5, "Agree?")
    assert not s.has_answer(q)
    s.set_answer(q, Answer(True))
    assert s.has_answer(q)


def test_course_students_sorted() -> None:
    """Students returned sorted by id."""
    c = Course("CSC148")
    c.enroll_students([
        Student(3, "C"),
        Student(1, "A"),
        Student(2, "B")
    ])
    ids = [s.id for s in c.get_students()]
    assert ids == [1, 2, 3]


def test_course_enroll_atomic() -> None:
    """Enrollment fails fully on id conflict."""
    c = Course("CSC148")
    c.enroll_students([Student(1, "A")])
    c.enroll_students([Student(1, "B"), Student(2, "C")])
    assert len(c.students) == 1


def test_course_all_answered_false() -> None:
    """Returns False if any answer missing."""
    c = Course("CSC148")
    s1 = Student(1, "A")
    s2 = Student(2, "B")
    q = YesNoQuestion(1, "Q")
    survey = Survey([q])
    s1.set_answer(q, Answer(True))
    c.enroll_students([s1, s2])
    assert not c.all_answered(survey)


def test_yesno_accept_bool() -> None:
    """Accepts True and False answers."""
    q = YesNoQuestion(1, "Q?")
    assert q.validate_answer(Answer(True))
    assert q.validate_answer(Answer(False))


def test_yesno_reject_non_bool() -> None:
    """Rejects non-boolean answers."""
    q = YesNoQuestion(1, "Q?")
    assert not q.validate_answer(Answer("yes"))
    assert not q.validate_answer(Answer(1))


def test_yesno_similarity() -> None:
    """Similarity is 1 if same, 0 otherwise."""
    q = YesNoQuestion(1, "Q?")
    assert q.get_similarity(Answer(True), Answer(True)) == 1.0
    assert q.get_similarity(Answer(True), Answer(False)) == 0.0


def test_answer_valid_mcq() -> None:
    """Valid MCQ answer returns True."""
    q = MultipleChoiceQuestion(1, "Pick", ["a", "b"])
    assert Answer("a").is_valid(q)


def test_answer_invalid_numeric() -> None:
    """Invalid numeric answer rejected."""
    q = NumericQuestion(2, "Rate", 1, 5)
    assert not Answer("3").is_valid(q)


def test_homogeneous_one() -> None:
    """Single answer scores 1."""
    crit = HomogeneousCriterion()
    q = YesNoQuestion(1, "Q")
    assert crit.score_answers(q, [Answer(True)]) == 1.0


def test_homogeneous_two_same() -> None:
    """Two identical answers score 1."""
    crit = HomogeneousCriterion()
    q = YesNoQuestion(1, "Q")
    ans = [Answer(True), Answer(True)]
    assert crit.score_answers(q, ans) == 1.0


def test_homogeneous_two_diff() -> None:
    """Two different answers score 0."""
    crit = HomogeneousCriterion()
    q = YesNoQuestion(1, "Q")
    ans = [Answer(True), Answer(False)]
    assert crit.score_answers(q, ans) == 0.0


def test_homogeneous_three_avg() -> None:
    """Average similarity for three answers."""
    crit = HomogeneousCriterion()
    q = YesNoQuestion(1, "Q")
    ans = [Answer(True), Answer(True), Answer(False)]
    assert crit.score_answers(q, ans) == 1 / 3


def test_group_len() -> None:
    """Group length equals member count."""
    g = Group([Student(1, "A"), Student(2, "B")])
    assert len(g) == 2


def test_group_contains() -> None:
    """Membership uses student id."""
    s1 = Student(1, "A")
    g = Group([s1])
    assert s1 in g


def test_group_members_copy() -> None:
    """get_members returns shallow copy."""
    members = [Student(1, "A")]
    g = Group(members)
    assert g.get_members() is not members


def test_grouping_reject_overlap() -> None:
    """Overlapping groups are rejected."""
    s = Student(1, "A")
    g1 = Group([s])
    g2 = Group([s])
    grouping = Grouping()
    assert grouping.add_group(g1)
    assert not grouping.add_group(g2)


def test_survey_get_questions() -> None:
    """Returns all questions sorted by id."""
    q1 = YesNoQuestion(2, "Q2")
    q2 = YesNoQuestion(1, "Q1")
    survey = Survey([q1, q2])
    ids = [q.id for q in survey.get_questions()]
    assert ids == [1, 2]


def test_survey_set_weight() -> None:
    """Weight updates when question exists."""
    q = YesNoQuestion(1, "Q")
    survey = Survey([q])
    assert survey.set_weight(3, q)


def test_survey_set_criterion() -> None:
    """Criterion updates when question exists."""
    q = YesNoQuestion(1, "Q")
    survey = Survey([q])
    assert survey.set_criterion(HeterogeneousCriterion(), q)


def test_alpha_grouping() -> None:
    """Alpha grouper groups by name order."""
    c = Course("CSC148")
    c.enroll_students([
        Student(1, "D"),
        Student(2, "A"),
        Student(3, "B"),
        Student(4, "C")
    ])
    survey = Survey([])
    g = AlphaGrouper(2).make_grouping(c, survey)
    assert len(g) == 2


def test_greedy_grouping() -> None:
    """Greedy grouper forms valid groups."""
    c = Course("CSC148")
    c.enroll_students([
        Student(1, "A"),
        Student(2, "B"),
        Student(3, "C"),
        Student(4, "D")
    ])
    survey = Survey([])
    g = GreedyGrouper(2).make_grouping(c, survey)
    assert len(g) == 2
