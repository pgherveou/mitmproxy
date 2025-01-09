from mitmproxy import http
import logging
import os

class JSONRPCMethodColumn:
    def load(self, loader):
        # Add a custom column to the flows view
        loader.add_option(
            name="json_rpc_method",
            typespec=str,
            default="",
            help="Display JSON-RPC method"
        )

    def request(self, flow: http.HTTPFlow):
        if flow.request.headers.get("Content-Type") == "application/json":
            try:
                # Extract JSON-RPC method from the request body
                json_data = flow.request.json()
                if "method" in json_data:
                    flow.metadata["path"] = json_data["method"] 
            except ValueError:
                # If the body is not JSON, ignore
                pass

    def response(self, flow: http.HTTPFlow):
        if flow.request.headers.get("Json-Rpc-Method"):
            flow.response.headers["Json-Rpc-Method"] = flow.request.headers["Json-Rpc-Method"]

addons = [
    JSONRPCMethodColumn()
]

# Configure logging
logging.basicConfig(filename='requests.log', level=logging.INFO, format='%(asctime)s - %(message)s')
FORWARD_PORT = int(os.getenv('FORWARD_PORT', "8545"))

def request(flow: http.HTTPFlow) -> None:
    logging.info(f"Request URL: {flow.request.pretty_url}")
    logging.info(f"Request Method: {flow.request.method}")
    logging.info(f"Request Headers: {flow.request.headers}")
    logging.info(f"Request Body: {flow.request.content}")

    flow.request.port = FORWARD_PORT

def response(flow: http.HTTPFlow) -> None:
    logging.info(f"Response Status Code: {flow.response.status_code}")
    logging.info(f"Response Headers: {flow.response.headers}")
    logging.info(f"Response Body: {flow.response.content}")
