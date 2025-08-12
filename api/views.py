# api/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pyzbar.pyzbar import decode
from PIL import Image
import io
import re

def scan_page(request):
    return render(request, "scanner.html")


def classify_text(text: str) -> dict:
    """Return a dict with type and a short description/payload based on simple heuristics."""
    t = text.strip()

    # URL
    if re.match(r'^(https?://)', t, re.I):
        return {"type": "url", "payload": t}

    # mailto:
    if t.lower().startswith("mailto:"):
        return {"type": "email", "payload": t[7:]}

    # tel:
    if t.lower().startswith("tel:"):
        return {"type": "phone", "payload": t[4:]}

    # SMS
    if t.lower().startswith("sms:") or t.lower().startswith("smsto:"):
        return {"type": "sms", "payload": t}

    # WiFi QR (format starts with WIFI:)
    if t.upper().startswith("WIFI:"):
        # parse WIFI:T:WPA;S:network;P:password;;
        payload = {}
        try:
            # simple parser for key:value; pairs
            inner = t[5:].rstrip(';')
            parts = inner.split(';')
            for part in parts:
                if ':' in part:
                    k, v = part.split(':', 1)
                    payload[k] = v
        except Exception:
            payload = {"raw": t}
        return {"type": "wifi", "payload": payload}

    # vCard
    if t.upper().startswith("BEGIN:VCARD"):
        return {"type": "vcard", "payload": t}

    # geo: coordinates
    if t.lower().startswith("geo:"):
        return {"type": "geo", "payload": t}

    # Bitcoin / crypto links (bitcoin: or pay)
    if t.lower().startswith("bitcoin:") or re.search(r'^(bc1|1|3)[0-9A-Za-z]{25,34}$', t):
        return {"type": "crypto", "payload": t}

    # UPI / payment-like (upi:// or contains easypaisa/pay/qr keywords)
    if t.lower().startswith("upi:") or re.search(r'(upi|easypaisa|pay|paytm|alipay)', t, re.I):
        return {"type": "payment", "payload": t}

    # phone number heuristic
    if re.fullmatch(r'[\d\+\-\s\(\)]{6,20}', t):
        return {"type": "phone", "payload": t}

    # fallback plain text
    return {"type": "text", "payload": t}


@csrf_exempt
def upload_qr(request):
    """
    Accepts POST with file field named 'file'. Returns decoded results and classifications.
    """
    if request.method == "POST" and request.FILES.get("file"):
        f = request.FILES["file"]
        try:
            image = Image.open(f)
        except Exception as e:
            return JsonResponse({"error": "Invalid image file", "detail": str(e)}, status=400)

        decoded = decode(image)
        results = []
        for obj in decoded:
            try:
                s = obj.data.decode("utf-8")
            except Exception:
                s = obj.data.decode(errors='ignore')
            results.append({"raw": s, **classify_text(s)})

        return JsonResponse({"results": results})
    return JsonResponse({"error": "No file uploaded"}, status=400)
