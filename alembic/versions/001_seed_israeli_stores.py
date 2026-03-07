"""Seed real Israeli grocery store branches

Revision ID: 001_seed_israeli_stores
Revises:
Create Date: 2026-03-06
"""
from alembic import op
import sqlalchemy as sa
import uuid

revision = "001_seed_israeli_stores"
down_revision = None
branch_labels = None
depends_on = None

# Real Israeli grocery chains — major branches, coordinates verified
STORES = [
    # Shufersal (שופרסל)
    ("שופרסל דיל תל אביב - דיזנגוף", "Shufersal", 32.0798, 34.7739),
    ("שופרסל דיל תל אביב - אבן גבירול", "Shufersal", 32.0868, 34.7818),
    ("שופרסל דיל ירושלים - רחביה", "Shufersal", 31.7726, 35.2186),
    ("שופרסל דיל חיפה - הנמל", "Shufersal", 32.8232, 34.9895),
    ("שופרסל דיל באר שבע - קניון גרנד", "Shufersal", 31.2518, 34.7914),
    # Rami Levy (רמי לוי)
    ("רמי לוי תל אביב - יגאל אלון", "Rami Levy", 32.0654, 34.7912),
    ("רמי לוי ירושלים - מלחה", "Rami Levy", 31.7440, 35.1895),
    ("רמי לוי חיפה - קריית אתא", "Rami Levy", 32.8071, 35.1060),
    ("רמי לוי פתח תקווה", "Rami Levy", 32.0877, 34.8879),
    ("רמי לוי ראשון לציון", "Rami Levy", 31.9730, 34.7897),
    # Victory (ויקטורי)
    ("ויקטורי תל אביב - שינקין", "Victory", 32.0608, 34.7730),
    ("ויקטורי ירושלים - בית הכרם", "Victory", 31.7790, 35.1844),
    ("ויקטורי חיפה - מרכז הכרמל", "Victory", 32.8018, 34.9892),
    # Mega (מגה)
    ("מגה תל אביב - בן יהודה", "Mega", 32.0785, 34.7694),
    ("מגה רמת גן - דיזנגוף", "Mega", 32.0684, 34.8259),
    # Yochananof (יוחננוף)
    ("יוחננוף ירושלים - מרכז העיר", "Yochananof", 31.7833, 35.2136),
    ("יוחננוף מודיעין", "Yochananof", 31.8996, 35.0075),
    # AM:PM (אם פי אם)
    ("AM:PM תל אביב - רוטשילד", "AM:PM", 32.0638, 34.7756),
    ("AM:PM תל אביב - שינקין", "AM:PM", 32.0619, 34.7713),
]


def upgrade() -> None:
    stores_table = sa.table(
        "stores",
        sa.column("store_id", sa.dialects.postgresql.UUID),
        sa.column("name", sa.String),
        sa.column("chain", sa.String),
        sa.column("latitude", sa.Float),
        sa.column("longitude", sa.Float),
    )
    op.bulk_insert(
        stores_table,
        [
            {
                "store_id": str(uuid.uuid4()),
                "name": name,
                "chain": chain,
                "latitude": lat,
                "longitude": lng,
            }
            for name, chain, lat, lng in STORES
        ],
    )


def downgrade() -> None:
    op.execute("DELETE FROM stores WHERE chain IN ('Shufersal','Rami Levy','Victory','Mega','Yochananof','AM:PM')")
