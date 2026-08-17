import re

class CodeDecompiler:
    def __init__(self, file_path, detected_info):
        self.file_path = file_path
        self.detected_info = detected_info

    def process_deobfuscation(self):
        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            code_content = f.read()

        file_type = self.detected_info.get("detected_type", "")

        if "JavaScript" in file_type:
            return self._clean_javascript(code_content)
        elif "Base64" in file_type:
            return self._clean_base64(code_content)
        else:
            # General cleanup for generic text/code
            return self._general_cleanup(code_content)

    def _clean_javascript(self, content):
        # Basic JavaScript deobfuscation / formatting placeholders
        # Yahan hum AST-based transformations ya pattern replacements kar sakte hain
        cleaned = content.replace("eval(", "console.log('Unwrapped eval: ', ")
        return {
            "status": "Success",
            "message": "JavaScript pattern processed and cleaned.",
            "clean_code": cleaned
        }

    def _clean_base64(self, content):
        import base64
        try:
            decoded_bytes = base64.b64decode(content.strip())
            decoded_text = decoded_bytes.decode('utf-8', errors='ignore')
            return {
                "status": "Success",
                "message": "Base64 payload successfully decoded.",
                "clean_code": decoded_text
            }
        except Exception as e:
            return {
                "status": "Failed",
                "message": f"Base64 decoding error: {str(e)}",
                "clean_code": content
            }

    def _general_cleanup(self, content):
        # Extra spaces aur unnecessary comments hatane ke liye
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        return {
            "status": "Success",
            "message": "General source cleanup applied.",
            "clean_code": "\n".join(lines)
        }