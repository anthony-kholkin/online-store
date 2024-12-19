"""Init models

Revision ID: 43ce38fec735
Revises:
Create Date: 2024-11-19 22:12:29.436083

"""

from alembic import op
import sqlalchemy as sa

import db

# revision identifiers, used by Alembic.
revision: str | None = "43ce38fec735"
down_revision: str | None = None
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "carts",
        sa.Column("cart_outlet_guid", sa.String(length=255), nullable=False),
        sa.PrimaryKeyConstraint("cart_outlet_guid", name=op.f("carts_pkey")),
    )
    op.create_table(
        "good_groups",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("parent_group_guid", sa.String(length=255), nullable=True),
        sa.Column("guid", db.models.mixins.GUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["parent_group_guid"], ["good_groups.guid"], name=op.f("good_groups_parent_group_guid_fkey")
        ),
        sa.PrimaryKeyConstraint("guid", name=op.f("good_groups_pkey")),
    )
    op.create_table(
        "price_types",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("guid", db.models.mixins.GUID(), nullable=False),
        sa.PrimaryKeyConstraint("guid", name=op.f("price_types_pkey")),
    )
    op.create_table(
        "specifications",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("guid", db.models.mixins.GUID(), nullable=False),
        sa.PrimaryKeyConstraint("guid", name=op.f("specifications_pkey")),
    )
    op.create_table(
        "goods",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("type", sa.Enum("NEW", "HIT", "REGULAR", name="goodtypesenum"), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("filling", sa.String(length=255), nullable=True),
        sa.Column("aroma", sa.String(length=255), nullable=True),
        sa.Column("strength", sa.String(length=255), nullable=True),
        sa.Column("format", sa.String(length=255), nullable=True),
        sa.Column("manufacturing_method", sa.String(length=255), nullable=False),
        sa.Column("package", sa.String(length=255), nullable=True),
        sa.Column("block", sa.String(length=255), nullable=True),
        sa.Column("box", sa.String(length=255), nullable=True),
        sa.Column("producing_country", sa.String(length=255), nullable=True),
        sa.Column("image_key", sa.Text(), nullable=True),
        sa.Column("good_group_guid", sa.String(length=255), nullable=False),
        sa.Column("guid", db.models.mixins.GUID(), nullable=False),
        sa.ForeignKeyConstraint(["good_group_guid"], ["good_groups.guid"], name=op.f("goods_good_group_guid_fkey")),
        sa.PrimaryKeyConstraint("guid", name=op.f("goods_pkey")),
    )
    op.create_table(
        "good_specifications",
        sa.Column("good_guid", db.models.mixins.GUID(), nullable=False),
        sa.Column("specification_guid", db.models.mixins.GUID(), nullable=False),
        sa.ForeignKeyConstraint(["good_guid"], ["goods.guid"], name=op.f("good_specifications_good_guid_fkey")),
        sa.ForeignKeyConstraint(
            ["specification_guid"], ["specifications.guid"], name=op.f("good_specifications_specification_guid_fkey")
        ),
        sa.PrimaryKeyConstraint("good_guid", "specification_guid", name=op.f("good_specifications_pkey")),
    )
    op.create_table(
        "good_storages",
        sa.Column("in_stock", sa.Integer(), nullable=False),
        sa.Column("good_guid", sa.String(length=255), nullable=False),
        sa.Column("specification_guid", sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(["good_guid"], ["goods.guid"], name=op.f("good_storages_good_guid_fkey")),
        sa.ForeignKeyConstraint(
            ["specification_guid"], ["specifications.guid"], name=op.f("good_storages_specification_guid_fkey")
        ),
        sa.PrimaryKeyConstraint("good_guid", "specification_guid", name=op.f("good_storages_pkey")),
    )
    op.create_table(
        "prices",
        sa.Column("good_guid", sa.String(length=255), nullable=False),
        sa.Column("specification_guid", sa.String(length=255), nullable=False),
        sa.Column("price_type_guid", sa.String(length=255), nullable=False),
        sa.Column("value", sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(["good_guid"], ["goods.guid"], name=op.f("prices_good_guid_fkey")),
        sa.ForeignKeyConstraint(["price_type_guid"], ["price_types.guid"], name=op.f("prices_price_type_guid_fkey")),
        sa.ForeignKeyConstraint(
            ["specification_guid"], ["specifications.guid"], name=op.f("prices_specification_guid_fkey")
        ),
        sa.PrimaryKeyConstraint(
            "good_guid", "specification_guid", "price_type_guid", name="good_spec_price_type_constraint"
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("prices")
    op.drop_table("good_storages")
    op.drop_table("good_specifications")
    op.drop_table("goods")
    op.drop_table("specifications")
    op.drop_table("price_types")
    op.drop_table("good_groups")
    op.drop_table("carts")
    # ### end Alembic commands ###
