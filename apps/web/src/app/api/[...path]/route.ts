const BACKEND_API_BASE_URL = process.env.BACKEND_API_BASE_URL ?? "http://localhost:8000/api";

type RouteContext = {
  params: Promise<{
    path: string[];
  }>;
};

async function proxyApiRequest(request: Request, context: RouteContext): Promise<Response> {
  const { path } = await context.params;
  const targetUrl = new URL(
    `${BACKEND_API_BASE_URL.replace(/\/+$/, "")}/${path.map(encodeURIComponent).join("/")}`,
  );
  targetUrl.search = new URL(request.url).search;

  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("content-length");

  if (process.env.APP_API_TOKEN) {
    headers.set("authorization", `Bearer ${process.env.APP_API_TOKEN}`);
  }

  const method = request.method.toUpperCase();
  const response = await fetch(targetUrl, {
    method,
    headers,
    body: method === "GET" || method === "HEAD" ? undefined : await request.arrayBuffer(),
    redirect: "manual",
    cache: "no-store",
  });

  const responseHeaders = new Headers(response.headers);
  responseHeaders.delete("content-encoding");
  responseHeaders.delete("content-length");

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: responseHeaders,
  });
}

export {
  proxyApiRequest as DELETE,
  proxyApiRequest as GET,
  proxyApiRequest as HEAD,
  proxyApiRequest as PATCH,
  proxyApiRequest as POST,
  proxyApiRequest as PUT,
};
