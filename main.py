from typing import Any, Dict
from engine import extract_notification_context
from providers import get_active_providers

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    try:
        formatted_message, custom_targets = extract_notification_context(event)
        active_providers = list(get_active_providers())
        if not active_providers:
            print("[WARNING] Zero active notification providers discovered in configuration.")
            return {"statusCode": 400, "body": "No active notification providers configured."}

        dispatch_results = []
        for provider in active_providers:
            success = provider.broadcast_message(formatted_message, custom_targets)
            dispatch_results.append(success)

        if not all(dispatch_results):
            return {"statusCode": 207, "body": "Partial failure detected during omni-channel dispatch."}
            
        return {"statusCode": 200, "body": "Omni-channel notifications dispatched successfully."}

    except Exception as e:
        print(f"[CRITICAL] Runtime Exception: {str(e)}")
        return {"statusCode": 500, "body": f"Internal Server Error: {str(e)}"}