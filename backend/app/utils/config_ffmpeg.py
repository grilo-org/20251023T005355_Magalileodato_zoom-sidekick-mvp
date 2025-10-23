"""
config_ffmpeg.py - Configuração do ffmpeg para PyDub
----------------------------------------------------
Garante que PyDub utilize o ffmpeg fornecido pelo imageio-ffmpeg,
evitando warnings de "Couldn't find ffmpeg".
"""

import warnings
from pydub import AudioSegment
import imageio_ffmpeg as ffmpeg

# ⚠️ Ignora warning do PyDub sobre ffmpeg
warnings.filterwarnings("ignore", message="Couldn't find ffmpeg or avconv.*")

# Força o PyDub a usar o executável do imageio-ffmpeg
AudioSegment.converter = ffmpeg.get_ffmpeg_exe()

print(f"[INFO] PyDub configurado para usar ffmpeg em: {AudioSegment.converter}")
