"""add paper chunk embeddings

Revision ID: 77c346370412
Revises: 56ddcfffe42e
Create Date: 2026-09-17 06:27:43.644857

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "77c346370412"
down_revision: Union[str, Sequence[str], None] = "56ddcfffe42e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "paper_chunk_embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("paper_id", sa.String(length=64), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("embedding", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "paper_id",
            "chunk_index",
            name="uq_paper_chunk_embedding_index",
        ),
    )

    op.create_index(
        op.f("ix_paper_chunk_embeddings_paper_id"),
        "paper_chunk_embeddings",
        ["paper_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_paper_chunk_embeddings_paper_id"),
        table_name="paper_chunk_embeddings",
    )

    op.drop_table("paper_chunk_embeddings")