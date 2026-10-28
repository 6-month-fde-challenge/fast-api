
from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import json

# Usage:
# python test_cors.py 5500
# Defaults to port 5500
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5500


class Handler(BaseHTTPRequestHandler):

    def do_GET(self):
        html = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>CORS Test</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 30px;
                }

                input {
                    padding: 8px;
                    width: 280px;
                    margin: 5px 0 15px;
                }

                button {
                    padding: 10px 18px;
                    cursor: pointer;
                }

                #result {
                    margin-top: 20px;
                    font-size: 16px;
                    white-space: pre-wrap;
                }
            </style>
        </head>

        <body>
            <h2>CORS Test Client</h2>

            <p><b>Frontend:</b> <span id="frontend"></span></p>

            <label for="backend">Backend URL:</label><br>
            <input
                id="backend"
                type="text"
                value="http://localhost:5000"
            ><br>

            <label for="endpoint">API endpoint:</label><br>
            <input
                id="endpoint"
                type="text"
                value="/test-cors"
            ><br>

            <button onclick="testCORS()">Test API</button>

            <p id="result">Enter the backend URL and click Test API.</p>

            <script>
                document.getElementById("frontend").textContent =
                    window.location.origin;

                async function testCORS() {
                    const result = document.getElementById("result");
                    const backend = document.getElementById("backend")
                        .value.trim().replace(/\\/$/, "");
                    const endpoint = document.getElementById("endpoint")
                        .value.trim();

                    const url = backend + (
                        endpoint.startsWith("/") ? endpoint : "/" + endpoint
                    );

                    result.textContent = "Calling " + url + "...";

                    try {
                        const response = await fetch(url);

                        const body = await response.text();

                        if (!response.ok) {
                            throw new Error(
                                "HTTP " + response.status + ": " + body
                            );
                        }

                        let data;
                        try {
                            data = JSON.parse(body);
                        } catch {
                            throw new Error(
                                "Expected JSON but received: " +
                                body.substring(0, 200)
                            );
                        }

                        result.textContent =
                            "SUCCESS\\nURL: " + url +
                            "\\nStatus: " + response.status +
                            "\\nResponse:\\n" +
                            JSON.stringify(data, null, 2);

                    } catch (error) {
                        result.textContent =
                            "FAILED\\nURL: " + url +
                            "\\nError: " + error.message +
                            "\\nCheck backend availability and CORS settings.";
                    }
                }
            </script>
        </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))


if __name__ == "__main__":
    server = HTTPServer(("localhost", PORT), Handler)

    print(f"Frontend running at http://localhost:{PORT}")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nFrontend server stopped.")
    finally:
        server.server_close()
