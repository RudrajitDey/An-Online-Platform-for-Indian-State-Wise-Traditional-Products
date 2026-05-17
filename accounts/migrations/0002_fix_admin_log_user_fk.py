from django.db import migrations


def rebuild_admin_log_table(apps, schema_editor):
    if schema_editor.connection.vendor != 'sqlite':
        return

    with schema_editor.connection.cursor() as cursor:
        cursor.execute('PRAGMA foreign_keys=OFF')
        cursor.execute(
            '''
            CREATE TABLE "django_admin_log_new" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "object_id" text NULL,
                "object_repr" varchar(200) NOT NULL,
                "action_flag" smallint unsigned NOT NULL
                    CHECK ("action_flag" >= 0),
                "change_message" text NOT NULL,
                "content_type_id" integer NULL
                    REFERENCES "django_content_type" ("id")
                    DEFERRABLE INITIALLY DEFERRED,
                "user_id" integer NOT NULL
                    REFERENCES "accounts_account" ("id")
                    DEFERRABLE INITIALLY DEFERRED,
                "action_time" datetime NOT NULL
            )
            '''
        )
        cursor.execute(
            '''
            INSERT INTO "django_admin_log_new" (
                "id", "object_id", "object_repr", "action_flag",
                "change_message", "content_type_id", "user_id", "action_time"
            )
            SELECT
                log."id", log."object_id", log."object_repr", log."action_flag",
                log."change_message", log."content_type_id", log."user_id", log."action_time"
            FROM "django_admin_log" AS log
            WHERE log."user_id" IN (SELECT "id" FROM "accounts_account")
            '''
        )
        cursor.execute('DROP TABLE "django_admin_log"')
        cursor.execute('ALTER TABLE "django_admin_log_new" RENAME TO "django_admin_log"')
        cursor.execute('PRAGMA foreign_keys=ON')


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(rebuild_admin_log_table, migrations.RunPython.noop),
    ]
