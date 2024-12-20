"""Add index on goods.good_group_guid

Revision ID: 3e776fcbe9dc
Revises: fc5dc36adf48
Create Date: 2024-12-05 20:29:06.550572

"""

from alembic import op


# revision identifiers, used by Alembic.
revision: str | None = "3e776fcbe9dc"
down_revision: str | None = "fc5dc36adf48"
branch_labels: str | None = None
depends_on: str | None = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f("goods_good_group_guid_idx"), "goods", ["good_group_guid"], unique=False)
    op.create_index("ix_goods_good_group_guid", "goods", ["good_group_guid"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_goods_good_group_guid", table_name="goods")
    op.drop_index(op.f("goods_good_group_guid_idx"), table_name="goods")
    # ### end Alembic commands ###
