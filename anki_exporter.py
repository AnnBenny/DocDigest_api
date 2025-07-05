import genanki
import random
from datetime import datetime

def export_to_anki(flashcards: list[tuple[str, str]], output_path: str):
    model = genanki.Model(
        random.randrange(1 << 30),
        'FlashcardModel',
        fields=[{'name': 'Question'}, {'name': 'Answer'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        }],
    )

    deck = genanki.Deck(
        random.randrange(1 << 30),
        f'AI Flashcards - {datetime.now().strftime("%Y-%m-%d %H:%M")}'
    )

    for q, a in flashcards:
        note = genanki.Note(model=model, fields=[q, a])
        deck.add_note(note)

    genanki.Package(deck).write_to_file(output_path)
