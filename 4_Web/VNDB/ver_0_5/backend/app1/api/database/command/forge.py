import random
from faker import Faker

import click
from flask.cli import with_appcontext

from api.database import create

fake = Faker()

@click.command('forge-db')
@click.option('--count', default=10, help='Quantity of data, default is 10.')
@with_appcontext
def forge_db(count):
    """Generate fake data for all models."""
    generate_fake_vns(count)
    generate_fake_tags(count)
    generate_fake_producers(count)
    generate_fake_staff(count)
    generate_fake_characters(count)
    generate_fake_traits(count)
    generate_fake_releases(count)  # New function added
    click.echo(f'Generated {count} fake entries for each model.')

def generate_fake_vns(count):
    for _ in range(count):
        vn_data = {
            'id': fake.uuid4(),
            'title': fake.sentence(nb_words=4),
            'titles': {'en': fake.sentence(nb_words=4), 'jp': fake.sentence(nb_words=4)},
            'aliases': [fake.word() for _ in range(3)],
            'olang': 'ja',
            'devstatus': random.randint(0, 2),  # 0: Finished, 1: In development, 2: Cancelled
            'released': [int(x) for x in fake.date_this_decade().split('-')],
            'languages': ['en', 'ja'],
            'platforms': ['win', 'lin', 'mac'],
            'image': {'url': fake.image_url(), 'thumbnail': fake.image_url()},
            'length': random.randint(1, 5),
            'length_minutes': random.randint(60, 3000),
            'length_votes': random.randint(1, 1000),
            'description': fake.text(),
            'screenshots': [{'url': fake.image_url(), 'thumbnail': fake.image_url()} for _ in range(3)],
            'relations': [],
            'tags': [],
            'developers': [],
            'staff': [],
            'va': [],
            'extlinks': []
        }
        create('vn', vn_data['id'], vn_data)

def generate_fake_tags(count):
    for _ in range(count):
        tag_data = {
            'id': fake.uuid4(),
            'aid': fake.uuid4(),
            'name': fake.word(),
            'aliases': [fake.word() for _ in range(2)],
            'description': fake.text(),
            'category': random.choice(['cont', 'ero', 'tech']),
            'searchable': fake.boolean(),
            'applicable': fake.boolean(),
            'vn_count': random.randint(0, 100)
        }
        create('tag', tag_data['id'], tag_data)

def generate_fake_producers(count):
    for _ in range(count):
        producer_data = {
            'id': fake.uuid4(),
            'name': fake.company(),
            'original': fake.company(),
            'aliases': [fake.company() for _ in range(2)],
            'lang': 'ja',
            'type': random.choice(['co', 'in', 'ng']),
            'description': fake.text()
        }
        create('producer', producer_data['id'], producer_data)

def generate_fake_staff(count):
    for _ in range(count):
        staff_data = {
            'id': fake.uuid4(),
            'aid': fake.uuid4(),
            'ismain': fake.boolean(),
            'name': fake.name(),
            'original': fake.name(),
            'lang': 'ja',
            'gender': random.choice(['m', 'f']),
            'description': fake.text(),
            'extlinks': [{'url': fake.url(), 'label': fake.word()} for _ in range(2)],
            'aliases': [{'name': fake.name(), 'original': fake.name()} for _ in range(2)]
        }
        create('staff', staff_data['id'], staff_data)

def generate_fake_characters(count):
    for _ in range(count):
        character_data = {
            'id': fake.uuid4(),
            'name': fake.name(),
            'original': fake.name(),
            'aliases': [fake.name() for _ in range(2)],
            'description': fake.text(),
            'image': {'url': fake.image_url(), 'thumbnail': fake.image_url()},
            'blood_type': random.choice(['a', 'b', 'ab', 'o']),
            'height': random.randint(140, 200),
            'weight': random.randint(40, 100),
            'bust': random.randint(70, 110),
            'waist': random.randint(50, 90),
            'hips': random.randint(70, 110),
            'cup': random.choice(['AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K']),
            'age': random.randint(1, 100),
            'birthday': [random.randint(1, 12), random.randint(1, 28)],
            'sex': [random.choice(['m', 'f', 'b', 'n'])],
            'vns': [],
            'traits': []
        }
        create('character', character_data['id'], character_data)

def generate_fake_traits(count):
    for _ in range(count):
        trait_data = {
            'id': fake.uuid4(),
            'name': fake.word(),
            'aliases': [fake.word() for _ in range(2)],
            'description': fake.text(),
            'searchable': fake.boolean(),
            'applicable': fake.boolean(),
            'group_id': fake.uuid4(),
            'group_name': fake.word(),
            'char_count': random.randint(0, 100)
        }
        create('trait', trait_data['id'], trait_data)

def generate_fake_releases(count):
    for _ in range(count):
        release_data = {
            'id': fake.uuid4(),
            'title': fake.sentence(nb_words=4),
            'alttitle': fake.sentence(nb_words=4),
            'languages': [{'lang': lang, 'title': fake.sentence(nb_words=3), 'latin': fake.sentence(nb_words=3), 'mtl': fake.boolean(), 'main': fake.boolean()} for lang in ['en', 'ja']],
            'platforms': ['win', 'lin', 'mac'],
            'media': [{'medium': 'dvd', 'qty': random.randint(1, 5)}],
            'vns': [{'id': fake.uuid4(), 'rtype': random.choice(['trial', 'partial', 'complete'])}],
            'producers': [{'id': fake.uuid4(), 'developer': fake.boolean(), 'publisher': fake.boolean()}],
            'images': [{'url': fake.image_url(), 'thumbnail': fake.image_url(), 'type': random.choice(['pkgfront', 'pkgback', 'pkgcontent', 'pkgside', 'pkgmed', 'dig'])}],
            'released': [int(x) for x in fake.date_this_decade().split('-')],
            'minage': random.randint(0, 18),
            'patch': fake.boolean(),
            'freeware': fake.boolean(),
            'uncensored': fake.boolean(),
            'official': fake.boolean(),
            'has_ero': fake.boolean(),
            'resolution': [random.randint(640, 1920), random.randint(480, 1080)],
            'engine': fake.word(),
            'voiced': random.randint(1, 4),  # 1: not voiced, 2: only ero scenes voiced, 3: partially voiced, 4: fully voiced
            'notes': fake.text(),
            'gtin': fake.ean13(),
            'catalog': fake.isbn13(),
            'extlinks': [{'url': fake.url(), 'label': fake.word(), 'name': fake.word(), 'id': fake.uuid4()} for _ in range(2)]
        }
        create('release', release_data['id'], release_data)