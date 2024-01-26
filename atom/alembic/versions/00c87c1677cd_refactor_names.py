"""refactor names

Revision ID: 00c87c1677cd
Revises: 7cb74c59d0b5
Create Date: 2024-01-25 14:23:54.440088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "00c87c1677cd"
down_revision: Union[str, None] = "7cb74c59d0b5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    op.drop_table("todos")
    op.drop_table("users")
    # ### end Alembic commands ###
    op.create_table(
        "users",
        sa.Column(
            "id", sa.Integer(), autoincrement=True, nullable=False, primary_key=True
        ),
        sa.Column("unique_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("first_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("last_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column(
            "email", sa.VARCHAR(), autoincrement=False, nullable=False, unique=True
        ),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
    )

    op.create_table(
        "todos",
        sa.Column(
            "id", sa.Integer(), autoincrement=True, nullable=False, primary_key=True
        ),
        sa.Column("unique_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("title", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("completed", sa.BOOLEAN(), autoincrement=False, nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            postgresql.TIMESTAMP(),
            autoincrement=False,
            nullable=True,
        ),
        sa.Column("owner_id", sa.Integer(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], name="todos_owner_id_fkey", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="todos_pkey"),
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "todos",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("unique_todo_id", sa.VARCHAR(), autoincrement=False, nullable=False),
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
        sa.Column("owner_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["owner_id"], ["users.id"], name="todos_owner_id_fkey", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id", name="todos_pkey"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("unique_user_id", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("first_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("last_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
        sa.UniqueConstraint("email", name="users_email_key"),
    )
    # ### end Alembic commands ###
