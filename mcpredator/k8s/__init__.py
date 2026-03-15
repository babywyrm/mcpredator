"""Kubernetes internal checks, MCP service discovery, and service fingerprinting."""

from mcpredator.k8s.scanner import run_k8s_checks
from mcpredator.k8s.discovery import discover_services, DiscoveredEndpoint
from mcpredator.k8s.fingerprint import fingerprint_services, ServiceFingerprint

__all__ = [
    "run_k8s_checks", "discover_services", "DiscoveredEndpoint",
    "fingerprint_services", "ServiceFingerprint",
]
