from mitmproxy import http

class JSONRPCMethodColumn:
    def load(self, loader):
        loader.add_option(
            name="json_rpc_method",
            typespec=str,
            default="",
            help="Display JSON-RPC method"
        )

    def request(self, flow: http.HTTPFlow):
        if flow.request.headers.get("Content-Type") == "application/json":
            try:
                json_data = flow.request.json()
                methods = set()
                if isinstance(json_data, list):
                    for item in json_data:
                        if "method" in item:
                            methods.add(item["method"])
                elif "method" in json_data:
                    methods.add(json_data["method"])
                if methods:
                    flow.metadata["path"] = ", ".join(methods)
            except ValueError:
                pass

    def response(self, flow: http.HTTPFlow):
        if flow.response and flow.request.headers.get("Json-Rpc-Method"):
            flow.response.headers["Json-Rpc-Method"] = flow.request.headers["Json-Rpc-Method"]

addons = [
    JSONRPCMethodColumn()
]

