"""initial migration

Revision ID: 001
Revises:
Create Date: 2024-02-12 06:30:14.856

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Create the truck_history table
    op.create_table(
        'truck_history',
        sa.Column('id', sa.String(50), nullable=False),
        sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('latitude', sa.Float(), nullable=False),
        sa.Column('longitude', sa.Float(), nullable=False),
        sa.Column('speed', sa.Float(), nullable=False),
        sa.Column('fuel_level', sa.Float(), nullable=False),
        sa.Column('engine_status', sa.String(20), nullable=False),
        sa.Column('running_time', sa.Integer(), nullable=False),
        sa.Column('miles_accumulated', sa.Float(), nullable=False),
    )

    # Create hypertable and index
    op.execute("""
        SELECT create_hypertable('truck_history', 'timestamp', if_not_exists => TRUE);
        CREATE INDEX IF NOT EXISTS idx_truck_history_id_time ON truck_history (id, timestamp DESC);
    """)

def downgrade() -> None:
    op.drop_table('truck_history')
