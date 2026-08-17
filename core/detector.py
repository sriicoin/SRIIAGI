import os

class ObfuscationDetector:
    def __init__(self, file_path):
        self.file_path = file_path

    def analyze_file(self):
        if not os.path.exists(self.file_path):
            return {"error": "File not found"}

        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(2000) # Shuruwati 2000 characters read karenge pattern ke liye

        # Detection logic based on signatures/patterns
        detection_result = {
            "file_size": os.path.getsize(self.file_path),
            "detected_type": "Unknown / Standard Source",
            "indicators": []
        }

        # 1. Check for JavaScript Obfuscation (e.g., _0x hex variables)
        if "_0x" in content or "eval(function(p,a,c,k,e,d)" in content:
            detection_result["detected_type"] = "Obfuscated JavaScript (Packed/Minified)"
            detection_result["indicators"].append("Hex-encoded variable patterns (_0x...) or Packer found.")

        # 2. Check for Base64 pattern
        elif self._is_likely_base64(content.strip()):
            detection_result["detected_type"] = "Base64 Encoded Payload"
            detection_result["indicators"].append("High density of Base64 character sets.")

        # 3. Check for Python Bytecode / Compiled markers
        elif content.startswith("PK") or self.file_path.endswith(('.pyc', '.class', '.exe')):
            detection_result["detected_type"] = "Compiled Binary / Bytecode"
            detection_result["indicators"].append("Binary file header detected.")

        else:
            detection_result["detected_type"] = "Standard Code / Plain Text"
            detection_result["indicators"].append("No heavy obfuscation patterns recognized instantly.")

        return detection_result

    def _is_likely_base64(self, s):
        if len(s) % 4 == 0 and len(s) > 20:
            import re
            return bool(re.match(r'^[A-Za-z0-9+/]+={0,2}$', s))
        return False