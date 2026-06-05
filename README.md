# Halepa (Халепа)

A stateless, ultra-lightweight, zero-dependency AWS Lambda utility designed to route raw cloud alerts and direct system broadcasts to multiple messenger applications simultaneously.

Built strictly with the Python 3.12 standard library to achieve near-zero cold starts and a sub-15KB deployment footprint. It leverages structural pattern matching for polymorphic payload ingestion and the Strategy Pattern for highly decoupled, omni-channel fan-out delivery.

## Key Architectural Highlights

* **Absolute Zero External Overhead:** Uses native standard library (`urllib`). No bulky external SDKs or HTTP clients (like `boto3` or `requests`), guaranteeing blazing-fast execution.
* **Polymorphic Ingestion Engine:** Natively consumes both asynchronous AWS SNS/CloudWatch record structures and direct, synchronous HTTPS system broadcasts (e.g., via a Lambda Function URL).
* **Decoupled Strategy Design:** Adding new delivery channels (Slack, Teams, Discord) requires zero modification to the core parsing or ingestion loops.
* **Self-Disabling Infrastructure:** Fully configuration-driven. If a provider's foundational credentials are not found in the environment, the engine dynamically skips it.

---

## Configuration Guide (.env / Lambda Environment)

Halepa reads configuration values exactly as they are structured in the environment. It supports relaxed syntax boundaries for target arrays, meaning lists can be supplied as raw strings, comma-separated lists, or wrapped in JSON-style brackets with loose whitespace.

Create a `.env` file in the root of the project for local development (this file is tracked in `.gitignore`):

```env
# ==============================================================================
# Halepa Environment Configuration Matrix
# ==============================================================================

# --- Telegram Strategy ---
# Token provided by @BotFather
TELEGRAM_BOT_TOKEN="1234567890:ABCdefGhIJKlmNoPQRsTUVwxyZ_12345678"
# Supports single IDs, bracketed arrays, or trailing spaces.
# Note: Group chats typically start with a negative sign (-)
TELEGRAM_CHAT_IDS="[123456789, -100987654321]"

# --- Slack Strategy ---
# Targeted Channel Webhooks generated via Slack Apps
SLACK_WEBHOOK_URLS="[[https://hooks.slack.com/services/T00/B00/X00](https://hooks.slack.com/services/T00/B00/X00), [https://hooks.slack.com/services/T00/B00/Y00](https://hooks.slack.com/services/T00/B00/Y00)]"

# --- Microsoft Teams Strategy ---
# Target Channel Connectors generated via Office 365 Webhooks
TEAMS_WEBHOOK_URLS="[[https://your-office.webhook.office.com/webhookb2/](https://your-office.webhook.office.com/webhookb2/)...]"

# --- WhatsApp Strategy ---
# Meta Graph API authorization token and originating business profile ID
WHATSAPP_API_TOKEN="EAAl..."
WHATSAPP_PHONE_NUMBER_ID="123456789"
# Array of destination recipient phone numbers in standard E.164 format
WHATSAPP_TARGET_PHONES="[+31600000000, +31611111111]"
```
## Supported Ingestion Formats

Halepa uses Python structural pattern matching to analyze the incoming event signatures and format the payload into human-readable alerts.

### 1. Asynchronous AWS SNS Payload (CloudWatch Alarms)
When a CloudWatch Alarm triggers an SNS topic subscription, Halepa parses the embedded JSON metadata fields (`AlarmName`, `NewStateValue`, `NewStateReason`) and crafts an organized alert block.

**Expected Event Shape:**
```json
{
  "Records": [
    {
      "EventSource": "aws:sns",
      "Sns": {
        "Subject": "ALB 5xx Spike Detected",
        "Message": "{\"AlarmName\":\"Production-ALB-High-5xx-Errors\",\"NewStateValue\":\"ALARM\",\"NewStateReason\":\"Threshold Crossed: 1 out of the last 1 datapoints was greater than the threshold.\"}"
      }
    }
  ]
}
```
### Direct Broadcast Payload
Perfect for firing manual system notifications, pipeline completion updates, or deployment logs via a Lambda Function URL. 

**Expected Event Shape:**
```json
{
  "broadcast_message": "Production deployment successful! Halepa Core v1.1.0 is live."
}
```
## Local Development

To run execution simulations locally without deploying infrastructure to AWS or spinning up emulators, use the untracked local test driver file:

1. Populate your credentials in the `.env` file.
2. Initialize the local test harness:
```bash
python main.local.py
```

