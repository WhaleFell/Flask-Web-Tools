"""empty message

Revision ID: 289716615b79
Revises: 
Create Date: 2021-09-21 16:15:56.469000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '289716615b79'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.alter_column('student_name',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.alter_column('student_class',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('student_photo',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('info', schema=None) as batch_op:
        batch_op.alter_column('student_photo',
               existing_type=sa.TEXT(),
               nullable=False)
        batch_op.alter_column('student_class',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('student_name',
               existing_type=sa.TEXT(),
               nullable=False)

    # ### end Alembic commands ###