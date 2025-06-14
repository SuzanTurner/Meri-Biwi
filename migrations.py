
from alembic import command
from alembic.config import Config
from datetime import datetime

def migrate_and_upgrade(message="auto migration"):
    alembic_cfg = Config("alembic.ini")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    migration_message = f"{timestamp}_{message.replace(' ', '_')}"

    print("🚀 Generating migration...")
    command.revision(config=alembic_cfg, message=migration_message, autogenerate=True)

    print("🔼 Applying migration...")
    command.upgrade(alembic_cfg, "head")

    print(f"✅ Migration '{migration_message}' generated and applied.")

if __name__ == "__main__":
    migrate_and_upgrade()
