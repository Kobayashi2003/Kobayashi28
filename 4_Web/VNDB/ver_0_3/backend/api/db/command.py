from api.db.database import db
from api.db.models  import VN, Tag, Producer, Staff, Character, Trait

import click
from flask.cli import with_appcontext

from faker import Faker
import random 

fake = Faker()

@click.command('initdb')
@click.option('--drop', is_flag=True, help='Create after drop.')
@with_appcontext
def initdb(drop):
    """Clear the existing data and create new tables."""
    if drop:
        click.confirm('This operation will delete the database, do you want to continue?', abort=True)
        db.drop_all()
        click.echo('Drop tables.')
    db.create_all()
    click.echo('Initialized the database.')

@click.command('forge')
@click.option('--count', default=10, help='Quantity of data, default is 10.')
@with_appcontext
def forge(count):
    """Generate fake data for all models."""
    generate_fake_vns(count)
    generate_fake_tags(count)
    generate_fake_producers(count)
    generate_fake_staff(count)
    generate_fake_characters(count)
    generate_fake_traits(count)
    click.echo(f'Generated {count} fake entries for each model.')

def generate_fake_vns(count):
    for _ in range(count):
        vn = VN(
            id=fake.uuid4(),
            title=fake.catch_phrase(),
            aliases=[fake.word() for _ in range(3)],
            olang=random.choice(['en', 'jp', 'zh']),
            devstatus=random.choice(['Finished', 'In development', 'Cancelled']),
            released=fake.date_between(start_date='-10y', end_date='today'),
            languages=[random.choice(['en', 'jp', 'zh']) for _ in range(2)],
            platforms=[random.choice(['win', 'lin', 'mac', 'and', 'ios']) for _ in range(2)],
            length=random.randint(1, 5),
            length_minutes=random.randint(60, 3600),
            description=fake.text(),
            titles=[{
                'lang': lang,
                'title': fake.catch_phrase(),
                'official': fake.boolean(),
                'main': fake.boolean()
            } for lang in ['en', 'jp', 'zh']],
            image={
                'id': fake.uuid4(),
                'url': fake.image_url(),
                'dims': [random.randint(800, 1200), random.randint(600, 900)],
                'sexual': random.randint(0, 2),
                'violence': random.randint(0, 2),
                'thumbnail': fake.image_url(),
                'thumbnail_dims': [random.randint(200, 300), random.randint(150, 225)]
            },
            screenshots=[{
                'url': fake.image_url(),
                'dims': [random.randint(800, 1200), random.randint(600, 900)],
                'sexual': random.randint(0, 2),
                'violence': random.randint(0, 2),
                'thumbnail': fake.image_url(),
                'thumbnail_dims': [random.randint(200, 300), random.randint(150, 225)]
            } for _ in range(3)],
            relations=[{
                'id': fake.uuid4(),
                'title': fake.catch_phrase(),
                'relation': random.choice(['sequel', 'prequel', 'side_story', 'alternative_version']),
                'relation_official': fake.boolean()
            } for _ in range(2)],
            tags=[{
                'id': fake.uuid4(),
                'name': fake.word(),
                'category': random.choice(['cont', 'ero', 'tech']),
                'rating': random.randint(0, 3),
                'spoiler': random.randint(0, 2),
                'lie': fake.boolean()
            } for _ in range(5)],
            developers=[{
                'id': fake.uuid4(),
                'name': fake.company(),
                'original': fake.company()
            } for _ in range(2)],
            staff=[{
                'id': fake.uuid4(),
                'name': fake.name(),
                'original': fake.name(),
                'eid': fake.uuid4(),
                'role': random.choice(['scenario', 'art', 'music'])
            } for _ in range(5)],
            va=[{
                'staff': {
                    'id': fake.uuid4(),
                    'name': fake.name(),
                    'original': fake.name()
                },
                'character': {
                    'id': fake.uuid4(),
                    'name': fake.name(),
                    'original': fake.name()
                }
            } for _ in range(3)],
            extlinks=[{
                'url': fake.url(),
                'label': fake.word(),
                'name': fake.word(),
                'id': fake.uuid4()
            } for _ in range(2)]
        )
        db.session.add(vn)
    db.session.commit()

def generate_fake_tags(count):
    for _ in range(count):
        tag = Tag(
            id=fake.uuid4(),
            name=fake.word(),
            aliases=[fake.word() for _ in range(3)],
            description=fake.text(),
            category=random.choice(['cont', 'ero', 'tech']),
            searchable=fake.boolean(),
            applicable=fake.boolean(),
            vn_count=random.randint(0, 1000)
        )
        db.session.add(tag)
    db.session.commit()

def generate_fake_producers(count):
    for _ in range(count):
        producer = Producer(
            id=fake.uuid4(),
            name=fake.company(),
            original=fake.company(),
            aliases=[fake.company() for _ in range(2)],
            lang=random.choice(['en', 'jp', 'zh']),
            type=random.choice(['co', 'in', 'ng']),
            description=fake.text()
        )
        db.session.add(producer)
    db.session.commit()

def generate_fake_staff(count):
    for _ in range(count):
        staff = Staff(
            id=fake.uuid4(),
            ismain=fake.boolean(),
            name=fake.name(),
            original=fake.name(),
            lang=random.choice(['en', 'jp', 'zh']),
            gender=random.choice(['m', 'f']),
            description=fake.text(),
            aliases=[{
                'aid': fake.uuid4(),
                'name': fake.name(),
                'original': fake.name(),
                'ismain': fake.boolean()
            } for _ in range(2)]
        )
        db.session.add(staff)
    db.session.commit()

def generate_fake_characters(count):
    for _ in range(count):
        character = Character(
            id=fake.uuid4(),
            name=fake.name(),
            original=fake.name(),
            aliases=[fake.name() for _ in range(2)],
            description=fake.text(),
            image={
                'id': fake.uuid4(),
                'url': fake.image_url(),
                'dims': [random.randint(800, 1200), random.randint(600, 900)],
                'sexual': random.randint(0, 2),
                'violence': random.randint(0, 2)
            },
            blood_type=random.choice(['a', 'b', 'ab', 'o']),
            height=random.randint(140, 200),
            weight=random.randint(40, 100),
            bust=random.randint(70, 120),
            waist=random.randint(50, 100),
            hips=random.randint(70, 120),
            cup=random.choice(['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']),
            age=random.randint(15, 50),
            birthday=[random.randint(1, 12), random.randint(1, 28)],
            sex=[random.choice(['m', 'f', 'b', 'n'])],
            vns=[{
                'id': fake.uuid4(),
                'title': fake.catch_phrase(),
                'spoiler': random.randint(0, 2),
                'role': random.choice(['main', 'side', 'appears'])
            } for _ in range(2)],
            traits=[{
                'id': fake.uuid4(),
                'name': fake.word(),
                'group_id': fake.uuid4(),
                'group_name': fake.word(),
                'spoiler': random.randint(0, 2),
                'lie': fake.boolean()
            } for _ in range(5)]
        )
        db.session.add(character)
    db.session.commit()

def generate_fake_traits(count):
    for _ in range(count):
        trait = Trait(
            id=fake.uuid4(),
            name=fake.word(),
            aliases=[fake.word() for _ in range(3)],
            description=fake.text(),
            searchable=fake.boolean(),
            applicable=fake.boolean(),
            group_id=fake.uuid4(),
            group_name=fake.word(),
            char_count=random.randint(1, 1000)
        )
        db.session.add(trait)
    db.session.commit()