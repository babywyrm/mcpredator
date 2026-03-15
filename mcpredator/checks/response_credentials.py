"""Scan tool response content for leaked credentials (MCP-T07)."""

import re

from mcpredator.core.models import TargetResult
from mcpredator.checks.base import time_check
from mcpredator.checks.tool_probes import _build_safe_args, _call_tool, _response_text, _should_invoke
from mcpredator.patterns.probes import CREDENTIAL_CONTENT_PATTERNS


def check_response_credentials(session, result: TargetResult, probe_opts: dict | None = None):
    """Call each tool with safe inputs and scan responses for credential patterns.

    Goes beyond error_leakage by checking ALL responses (success and error)
    for secrets like API keys, connection strings, private keys, and passwords
    that slip through incomplete server-side redaction.
    """
    opts = probe_opts or {}
    with time_check("response_credentials", result):
        for tool in result.tools:
            if not _should_invoke(tool, opts):
                continue
            name = tool.get("name", "")
            args = _build_safe_args(tool)
            resp = _call_tool(session, name, args)
            text = _response_text(resp)
            if not text:
                continue

            for pat, cred_type in CREDENTIAL_CONTENT_PATTERNS:
                m = re.search(pat, text, re.IGNORECASE)
                if m:
                    result.add(
                        "response_credentials",
                        "CRITICAL",
                        f"Credential leak in tool '{name}' response: {cred_type}",
                        f"Tool response contains what appears to be a live {cred_type}",
                        evidence=m.group()[:200],
                    )
                    break
