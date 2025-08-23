from alembic import op
import sqlalchemy as sa

revision = '0003_users'
down_revision = '0002_audit_log'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'user',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('sub', sa.String(length=255), nullable=False, index=True, unique=True),
        sa.Column('role', sa.String(length=64), nullable=False, index=True),
        sa.Column('ts', sa.DateTime, nullable=False, index=True)
    )

def downgrade():
    op.drop_table('user')