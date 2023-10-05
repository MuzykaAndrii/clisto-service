"""empty message

Revision ID: 08948fb606c5
Revises: 0eca352c170c
Create Date: 2023-10-04 23:00:00.923413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08948fb606c5'
down_revision: Union[str, None] = '0eca352c170c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointments_appointment', 'phone',
               existing_type=sa.VARCHAR(length=15),
               type_=sa.String(length=20),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointments_appointment', 'phone',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=15),
               existing_nullable=False)
    # ### end Alembic commands ###