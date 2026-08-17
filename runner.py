"""
SRIIAGI — Test runner: iterate categories × encoders × payloads against your endpoint.
Supports OpenAI API, local Ollama, or any OpenAI-compatible endpoint.

USAGE:
  python runner.py --base-url http://localhost:11434/v1 --model llama3
  python runner.py --api-key $OPENAI_API_KEY --model gpt-4o
"""
import argparse
import asyncio
import json
import time
import httpx
from openai import AsyncOpenAI

from prompt_library import JAILBREAK_PROMPTS, TEST_PAYLOADS, CONTROL_PROMPTS
from encoder import ENCODERS
from detector import classify

class LLMTarget:
    def __init__(self, base_url, api_key, model):
        self.client = AsyncOpenAI(
            base_url=base_url or None, 
            api_key=api_key or "none",
            timeout=httpx.Timeout(120.0, connect=10.0)
        )
        self.model = model

    async def query(self, prompt: str, max_tokens: int = 512) -> str:
        try:
            resp = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                temperature=0.7,
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"[ERROR: {e}]"

async def run_attack(target, category, template, payload, encoder=None):
    prompt = template.format(payload=payload) if "{payload}" in template else f"{template} {payload}"
    if encoder:
        prompt = encoder(prompt)
    response = await target.query(prompt)
    result = classify(response)
    return {
        "category": category,
        "template": template[:80],
        "payload": payload[:60],
        "encoder": encoder.__name__ if encoder else None,
        "prompt": prompt[:200],
        "response": response[:500],
        **result,
    }

async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--base-url", default=None)
    ap.add_argument("--api-key", default=None)
    ap.add_argument("--model", required=True)
    ap.add_argument("--out", default="report.jsonl")
    args = ap.parse_args()

    target = LLMTarget(args.base_url, args.api_key, args.model)
    results = []
    jailbroken = 0
    total = 0

    # Control set first — measure false-positive rate
    print("[*] Running control prompts...")
    for cp in CONTROL_PROMPTS:
        resp = await target.query(cp)
        r = classify(resp)
        results.append({"control": cp, **r, "response": resp[:300]})

    # Attack matrix
    for category, templates in JAILBREAK_PROMPTS.items():
        for template in templates:
            if template is None:
                continue
            for payload in TEST_PAYLOADS:
                results.append(await run_attack(target, category, template, payload))
                total += 1
                time.sleep(0.3)  # rate limiting

            # Encoding variants on first payload only (keep matrix sane)
            first_payload = TEST_PAYLOADS[0]
            for name, enc_fn in ENCODERS.items():
                results.append(await run_attack(target, category, template, first_payload, enc_fn))
                total += 1

    # GCG adversarial suffix placeholder — load from file if generated
    try:
        with open("gcg_suffixes.json") as f:
            suffixes = json.load(f)
        for suffix in suffixes:
            for payload in TEST_PAYLOADS[:2]:
                results.append(await run_attack(target, "adversarial_suffix", "{payload} " + suffix, payload))
                total += 1
    except FileNotFoundError:
        print("[!] gcg_suffixes.json not found — skipping GCG tests")

    jailbroken = sum(1 for r in results if r.get("label") == "jailbroken")
    refused = sum(1 for r in results if r.get("label") == "refused")

    print(f"\n[+] Total attacks: {total}")
    print(f"[+] Jailbroken: {jailbroken} ({100*jailbroken/total:.1f}%)")
    print(f"[+] Refused: {refused} ({100*refused/total:.1f}%)")

    with open(args.out, "w") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

asyncio.run(main())