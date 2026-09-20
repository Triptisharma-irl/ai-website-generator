import os
import json
from http.server import BaseHTTPRequestHandler
import google.generativeai as genai

SYSTEM_PROMPT = """You are an expert web designer and front-end developer.
Given a description of a website, generate a single, complete, self-contained
HTML file that implements it.

Rules:
- Output ONLY the raw HTML. No explanation, no markdown code fences, no commentary.
- Put all CSS in a <style> tag in the <head>. Put all JavaScript in a <script> tag before </body>.
- Do not reference any external files, images, or stylesheets other than Google Fonts.
- Make it visually polished: thoughtful typography, spacing, and color choices
  appropriate to the subject matter. Avoid generic templated-looking design.
- Make it responsive and usable on mobile.
- The result must render correctly as a standalone .html file with no build step.
"""


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = json.loads(self.rfile.read(content_length))
            prompt = body.get("prompt", "").strip()

            if not prompt:
                self._send_json(400, {"error": "Prompt is required."})
                return

            api_key = os.environ.get("GEMINI_API_KEY")
            if not api_key:
                self._send_json(500, {"error": "Server is missing GEMINI_API_KEY."})
                return

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="gemini-3.6-flash",
                system_instruction=SYSTEM_PROMPT,
            )
            response = model.generate_content(prompt)
            html_out = response.text.strip()

            if html_out.startswith("```"):
                html_out = html_out.split("\n", 1)[1]
            if html_out.endswith("```"):
                html_out = html_out.rsplit("```", 1)[0]

            self._send_json(200, {"html": html_out})

        except Exception as e:
            self._send_json(500, {"error": str(e)})

    def _send_json(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
