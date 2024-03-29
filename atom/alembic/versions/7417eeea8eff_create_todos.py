"""create todos

Revision ID: 7417eeea8eff
Revises: 
Create Date: 2024-01-17 18:43:53.359615

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "7417eeea8eff"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("todos")
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("user_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("first_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("last_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("user_id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "todos",
        sa.Column("todo_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("todo_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("todo_done_or_not", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "todo_created_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "todo_updated_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("owner_id", sa.VARCHAR(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.user_id"], name="todos_owner_id_fkey"
        ),
        sa.PrimaryKeyConstraint("todo_id", name="todos_pkey"),
    )
    # ### end Alembic commands ###
