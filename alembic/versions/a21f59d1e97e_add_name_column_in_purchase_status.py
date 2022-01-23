"""add name column in purchase_status

Revision ID: a21f59d1e97e
Revises: 0b3e71986e87
Create Date: 2022-01-22 11:28:43.901362

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "a21f59d1e97e"
down_revision = "0b3e71986e87"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "purchase_status", sa.Column("name", sa.String(), nullable=True)
    )
    op.drop_index(
        "ix_purchase_status_description", table_name="purchase_status"
    )
    op.create_index(
        op.f("ix_purchase_status_name"),
        "purchase_status",
        ["name"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_purchase_status_name"), table_name="purchase_status"
    )
    op.create_index(
        "ix_purchase_status_description",
        "purchase_status",
        ["description"],
        unique=False,
    )
    op.drop_column("purchase_status", "name")
    # ### end Alembic commands ###
