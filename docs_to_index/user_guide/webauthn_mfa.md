# WebAuthn / Passkey MFA

Forail supports WebAuthn (FIDO2) for multi-factor authentication. Users can register hardware security keys (YubiKey), platform authenticators (Touch ID, Windows Hello), or passkeys for passwordless login.

## MFA Policy

Administrators can enforce MFA at the organization level with three settings:

| Setting | Behavior |
|---------|----------|
| **none** | MFA is optional for all users. |
| **admins** | MFA is required for admin/superuser accounts only. |
| **all** | MFA is required for all users in the organization. |

Configure this in **Settings > Security > WebAuthn Required**.

## Registering a Security Key

1. Navigate to your **User Security** page (`/me/security`).
2. Click **Register New Key**.
3. Follow the browser prompt — touch your security key or use biometrics.
4. Give the key a **label** (e.g., "YubiKey 5C", "MacBook Touch ID").
5. The key is now registered and can be used for MFA challenges.

## Authentication Flow

1. User enters username and password on the login page.
2. If MFA is required, Forail redirects to `/auth/mfa`.
3. The browser prompts for the security key or passkey.
4. Forail verifies the signature and sign count (replay protection).
5. On success, the session is created.

## Replay Protection

Forail tracks the **sign count** of each authenticator. If a presented sign count is less than or equal to the stored count, the authentication is rejected as a potential replay attack. The exception is authenticators that never increment (both stored and presented are 0).

## Managing Keys

Users can:
- View all registered keys with their labels, last used date, and transport types.
- Delete keys they no longer use.
- Register multiple keys for backup.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v2/webauthn/credentials/` | List registered credentials |
| DELETE | `/api/v2/webauthn/credentials/{id}/` | Remove a credential |
| POST | `/api/v2/webauthn/register/begin/` | Start registration |
| POST | `/api/v2/webauthn/register/complete/` | Complete registration |
| POST | `/api/v2/webauthn/authenticate/begin/` | Start authentication |
| POST | `/api/v2/webauthn/authenticate/complete/` | Complete authentication |
