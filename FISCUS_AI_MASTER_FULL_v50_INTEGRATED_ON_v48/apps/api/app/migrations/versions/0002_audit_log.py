from alembic import op
import sqlalchemy as sa

revision = '0002_audit_log'
down_revision = '0001_init'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'auditlog',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ts', sa.DateTime, nullable=False, index=True),
        sa.Column('actor', sa.String(length=255), nullable=False, index=True),
        sa.Column('role', sa.String(length=64), nullable=False, index=True),
        sa.Column('action', sa.String(length=255), nullable=False, index=True),
        sa.Column('target', sa.String(length=1024), nullable=False, index=True),
        sa.Column('meta', sa.Text, nullable=False)
    )

def downgrade():
    op.drop_table('auditlog')