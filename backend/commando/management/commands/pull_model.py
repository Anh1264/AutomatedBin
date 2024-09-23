import helpers_folder
from django.conf import settings
from typing import Any
from django.core.management.base import BaseCommand
from pathlib import Path

AI_MODEL_DIR = getattr(settings, 'AI_MODEL_DIR')

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any):
        self.stdout.write("Downloading keras model")
        # model_url = "https://github.com/Anh1264/AutomatedBin/blob/efefafb917d6b686d0791e33ec89fcaf4dc68049/backend/AI_model/biio.keras"  # Replace with the actual URL
        model_url = "https://drive.google.com/uc?export=download&id=1m_Bmm569ml25H5Ndz6V0IpKfW0HA1Lw-"
        model_path = AI_MODEL_DIR / 'biio.keras' # Adjust if needed
        dl_success= helpers_folder.download_to_local(model_url, model_path)

        if dl_success:
            self.stdout.write(
                self.style.SUCCESS(f"Successfully downloaded keras model!")
            )
        else:
            self.stdout.write(
                self.style.ERROR(f'Failed to download {model_url}')
            )
            