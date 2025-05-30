def load_processes_from_lines(lines):
    procs = []
    for i, line in enumerate(lines, 1):
        parts = [x.strip() for x in line.split(',')]
        if len(parts) != 4:
            raise ValueError(f"[processes.txt] Línea {i} mal formada (esperado: PID, BT, AT, PRIORIDAD): {line}")

        pid, bt, at, prio = parts

        # Validación de enteros
        try:
            bt = int(bt)
            at = int(at)
            prio = int(prio)
        except ValueError:
            raise ValueError(f"[processes.txt] Línea {i}: BT, AT y PRIORIDAD deben ser números enteros. Línea: {line}")

        procs.append({
            'pid': pid,
            'bt': bt,
            'at': at,
            'prio': prio,
            'remaining': bt,
            'completed': False,
            'finish': None
        })
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