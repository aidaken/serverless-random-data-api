import json
import random
import logging

# Configure logging (goes to CloudWatch Logs)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    Random Data API (Lambda Proxy Integration)
    GET /random?type=quote|number|color
    """
    try:
        # Log incoming event for debugging
        logger.info("Received event: %s", json.dumps(event))

        # Safe query param parsing
        query_params = event.get("queryStringParameters") or {}
        data_type = (query_params.get("type") or "quote").lower().strip()

        # Data sources
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "Life is what happens to you while you're busy making other plans. - John Lennon",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
        ]

        colors = [
            {"name": "Ocean Blue", "hex": "#006994", "rgb": "rgb(0, 105, 148)"},
            {"name": "Sunset Orange", "hex": "#FF6B35", "rgb": "rgb(255, 107, 53)"},
            {"name": "Forest Green", "hex": "#2E8B57", "rgb": "rgb(46, 139, 87)"},
            {"name": "Purple Haze", "hex": "#9370DB", "rgb": "rgb(147, 112, 219)"},
            {"name": "Golden Yellow", "hex": "#FFD700", "rgb": "rgb(255, 215, 0)"},
        ]

        # Generate data based on type
        if data_type == "quote":
            data = random.choice(quotes)
        elif data_type == "number":
            data = random.randint(1, 1000)
        elif data_type == "color":
            data = random.choice(colors)
        else:
            # Fallback to quote for unknown types
            data_type = "quote"
            data = random.choice(quotes)

        # Build response body
        response_body = {
            "type": data_type,
            "data": data,
            "requestId": getattr(context, "aws_request_id", None),
            "message": f"Random {data_type} generated successfully",
        }

        # Return successful response (Lambda Proxy format)
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type",
            },
            "body": json.dumps(response_body),
        }

    except Exception as e:
        logger.exception("Unhandled error")  # logs stack trace to CloudWatch
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
            },
            "body": json.dumps(
                {
                    "error": "Internal server error",
                    "message": "Failed to generate random data",
                    "requestId": getattr(context, "aws_request_id", None),
                }
            ),
        }
