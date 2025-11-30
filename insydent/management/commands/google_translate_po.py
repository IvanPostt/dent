import os
import polib
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from google.cloud import translate

class Command(BaseCommand):
    help = 'Translates .po files using Google Cloud Translation API.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--language',
            dest='language',
            default=None,
            help='Specify the language to translate (e.g., en)',
        )
        parser.add_argument(
            '--project-id',
            dest='project_id',
            default=None,
            help='Your Google Cloud Project ID.',
        )

    def handle(self, *args, **options):
        project_id = options['project_id']
        if not project_id:
            raise CommandError("Please provide your Google Cloud Project ID using --project-id.")

        # Путь к файлу JSON-ключа учетных данных Google Cloud
        # Рекомендуется установить переменную окружения GOOGLE_APPLICATION_CREDENTIALS
        # Или указать путь напрямую, как показано ниже (менее безопасно для продакшена)
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

        client = translate.TranslationServiceClient()

        target_language = options['language']
        if not target_language:
            raise CommandError("Please specify a target language using --language (e.g., --language en).")

        # Пути к локалям
        locale_paths = [
            os.path.join(app_config.path, 'locale')
            for app_config in settings.APPS_CONFIGS
            if os.path.isdir(os.path.join(app_config.path, 'locale'))
        ] + list(settings.LOCALE_PATHS)

        po_files_found = False
        for locale_path in locale_paths:
            lang_path = os.path.join(locale_path, target_language, 'LC_MESSAGES')
            po_file_path = os.path.join(lang_path, 'django.po')

            if os.path.exists(po_file_path):
                po_files_found = True
                self.stdout.write(self.style.SUCCESS(f"Processing {po_file_path} for language {target_language}..."))
                po = polib.pofile(po_file_path)

                translated_count = 0
                for entry in po.untranslated_entries():
                    if entry.msgid and not entry.msgstr:
                        try:
                            response = client.translate_text(
                                parent=f"projects/{project_id}",
                                contents=[entry.msgid],
                                target_language_code=target_language,
                                source_language_code=settings.LANGUAGE_CODE, # Исходный язык из настроек Django (ru)
                            )
                            entry.msgstr = response.translations[0].translated_text
                            translated_count += 1
                            self.stdout.write(f"  Translated '{entry.msgid}' to '{entry.msgstr}'")
                        except Exception as e:
                            self.stderr.write(self.style.ERROR(f"  Google Cloud Translation API error for '{entry.msgid}': {e}"))
                            break # Прерываем, если API выдал ошибку

                if translated_count > 0:
                    po.save()
                    self.stdout.write(self.style.SUCCESS(f"Successfully translated {translated_count} entries in {po_file_path}."))
                else:
                    self.stdout.write(self.style.WARNING(f"No untranslated entries found in {po_file_path} for language {target_language}."))
            else:
                self.stdout.write(self.style.WARNING(f"'django.po' not found at {po_file_path}."))

        if not po_files_found:
            raise CommandError(f"No .po files found for language {target_language} in configured locale paths.")

