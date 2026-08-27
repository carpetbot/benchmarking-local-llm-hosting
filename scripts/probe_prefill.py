import json, urllib.request, time
LONG = ('You are reviewing a technical document. Here is the document:\n\n'
        + ('A single-board computer integrates a processor, memory, storage and I/O '
           'onto one printed circuit board. Memory bandwidth constrains token '
           'generation speed for large language model inference, while compute '
           'throughput constrains prompt processing. These are distinct axes and '
           'should never be conflated when evaluating hardware. ') * 40
        + '\n\nSummarize the document in three sentences.')
body = json.dumps({'model': 'qwen3:8b', 'prompt': LONG, 'stream': False,
                   'options': {'num_predict': 32, 'temperature': 0}}).encode()
req = urllib.request.Request('http://localhost:11434/api/generate', data=body,
                             headers={'Content-Type': 'application/json'})
t0 = time.time()
r = json.load(urllib.request.urlopen(req, timeout=3600))
wall = time.time() - t0

out = {}
for k in ['prompt_eval_count', 'prompt_eval_duration', 'eval_count',
          'eval_duration', 'load_duration', 'total_duration']:
    out[k] = r.get(k, 0)
out['wall_clock_s'] = round(wall, 2)

pe_n, pe_d = r['prompt_eval_count'], r['prompt_eval_duration']
out['reported_prefill_tok_s'] = round(pe_n / (pe_d / 1e9), 2) if pe_d else None
sum_ns = r['prompt_eval_duration'] + r['eval_duration'] + r.get('load_duration', 0)
out['sum_of_parts_s'] = round(sum_ns / 1e9, 2)
out['total_duration_s'] = round(r['total_duration'] / 1e9, 2)
out['unaccounted_s'] = round((r['total_duration'] - sum_ns) / 1e9, 2)
# The honest number: prefill tokens over (wall - decode time)
decode_s = r['eval_duration'] / 1e9
out['wall_derived_prefill_tok_s'] = round(pe_n / max(wall - decode_s, 0.001), 2)

json.dump(out, open('/home/orangepi/prefill_artifact_probe.json', 'w'), indent=2)
print(json.dumps(out, indent=2))
