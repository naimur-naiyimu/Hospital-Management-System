from whitenoise.storage import CompressedManifestStaticFilesStorage
from django.contrib.staticfiles.storage import StaticFilesStorage

class CustomStaticFilesStorage(CompressedManifestStaticFilesStorage):
    def _post_process(self, paths, dry_run=False, **options):
        try:
            return super()._post_process(paths, dry_run, **options)
        except Exception as e:
            # Ignore the specific error for jquery-ui.css
            if "jquery-ui.css" in str(e):
                print(f"Ignoring post-processing error: {e}")
                return []
            raise  # Raise the error if it's not related to jquery-ui.css
