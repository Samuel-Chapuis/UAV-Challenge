import subprocess
import sys

def open_labelimg():
    try:
        subprocess.run(["labelImg"], check=True)
    except FileNotFoundError:
        print("❌ LabelImg n'est pas installé. Installation en cours...")
        subprocess.run([sys.executable, "-m", "pip", "install", "labelImg"])
        print("✅ Installation terminée. Lancement de LabelImg...")
        subprocess.run(["labelImg"])

if __name__ == "__main__":
    open_labelimg()
