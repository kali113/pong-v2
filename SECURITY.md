# Security Policy

## Supported Versions

| Version | Supported |
|---------|-----------|
| 1.0.0-alpha | ✅ Active development |

## Reporting a Vulnerability

**DO NOT** open public issues for security vulnerabilities.

Instead:
1. Email: gayzmore1@gmail.com or open a private security advisory
2. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours.

## Security Considerations

### LAN Multiplayer
- **Network binding**: The game binds to `0.0.0.0` for LAN multiplayer
- **Intended use**: Local network only (home/office WiFi)
- **DO NOT**: Expose to the internet or untrusted networks
- **Firewall**: Ensure your firewall is configured properly

### Dependencies
- Regular security updates via Dependabot
- Only uses well-maintained packages:
  - pygame >= 2.6.0
  - numpy >= 1.24.0

### Data Storage
- Settings stored locally in `~/.pong_ai_settings.json`
- No personal data collected
- No network tracking or analytics

## Best Practices

When hosting multiplayer games:
1. Only connect to trusted players
2. Use private networks (not public WiFi)
3. Firewall rules: Allow only necessary ports
4. Keep Python and dependencies updated

## Known Issues

None currently reported.

## Updates

Security updates are released as patch versions (e.g., v1.0.1, v1.0.2).
Subscribe to releases for notifications.
