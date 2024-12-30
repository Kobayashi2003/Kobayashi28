"""Rename last_modified_at to updated_at and pluralize table names

Revision ID: 3e065f0d98a6
Revises: 
Create Date: 2024-12-29 20:09:35.721022

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3e065f0d98a6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Rename last_modified_at to updated_at for all tables
    tables = ['vn_metadata', 'tag_metadata', 'producer_metadata', 'staff_metadata', 
              'character_metadata', 'trait_metadata', 'release_metadata']
    for table in tables:
        op.alter_column(table, 'last_modified_at', new_column_name='updated_at')

    # Rename tables to plural form
    op.rename_table('vn', 'vns')
    op.rename_table('tag', 'tags')
    op.rename_table('producer', 'producers')
    op.rename_table('character', 'characters')
    op.rename_table('trait', 'traits')
    op.rename_table('release', 'releases')

    op.rename_table('vn_metadata', 'vn_metadatas')
    op.rename_table('tag_metadata', 'tag_metadatas')
    op.rename_table('producer_metadata', 'producer_metadatas')
    op.rename_table('staff_metadata', 'staff_metadatas')
    op.rename_table('character_metadata', 'character_metadatas')
    op.rename_table('trait_metadata', 'trait_metadatas')
    op.rename_table('release_metadata', 'release_metadatas')

    # Update foreign key references
    with op.batch_alter_table('vn_metadatas') as batch_op:
        batch_op.drop_constraint('vn_metadata_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('vn_metadatas_id_fkey', 'vns', ['id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('tag_metadatas') as batch_op:
        batch_op.drop_constraint('tag_metadata_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('tag_metadatas_id_fkey', 'tags', ['id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('producer_metadatas') as batch_op:
        batch_op.drop_constraint('producer_metadata_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('producer_metadatas_id_fkey', 'producers', ['id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('staff_metadatas') as batch_op:
        batch_op.drop_constraint('staff_metadata_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('staff_metadatas_id_fkey', 'staff', ['id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('character_metadatas') as batch_op:
        batch_op.drop_constraint('character_metadata_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('character_metadatas_id_fkey', 'characters', ['id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('trait_metadatas') as batch_op:
        batch_op.drop_constraint('trait_metadata_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('trait_metadatas_id_fkey', 'traits', ['id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('release_metadatas') as batch_op:
        batch_op.drop_constraint('release_metadata_id_fkey', type_='foreignkey')
        batch_op.create_foreign_key('release_metadatas_id_fkey', 'releases', ['id'], ['id'], ondelete='CASCADE')
