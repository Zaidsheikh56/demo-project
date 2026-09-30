"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-09-29

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

customer_status = postgresql.ENUM(
    "lead", "confirmed", "in_progress", "completed", "cancelled",
    name="customerstatus",
)
event_type = postgresql.ENUM(
    "engagement", "haldi", "sangeet", "wedding", "reception", "other",
    name="eventtype",
)


def upgrade() -> None:
    bind = op.get_bind()
    customer_status.create(bind, checkfirst=True)
    event_type.create(bind, checkfirst=True)

    op.create_table(
        "customers",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("phone", sa.String(20), nullable=False),
        sa.Column("email", sa.String(120), nullable=True),
        sa.Column("partner_name", sa.String(120), nullable=True),
        sa.Column("event_type", event_type, nullable=False, server_default="wedding"),
        sa.Column("event_date", sa.Date(), nullable=True),
        sa.Column("venue", sa.String(200), nullable=True),
        sa.Column("guest_count", sa.String(20), nullable=True),
        sa.Column("budget", sa.Numeric(12, 2), nullable=True),
        sa.Column("status", customer_status, nullable=False, server_default="lead"),
        sa.Column("source", sa.String(80), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "payments",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("amount", sa.Numeric(12, 2), nullable=False),
        sa.Column("method", sa.String(40), nullable=True),
        sa.Column("paid_on", sa.Date(), nullable=False, server_default=sa.func.current_date()),
        sa.Column("remarks", sa.String(200), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "notes",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("customer_id", postgresql.UUID(as_uuid=True),
                   sa.ForeignKey("customers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_index("ix_customers_name", "customers", ["name"])
    op.create_index("ix_customers_phone", "customers", ["phone"])
    op.create_index("ix_payments_customer_id", "payments", ["customer_id"])
    op.create_index("ix_notes_customer_id", "notes", ["customer_id"])


def downgrade() -> None:
    op.drop_table("notes")
    op.drop_table("payments")
    op.drop_table("customers")
    customer_status.drop(op.get_bind(), checkfirst=True)
    event_type.drop(op.get_bind(), checkfirst=True)
