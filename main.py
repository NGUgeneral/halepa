import os
from typing import Any, Dict
from engine import extract_notification_context
from providers import get_provider

TARGET_PROVIDER = os.environ.get("HALEPA_PROVIDER", "telegram")

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    print(f"[INFO] Processing event: {list(event.keys())}")
    
    try:
        # 1. Parse out message context and potential target list
        formatted_message, targets = extract_notification_context(event)
        
        # 2. Get provider strategy
        provider = get_provider(TARGET_PROVIDER)
        
        # 3. Broadcast to all subscribers
        success = provider.broadcast_message(formatted_message, targets)
        
        if not success:
            return {"statusCode": 207, "body": "Partial or total failure during fan-out dispatch."}
            
        return {"statusCode": 200, "body": "All notifications dispatched successfully."}

    except Exception as e:
        print(f"[CRITICAL] Runtime Exception: {str(e)}")
        return {"statusCode": 500, "body": f"Internal Server Error: {str(e)}"}