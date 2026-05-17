from django.db import migrations


def rebuild_vendor_table(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute('PRAGMA foreign_keys=OFF')
        cursor.execute(
            '''
            CREATE TABLE "shop_vendor_new" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "shop_name" varchar(255) NOT NULL,
                "owner_name" varchar(255) NOT NULL,
                "phone" varchar(15) NOT NULL,
                "email" varchar(254) NOT NULL,
                "gst_number" varchar(20) NOT NULL UNIQUE,
                "drug_license_number" varchar(50) NOT NULL UNIQUE,
                "gst_certificate" varchar(100) NOT NULL,
                "drug_license_file" varchar(100) NOT NULL,
                "id_proof" varchar(100) NOT NULL,
                "address" text NOT NULL,
                "city" varchar(100) NOT NULL,
                "state" varchar(100) NOT NULL,
                "pincode" varchar(100) NOT NULL,
                "status" varchar(10) NOT NULL,
                "is_active" bool NOT NULL,
                "created_at" datetime NOT NULL,
                "user_id" bigint NOT NULL UNIQUE
                    REFERENCES "accounts_account" ("id")
                    DEFERRABLE INITIALLY DEFERRED
            )
            '''
        )
        cursor.execute(
            '''
            INSERT INTO "shop_vendor_new" (
                "id", "shop_name", "owner_name", "phone", "email",
                "gst_number", "drug_license_number", "gst_certificate",
                "drug_license_file", "id_proof", "address", "city", "state",
                "pincode", "status", "is_active", "created_at", "user_id"
            )
            SELECT
                "id", "shop_name", "owner_name", "phone", "email",
                "gst_number", "drug_license_number", "gst_certificate",
                "drug_license_file", "id_proof", "address", "city", "state",
                "pincode", "status", "is_active", "created_at", "user_id"
            FROM "shop_vendor"
            '''
        )
        cursor.execute('DROP TABLE "shop_vendor"')
        cursor.execute('ALTER TABLE "shop_vendor_new" RENAME TO "shop_vendor"')
        cursor.execute('PRAGMA foreign_keys=ON')


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_vendor_user'),
    ]

    operations = [
        migrations.RunPython(rebuild_vendor_table, migrations.RunPython.noop),
    ]
