#!/usr/bin/env python3
import json, sys, os, datetime, traceback, requests

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "interia_config.json")

def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def now_iso():
    return datetime.datetime.utcnow().isoformat() + "Z"

def ask_openai(cfg, question):
    key = cfg.get("openai_api_key")
    if not key: return None
    try:
        url = cfg.get("openai_endpoint", "https://api.openai.com/v1/chat/completions")
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {"model": cfg.get("openai_model","gpt-4o"), "messages":[{"role":"user","content":question}], "temperature":0}
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        r.raise_for_status()
        d = r.json()
        return d["choices"][0]["message"]["content"]
    except Exception:
        traceback.print_exc()
        return None

def ask_deepseek(cfg, question):
    key = cfg.get("deepseek_api_key")
    if not key: return None
    try:
        url = cfg.get("deepseek_endpoint","https://api.deepseek.com/chat/completions")
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {
            "model":"deepseek-chat",
            "messages":[
                {"role":"system","content":"You are part of HUMEAN inter-IA."},
                {"role":"user","content":question}
            ],
            "max_tokens":256,
            "temperature":0.1
        }
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code in (200,402,429):
            try:
                d = r.json()
                if "choices" in d: 
                    return d["choices"][0]["message"]["content"]
                return f"[deepseek:{r.status_code}] {d}"
            except Exception:
                return f"[deepseek:{r.status_code}]"
        r.raise_for_status()
        d = r.json()
        return d.get("choices",[{"message":{"content":json.dumps(d)}}])[0]["message"]["content"]
    except Exception:
        traceback.print_exc()
        return None

def ask_grok(cfg, question):
    key = cfg.get("grok_api_key")
    if not key: return None
    try:
        url = cfg.get("grok_endpoint","https://api.x.ai/v1/chat/completions")
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
        payload = {"model":"grok-beta","messages":[{"role":"user","content":question}],"temperature":0}
        r = requests.post(url, headers=headers, json=payload, timeout=30)
        if r.status_code in (200,403,429):
            try:
                d = r.json()
                if "choices" in d:
                    return d["choices"][0]["message"]["content"]
                return f"[grok:{r.status_code}] {d}"
            except Exception:
                return f"[grok:{r.status_code}]"
        r.raise_for_status()
        d = r.json()
        return d.get("choices",[{"message":{"content":json.dumps(d)}}])[0]["message"]["content"]
    except Exception:
        traceback.print_exc()
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: ask_all_models.py \"ta question ici\"", file=sys.stderr); sys.exit(1)
    question = sys.argv[1]
    cfg = load_config()
    out = {"question":question, "asked_at":now_iso(), "responses":{}}
    out["responses"]["openai"]   = ask_openai(cfg, question)
    out["responses"]["deepseek"] = ask_deepseek(cfg, question)
    out["responses"]["grok"]     = ask_grok(cfg, question)
    print(json.dumps(out, ensure_ascii=False, indent=2))
if __name__ == "__main__":
    main()
