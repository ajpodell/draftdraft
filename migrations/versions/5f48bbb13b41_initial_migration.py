"""Initial migration.

Revision ID: 5f48bbb13b41
Revises: 
Create Date: 2023-01-22 01:46:15.488733

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.schema import Sequence, CreateSequence, DropSequence

# revision identifiers, used by Alembic.
revision = '5f48bbb13b41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player',
    sa.Column('player_id', sa.Integer(), nullable=False),
    sa.Column('player_name_first', sa.String(), nullable=True),
    sa.Column('player_name_last', sa.String(), nullable=True),
    sa.Column('college_team', sa.String(), nullable=True),
    sa.Column('position', sa.String(), nullable=True),
    sa.Column('nfl_draft_pick', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('player_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('is_admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('selection',
    sa.Column('row_id', sa.Integer(), nullable=False),
    sa.Column('draftdraft_selection', sa.Integer(), nullable=False),
    sa.Column('player_id', sa.Integer(), nullable=True),
    sa.Column('selecting_team_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['player_id'], ['player.player_id'], ),
    sa.ForeignKeyConstraint(['selecting_team_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('row_id')
    )
    # ### end Alembic commands ###

    # Need to add sequences manually
    op.execute(CreateSequence(Sequence('selection_seq')))


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('selection')
    op.drop_table('user')
    op.drop_table('player')
    # ### end Alembic commands ###

    # Need to drop sequences manually
    op.execute(DropSequence(Sequence('selection_seq')))
