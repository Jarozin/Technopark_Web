ANSWERS = [
    {
        'id': i,
        'text': f'Text {i}',
        'correct answer': 0,
        'likes': i + 5,
    }for i in range(3)
]

TAGS = [
    {
        'name': f'Tag_{i}',
    }for i in range(5)
]

MEMBERS = [
    {
        'name': f'Name_{i}',
    }for i in range(9)
]
QUESTIONS = [
    {
        'id': i,
        'title': f'Question {i}',
        'text': f'Text {i}',
        'likes': i + 5,
        'tags': [TAGS[i], TAGS[i + 1]],
    } for i in range(3)
]
