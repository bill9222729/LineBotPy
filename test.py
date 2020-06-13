from alembic import op
from sqlalchemy import Column, String, Boolean

op.add_column('user',
              Column(Boolean, nullable=False, default=False)
              )
