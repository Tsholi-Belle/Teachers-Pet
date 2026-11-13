#!/usr/bin/env python3
"""
Teacher's Pet Web Server & Orchestrator.
Provides REST and event streaming APIs for the 6-stage multi-agent workflow:
01 Goal -> 02 Plan -> 03 Act -> 04 Check -> 05 Correct -> 06 Deliver.
Zero external dependencies, uses standard Python http.server.
"""

import http.server
import socketserver
import json
import os
import sys
import urllib.parse
from typing import Dict, Any

# Ensure project root is in python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from curriculum_colleague.workflow import CurriculumColleagueWorkflow
from curriculum_colleague.verification.fact_checker import FactChecker


class CurriculumRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Serve static directory
        super().__init__(*args, directory=os.path.join(BASE_DIR, "static"), **kwargs)

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/status":
            self._send_json({"status": "running", "service": "Teacher's Pet", "version": "1.0.0"})
        elif parsed.path == "/api/standards":
            checker = FactChecker()
            self._send_json({"curricula": checker.curricula})
        else:
            # Fallback to static files
            super().do_GET()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        content_len = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_len).decode("utf-8") if content_len > 0 else "{}"
        
        try:
            req_json = json.loads(post_data)
        except Exception:
            req_json = {}

        if parsed.path == "/api/run":
            goal = req_json.get("goal", "Grade 7 Natural Sciences: Photosynthesis & Food Chains for 45 students in public school")
            force_correction = req_json.get("force_correction", False)

            events = []
            def record_event(evt):
                events.append(evt)

            workflow = CurriculumColleagueWorkflow(on_event=record_event)
            bundle = workflow.run(user_goal=goal, force_correction_demo=force_correction)

            response = {
                "success": True,
                "events": events,
                "bundle": bundle
            }
            self._send_json(response)

        elif parsed.path == "/api/verify":
            plan = req_json.get("plan", {})
            checker = FactChecker()
            audit = checker.verify_lesson_plan(plan)
            self._send_json({"success": True, "audit": audit})

        else:
            self.send_error(404, "Endpoint not found")

    def _send_json(self, data: Dict[str, Any], status: int = 200):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()


def start_server(port: int = 8080):
    handler = CurriculumRequestHandler
    # Allow port reuse
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"Teacher's Pet Server running at http://localhost:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    start_server(port)
