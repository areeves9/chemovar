"""empty message

Revision ID: 06782b70b992
Revises: 
Create Date: 2020-04-24 17:50:09.333625

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06782b70b992'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('compound',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=96), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('strain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image', sa.String(length=255), nullable=True),
    sa.Column('genetics', sa.Text(), nullable=True),
    sa.Column('lineage', sa.JSON(), nullable=True),
    sa.Column('name', sa.String(length=96), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('terpene',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('aroma', sa.String(length=255), nullable=False),
    sa.Column('compound_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['compound_id'], ['compound.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('assay',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('conc', sa.Float(precision=3, asdecimal=True), nullable=False),
    sa.Column('strain', sa.Integer(), nullable=False),
    sa.Column('terpene', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['strain'], ['strain.id'], ),
    sa.ForeignKeyConstraint(['terpene'], ['terpene.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tags',
    sa.Column('terpene_id', sa.Integer(), nullable=False),
    sa.Column('strain_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['strain_id'], ['strain.id'], ),
    sa.ForeignKeyConstraint(['terpene_id'], ['terpene.id'], ),
    sa.PrimaryKeyConstraint('terpene_id', 'strain_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tags')
    op.drop_table('assay')
    op.drop_table('terpene')
    op.drop_table('strain')
    op.drop_table('compound')
    # ### end Alembic commands ###
