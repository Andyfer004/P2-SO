
import copy

def _blocks_from_timeline(tl):
    blocks, cur = [], None
    for ev in tl:
        if cur and ev['pid'] == cur['pid'] and ev['time'] == cur['end']:
            cur['end'] += 1
        else:
            if cur:
                blocks.append(cur)
            cur = {'pid': ev['pid'], 'start': ev['time'], 'end': ev['time'] + 1}
    if cur:
        blocks.append(cur)

    return [{'pid': b['pid'], 'start': b['start'], 'duration': b['end'] - b['start']}
            for b in blocks if b['pid'] is not None]

def _compute_avg_wt(procs):
    finished = [p for p in procs if p['finish'] is not None]
    if not finished:
        return 0
    total = sum((p['finish'] - p['at'] - p['bt']) for p in finished)
    return total / len(finished)

def simulate_fifo(procs):
    procs2 = sorted(procs, key=lambda p: p['at'])
    time, tl = 0, []
    for p in procs2:
        time = max(time, p['at'])
        for _ in range(p['bt']):
            tl.append({'time': time, 'pid': p['pid']})
            time += 1
        p['finish'], p['completed'] = time, True
    return tl

def simulate_sjf(procs2):
    time, tl, done = 0, [], 0
    while done < len(procs2):
        ready = [p for p in procs2 if not p['completed'] and p['at'] <= time]
        if ready:
            p = min(ready, key=lambda x: x['bt'])
            for _ in range(p['bt']):
                tl.append({'time': time, 'pid': p['pid']})
                time += 1
            for proc in procs2:
                if proc['pid'] == p['pid']:
                    proc['finish'], proc['completed'] = time, True
                    done += 1
                    break
        else:
            tl.append({'time': time, 'pid': None})
            time += 1
    return tl

def simulate_srt(procs2):
    time, tl, done = 0, [], 0
    while done < len(procs2):
        ready = [p for p in procs2 if not p['completed'] and p['at'] <= time]
        if ready:
            p = min(ready, key=lambda x: x['remaining'])
            tl.append({'time': time, 'pid': p['pid']})
            p['remaining'] -= 1
            time += 1
            if p['remaining'] == 0:
                for proc in procs2:
                    if proc['pid'] == p['pid']:
                        proc['finish'], proc['completed'] = time, True
                        done += 1
                        break
        else:
            tl.append({'time': time, 'pid': None})
            time += 1
    return tl

def simulate_rr(procs2, quantum):
    queue, time, tl, idx, done = [], 0, [], 0, 0
    n = len(procs2)
    while done < n:
        while idx < n and procs2[idx]['at'] <= time:
            queue.append(procs2[idx])
            idx += 1
        if queue:
            p = queue.pop(0)
            run = min(p['remaining'], quantum)
            for _ in range(run):
                tl.append({'time': time, 'pid': p['pid']})
                time += 1
            p['remaining'] -= run
            while idx < n and procs2[idx]['at'] <= time:
                queue.append(procs2[idx])
                idx += 1
            if p['remaining'] > 0:
                queue.append(p)
            else:
                for proc in procs2:
                    if proc['pid'] == p['pid']:
                        proc['finish'], proc['completed'] = time, True
                        done += 1
                        break
        else:
            tl.append({'time': time, 'pid': None})
            time += 1
    return tl

def simulate_priority(procs2):
    time, tl, done = 0, [], 0
    while done < len(procs2):
        ready = [p for p in procs2 if not p['completed'] and p['at'] <= time]
        if ready:
            p = min(ready, key=lambda x: x['prio'])
            for _ in range(p['bt']):
                tl.append({'time': time, 'pid': p['pid']})
                time += 1
            for proc in procs2:
                if proc['pid'] == p['pid']:
                    proc['finish'], proc['completed'] = time, True
                    done += 1
                    break
        else:
            tl.append({'time': time, 'pid': None})
            time += 1
    return tl

def run_scheduling(procs, alg, quantum=1):
    procs2 = copy.deepcopy(procs)
    for p in procs2:
        p['remaining'] = p['bt']
        p['completed'] = False
        p['finish'] = None

    if alg == 'fifo':
        tl = simulate_fifo(procs2)
    elif alg == 'sjf':
        tl = simulate_sjf(procs2)
    elif alg == 'srt':
        tl = simulate_srt(procs2)
    elif alg == 'rr':
        tl = simulate_rr(procs2, quantum)
    else:
        tl = simulate_priority(procs2)

    avg = _compute_avg_wt(procs2)
    blocks = _blocks_from_timeline(tl)
    return blocks, avg