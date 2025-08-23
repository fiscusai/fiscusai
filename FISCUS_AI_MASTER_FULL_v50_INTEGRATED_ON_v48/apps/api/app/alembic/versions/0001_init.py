from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('customer',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('external_id', sa.String, nullable=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=True),
        sa.Column('tax_id', sa.String, nullable=True),
        sa.Column('organization_id', sa.String, nullable=True),
    )
    op.create_table('invoice',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('number', sa.String, nullable=False),
        sa.Column('customer', sa.String, nullable=False),
        sa.Column('date', sa.Date, nullable=False),
        sa.Column('total', sa.Float, nullable=False),
        sa.Column('vat', sa.Float, nullable=False),
        sa.Column('currency', sa.String, nullable=False),
        sa.Column('organization_id', sa.String, nullable=True),
    )

def downgrade():
    op.drop_table('invoice')
    op.drop_table('customer')
