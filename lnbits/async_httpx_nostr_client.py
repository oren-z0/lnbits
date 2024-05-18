import urllib
import typing
import httpx
from lnbits.settings import settings

class AsyncHttpxNostrClient(httpx.AsyncClient):
    def build_request(
        self,
        method: str,
        url: httpx._types.URLTypes,
        *,
        headers: httpx._types.HeaderTypes | None = None,
        **kws: typing.Any,
    ):
        if settings.lnbits_http2nostr_host:
            try:
                if isinstance(url, httpx.URL):
                    parsed_url = url
                else:
                    parsed_url = httpx.URL(url) 
                if parsed_url.scheme == "http" and parsed_url.host.endswith(".nostr") and parsed_url.port is None:
                    url = parsed_url.copy_with(host = settings.lnbits_http2nostr_host)
                    headers = httpx.Headers(headers)
                    headers["X-Nostr-Destination"] = parsed_url.host[:-len(".nostr")]
            except (httpx.InvalidURL, ValueError) as _error:
                pass
        return super().build_request(method, url, headers=headers, **kws)
