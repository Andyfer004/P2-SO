def load_processes_from_lines(lines):
    print(f"[DEBUG] Líneas leídas: {lines}")
    procs = []
    for i, line in enumerate(lines, 1):
        parts = [x.strip() for x in line.split(',')]
        if len(parts) != 4:
            raise ValueError(f"Línea {i}: formato inválido en processes.txt")
        pid, bt, at, prio = parts
        procs.append({
            'pid': pid,
            'bt': int(bt),
            'at': int(at),
            'prio': int(prio),
            'remaining': int(bt),
            'completed': False,
            'finish': None
        })
    print(f"[DEBUG] Procesos cargados: {procs}")
    return procs

def load_resources_from_lines(lines):
    res = {}
    for i, line in enumerate(lines, 1):
        parts = [x.strip() for x in line.split(',')]
        if len(parts) != 2:
            raise ValueError(f"Línea {i}: formato inválido en resources.txt")
        name, cnt = parts
        res[name] = int(cnt)
    return res

def load_actions_from_lines(lines):
    acts = []
    for i, line in enumerate(lines, 1):
        parts = [x.strip() for x in line.split(',')]
        if len(parts) != 4:
            raise ValueError(f"Línea {i}: formato inválido en actions.txt")
        pid, action, resource, cycle = parts
        acts.append({
            'pid': pid,
            'action': action,
            'resource': resource,
            'cycle': int(cycle)
        })
    return sorted(acts, key=lambda x: x['cycle'])