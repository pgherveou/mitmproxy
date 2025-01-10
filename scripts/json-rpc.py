from mitmproxy import http

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
        if flow.response and flow.request.headers.get("Json-Rpc-Method"):
            flow.response.headers["Json-Rpc-Method"] = flow.request.headers["Json-Rpc-Method"]

addons = [
    JSONRPCMethodColumn()
]

