from alembic import op
import sqlalchemy as sa

revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # örnek tablo
    op.create_table(
        'health_check',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ts', sa.DateTime, nullable=False)
    )

def downgrade():
    op.drop_table('health_check')