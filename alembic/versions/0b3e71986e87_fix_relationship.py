"""fix relationship

Revision ID: 0b3e71986e87
Revises: 11558fbe6d88
Create Date: 2022-01-22 10:51:34.890371

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "0b3e71986e87"
down_revision = "11558fbe6d88"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "purchase_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_purchase_status_description"),
        "purchase_status",
        ["description"],
        unique=False,
    )
    op.create_index(
        op.f("ix_purchase_status_id"), "purchase_status", ["id"], unique=False
    )
    op.create_table(
        "user",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("full_name", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("cpf", sa.String(length=11), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_cpf"), "user", ["cpf"], unique=True)
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(
        op.f("ix_user_full_name"), "user", ["full_name"], unique=False
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_table(
        "purchase",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("code", sa.String(), nullable=True),
        sa.Column("value", sa.Numeric(), nullable=False),
        sa.Column("date", sa.Date(), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=True),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("time_created", sa.DateTime(), nullable=False),
        sa.Column("time_updated", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["purchase_status.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_purchase_code"), "purchase", ["code"], unique=False
    )
    op.create_index(op.f("ix_purchase_id"), "purchase", ["id"], unique=False)
    op.create_index(
        op.f("ix_purchase_value"), "purchase", ["value"], unique=True
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_purchase_value"), table_name="purchase")
    op.drop_index(op.f("ix_purchase_id"), table_name="purchase")
    op.drop_index(op.f("ix_purchase_code"), table_name="purchase")
    op.drop_table("purchase")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_full_name"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_index(op.f("ix_user_cpf"), table_name="user")
    op.drop_table("user")
    op.drop_index(op.f("ix_purchase_status_id"), table_name="purchase_status")
    op.drop_index(
        op.f("ix_purchase_status_description"), table_name="purchase_status"
    )
    op.drop_table("purchase_status")
    # ### end Alembic commands ###
