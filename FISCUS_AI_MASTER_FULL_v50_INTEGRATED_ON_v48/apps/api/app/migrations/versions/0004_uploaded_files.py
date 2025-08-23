from alembic import op
import sqlalchemy as sa

revision = '0004_uploaded_files'
down_revision = '0003_users'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'uploadedfile',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('key', sa.String(length=1024), nullable=False, unique=True, index=True),
        sa.Column('owner_sub', sa.String(length=255), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime, nullable=False, index=True),
        sa.Column('status', sa.String(length=32), nullable=False, index=True),
        sa.Column('size', sa.Integer, nullable=True),
        sa.Column('mime', sa.String(length=255), nullable=True)
    )

def downgrade():
    op.drop_table('uploadedfile')