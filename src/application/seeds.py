import binascii
import os
from pathlib import Path

from fastapi.logger import logger

from src.infrastructure.database import db
from src.infrastructure.repository.accounts.utils import hash_password


async def seed_database():
    await _add_initial_admin_account()
    create_secret_file()


async def _add_initial_admin_account():
    count = await db.fetch_val("SELECT COUNT(*) FROM account.account WHERE is_admin")
    if count == 0:
        logger.info("Adding default admin account. Please change the credentials ASAP!")

        await db.execute("""
        INSERT INTO account.account (username, password, email, is_admin)
        VALUES (:username, :password, :email, TRUE)
        """, {'username': 'admin', 'password': hash_password("admin", "ABCDE"), 'email': 'daniel.bok@outlook.com'})


def create_secret_file():
    secret_folder = Path(__file__).parents[3] / "tmp"
    if not secret_folder.exists():
        secret_folder.mkdir(parents=True, exist_ok=True)

    file = secret_folder / "secret.txt"
    if not file.exists():
        secret = binascii.b2a_hex(os.urandom(128)).decode()
        with open(file, 'w') as f:
            logger.info(f"Creating secret file at {file}")
            f.write(secret)
