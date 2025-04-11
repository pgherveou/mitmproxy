from mitmproxy import http
import json
from eth.vm.forks.arrow_glacier.transactions import ArrowGlacierTransactionBuilder as TransactionBuilder
from eth_utils import  conversions

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
                    if json_data["method"] == "eth_sendRawTransaction":
                        raw_tx = conversions.to_bytes(hexstr=json_data["params"][0])
                        decoded_tx = TransactionBuilder().decode(raw_tx)
                        flow.metadata["decoded-tx"] = decoded_tx.__dict__

                if methods:
                    flow.metadata["json-rpc-path"] = ", ".join(methods)
            except ValueError:
                pass


    def response(self, flow: http.HTTPFlow):
        if flow.metadata["json-rpc-path"]:
            try:
                if flow.response is None:
                    flow.metadata["json-rpc-response"] = "No response"
                    return
                
                json_data = flow.response.json()
                results = set()
                
                if isinstance(json_data, list):
                    for item in json_data:
                        if "result" in item:
                            results.add(json.dumps(item["result"]))
                        elif "error" in item:
                            results.add(json.dumps(item["error"]))
                elif "result" in json_data:
                    results.add(json.dumps(json_data["result"]))
                elif "error" in json_data:
                    results.add(json.dumps(json_data["error"]))
                
                if results:
                    flow.metadata["json-rpc-response"] = ", ".join(results)
                else:
                    flow.metadata["json-rpc-response"] = "No result"
            except (ValueError, TypeError):
                pass

addons = [
    JSONRPCMethodColumn()
]

