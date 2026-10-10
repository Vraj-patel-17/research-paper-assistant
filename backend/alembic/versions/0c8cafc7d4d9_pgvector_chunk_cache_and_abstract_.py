"""pgvector chunk cache and abstract embeddings

Revision ID: 0c8cafc7d4d9
Revises: 77c346370412
Create Date: 2026-10-08 14:23:47.986360

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '0c8cafc7d4d9'
down_revision: Union[str, Sequence[str], None] = '77c346370412'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

EMBEDDING_DIM = 768

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Abstract embeddings: abstracts are CC0 metadata, so these are kept permanently.
    op.add_column(
        "papers",
        sa.Column("abstract_embedding", Vector(EMBEDDING_DIM), nullable=True),
    )
    op.create_index(
        "ix_papers_abstract_embedding_hnsw",
        "papers",
        ["abstract_embedding"],
        unique=False,
        postgresql_using="hnsw",
        postgresql_ops={"abstract_embedding": "vector_cosine_ops"},
    )

    # Retire permanent full-text storage and the JSON embedding cache.
    # Order matters: paper_chunks references paper_contents.
    op.execute("DROP TABLE IF EXISTS paper_chunks")
    op.execute("DROP TABLE IF EXISTS paper_contents")
    op.execute("DROP TABLE IF EXISTS paper_chunk_embeddings")

    # Replace them with an expiring cache of chunk text + pgvector embeddings.
    op.create_table(
        "paper_chunks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("paper_id", sa.UUID(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("page", sa.Integer(), nullable=True),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["paper_id"], ["papers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("paper_id", "chunk_index", name="uq_paper_chunk_index"),
    )
    op.create_index(op.f("ix_paper_chunks_paper_id"), "paper_chunks", ["paper_id"], unique=False)
    op.create_index(op.f("ix_paper_chunks_expires_at"), "paper_chunks", ["expires_at"], unique=False)



def downgrade() -> None:
    op.drop_table("paper_chunks")

    op.drop_index("ix_papers_abstract_embedding_hnsw", table_name="papers")
    op.drop_column("papers", "abstract_embedding")

    # Recreate the previous (empty) structures.
    op.create_table(
        "paper_chunk_embeddings",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("paper_id", sa.String(length=64), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("embedding", sa.JSON(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("paper_id", "chunk_index", name="uq_paper_chunk_embedding_index"),
    )
    op.create_index(
        op.f("ix_paper_chunk_embeddings_paper_id"),
        "paper_chunk_embeddings",
        ["paper_id"],
        unique=False,
    )

    op.create_table(
        "paper_contents",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("paper_id", sa.UUID(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["paper_id"], ["papers.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("paper_id"),
    )
    op.create_table(
        "paper_chunks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("paper_content_id", sa.UUID(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("section", sa.Text(), nullable=True),
        sa.Column("embedding", Vector(3072), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["paper_content_id"], ["paper_contents.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("paper_content_id", "chunk_index", name="uq_paper_content_chunk_index"),
    )
    op.create_index(
        op.f("ix_paper_chunks_paper_content_id"),
        "paper_chunks",
        ["paper_content_id"],
        unique=False,
    )
