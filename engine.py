import json
from typing import Any, Dict, List, Tuple

def parse_sns_message(sns_record: Dict[str, Any]) -> str:
    subject = sns_record.get("Subject", "⚠️ Halepa Alert Triggered")
    raw_message = sns_record.get("Message", "")
    try:
        msg_json = json.loads(raw_message)
        alarm_name = msg_json.get("AlarmName", "Unknown Alarm")
        new_state = msg_json.get("NewStateValue", "UNKNOWN")
        reason = msg_json.get("NewStateReason", "No reason provided.")
        return (
            f"<b>🚨 {subject}</b>\n\n"
            f"<b>Alarm:</b> {alarm_name}\n"
            f"<b>Status:</b> {new_state}\n"
            f"<b>Reason:</b> <code>{reason}</code>"
        )
    except json.JSONDecodeError:
        return f"<b>🚨 {subject}</b>\n\n{raw_message}"

def extract_notification_context(event: Dict[str, Any]) -> Tuple[str, List[str] | None]:
    match event:
        # Case 1: Standard AWS SNS event payload
        case {"Records": [{"EventSource": "aws:sns", "Sns": sns_record}, *__]}:
            return parse_sns_message(sns_record), None
        
        # Case 2: Direct Broadcast with custom target override
        case {"broadcast_message": str(text), "targets": list(custom_targets)}:
            return f"<b>📣 System Broadcast:</b>\n\n{text}", [str(t) for t in custom_targets]
            
        # Case 3: Direct Broadcast Payload (default environmental targets)
        case {"broadcast_message": str(text)}:
            return f"<b>📣 System Broadcast:</b>\n\n{text}", None
        
        # Case 4: Fallback
        case _:
            print(f"[WARNING] Unrecognized event structure: {json.dumps(event)}")
            return f"<b>⚠️ Halepa Warning</b>\nReceived unparsed system event payload.", None