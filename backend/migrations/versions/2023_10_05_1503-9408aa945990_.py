"""empty message

Revision ID: 9408aa945990
Revises: 08948fb606c5
Create Date: 2023-10-05 15:03:18.686856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy_file


# revision identifiers, used by Alembic.
revision: str = '9408aa945990'
down_revision: Union[str, None] = '08948fb606c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('maintenance_services', sa.Column('icon', sqlalchemy_file.types.ImageField(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('maintenance_services', 'icon')
    # ### end Alembic commands ###