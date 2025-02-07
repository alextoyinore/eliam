"""made a few changes to post

Revision ID: 6de777225177
Revises: 8dad793875c3
Create Date: 2025-02-05 02:36:18.504472

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6de777225177'
down_revision = '8dad793875c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('post_author', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('publish_at', sa.DateTime(timezone=True), nullable=True))
        batch_op.drop_constraint('post_authors', type_='foreignkey')
        batch_op.create_foreign_key('user_posts', 'users', ['post_author'], ['id'], ondelete='CASCADE')
        batch_op.drop_column('author')
        batch_op.drop_column('tags')
        batch_op.drop_column('publish_date')
        batch_op.drop_column('categories')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('posts', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categories', sa.TEXT(), nullable=False))
        batch_op.add_column(sa.Column('publish_date', sa.DATETIME(), nullable=True))
        batch_op.add_column(sa.Column('tags', sa.TEXT(), nullable=False))
        batch_op.add_column(sa.Column('author', sa.INTEGER(), nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('post_authors', 'users', ['author'], ['id'])
        batch_op.drop_column('publish_at')
        batch_op.drop_column('post_author')

    # ### end Alembic commands ###
