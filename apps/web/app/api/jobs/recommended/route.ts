import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  const backendUrl =
    process.env.NEXT_PUBLIC_API_BASE_URL ||
    "http://127.0.0.1:8000";

  const authorization = request.headers.get("authorization");

  if (!authorization) {
    return NextResponse.json(
      { detail: "Missing authorization header." },
      { status: 401 },
    );
  }

  try {
    const response = await fetch(
      `${backendUrl}/api/v1/jobs/recommended`,
      {
        method: "GET",
        headers: {
          Authorization: authorization,
        },
        cache: "no-store",
      },
    );

    const body = await response.text();

    return new NextResponse(body, {
      status: response.status,
      headers: {
        "Content-Type":
          response.headers.get("content-type") ?? "application/json",
      },
    });
  } catch {
    return NextResponse.json(
      { detail: "CareerOS backend is unavailable." },
      { status: 503 },
    );
  }
}