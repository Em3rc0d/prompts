import { createHash } from 'node:crypto';

export const runtime = 'nodejs';
export const dynamic = 'force-dynamic';

const CASE_ID = 'PM-STARTER-CR-NORMAL-0001';
const EXPECTED_SHA256 = 'd8572fb1731242224cf76520ebfd1fdcbe496964205837613c02a24af7d9c207';
const DEFAULT_MODEL = 'openai/gpt-5.6-sol';

function sha256(value: Buffer) {
  return createHash('sha256').update(value).digest('hex');
}

export async function POST(request: Request) {
  const executionToken = process.env.N09_EXECUTION_TOKEN;
  const envelopeB64 = process.env.N09_RUNTIME_ENVELOPE_B64;
  const oidcToken = process.env.VERCEL_OIDC_TOKEN;
  const model = process.env.N09_MODEL || DEFAULT_MODEL;

  if (!executionToken || !envelopeB64 || !oidcToken) {
    return Response.json(
      { ok: false, case_id: CASE_ID, state: 'BLOCKED_SURFACE_NOT_ARMED' },
      { status: 503 },
    );
  }

  if (request.headers.get('authorization') !== `Bearer ${executionToken}`) {
    return Response.json(
      { ok: false, case_id: CASE_ID, state: 'BLOCKED_INVALID_EXECUTION_TOKEN' },
      { status: 401 },
    );
  }

  const envelope = Buffer.from(envelopeB64, 'base64');
  const envelopeSha256 = sha256(envelope);
  if (envelope.length !== 8100 || envelopeSha256 !== EXPECTED_SHA256) {
    return Response.json(
      {
        ok: false,
        case_id: CASE_ID,
        state: 'BLOCKED_ENVELOPE_DRIFT',
        runtime_envelope_bytes: envelope.length,
        runtime_envelope_sha256: envelopeSha256,
      },
      { status: 412 },
    );
  }

  let gatewayResponse: Response;
  try {
    gatewayResponse = await fetch('https://ai-gateway.vercel.sh/v1/chat/completions', {
      method: 'POST',
      headers: {
        authorization: `Bearer ${oidcToken}`,
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model,
        messages: [{ role: 'user', content: envelope.toString('utf8') }],
        stream: false,
        store: false,
      }),
      cache: 'no-store',
    });
  } catch (error) {
    return Response.json(
      {
        ok: false,
        case_id: CASE_ID,
        state: 'GATEWAY_TRANSPORT_ERROR_AFTER_SINGLE_SUBMISSION',
        runtime_envelope_bytes: envelope.length,
        runtime_envelope_sha256: envelopeSha256,
        model_requested: model,
        error: error instanceof Error ? error.message : 'unknown transport error',
      },
      { status: 502 },
    );
  }

  const rawGatewayBody = await gatewayResponse.text();
  let gatewayPayload: unknown = rawGatewayBody;
  try {
    gatewayPayload = JSON.parse(rawGatewayBody);
  } catch {
    // Preserve non-JSON gateway body verbatim.
  }

  if (!gatewayResponse.ok) {
    return Response.json(
      {
        ok: false,
        case_id: CASE_ID,
        state: 'GATEWAY_REJECTED_AFTER_SINGLE_SUBMISSION',
        runtime_envelope_bytes: envelope.length,
        runtime_envelope_sha256: envelopeSha256,
        model_requested: model,
        gateway_http_status: gatewayResponse.status,
        gateway_payload: gatewayPayload,
      },
      { status: 502 },
    );
  }

  const payload = gatewayPayload as {
    model?: string;
    choices?: Array<{ message?: { content?: string } }>;
    usage?: unknown;
    id?: string;
  };
  const output = payload.choices?.[0]?.message?.content;

  if (!output) {
    return Response.json(
      {
        ok: false,
        case_id: CASE_ID,
        state: 'NO_OBSERVABLE_OUTPUT_AFTER_SINGLE_SUBMISSION',
        runtime_envelope_bytes: envelope.length,
        runtime_envelope_sha256: envelopeSha256,
        model_requested: model,
        model_observed: payload.model ?? null,
        gateway_response_id: payload.id ?? null,
        usage: payload.usage ?? null,
      },
      { status: 502 },
    );
  }

  return Response.json({
    ok: true,
    case_id: CASE_ID,
    state: 'REAL_CLEAN_RUNTIME_OBSERVATION_REVIEW_REQUIRED',
    execution_surface: 'VERCEL_AI_GATEWAY_PREVIEW',
    clean_independent_surface: true,
    evaluation_contract_present_in_runtime_input: false,
    expected_result_present_in_runtime_input: false,
    runtime_envelope_bytes: envelope.length,
    runtime_envelope_sha256: envelopeSha256,
    model_requested: model,
    model_observed: payload.model ?? null,
    gateway_response_id: payload.id ?? null,
    usage: payload.usage ?? null,
    raw_output: output,
    automatic_retries: 0,
    automatic_second_case: false,
    human_review_required: true,
  });
}
