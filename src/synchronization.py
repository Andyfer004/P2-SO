def run_sync(procs, resources, actions, mode='mutex'):
    """
    procs: lista de dicts con 'pid' (pero aquí no los usamos más que para timeline)
    resources: dict {recurso: contador_inicial}
    actions: lista de dicts con 'pid','action' ('READ' o 'WRITE'), 'resource','cycle'
    mode: 'mutex' o 'semaphore'
    """
    # 1) Copia de contadores
    counts = resources.copy()
    timeline = []

    # 2) Agrupar acciones por ciclo
    from collections import defaultdict
    by_cycle = defaultdict(list)
    for a in actions:
        by_cycle[a['cycle']].append(a)

    last = max(by_cycle.keys()) if by_cycle else -1

    # 3) Bucle de simulación
    for cycle in range(last + 1):
        batch = by_cycle.get(cycle, [])

        # 3a) Primero los WRITEs (release)
        for a in batch:
            if a['action'].strip().upper() == 'WRITE':
                r = a['resource']
                if mode == 'semaphore':
                    counts[r] = counts.get(r, 0) + 1
                else:  # mutex
                    counts[r] = 1

        # 3b) Luego los READs (acquire)
        for a in batch:
            if a['action'].strip().upper() == 'READ':
                r = a['resource']
                if counts.get(r, 0) > 0:
                    status = 'ACCESSED'
                    if mode == 'semaphore':
                        counts[r] -= 1
                    else:
                        counts[r] = 0
                else:
                    status = 'WAITING'
                timeline.append({
                    'pid':      a['pid'],
                    'action':   'acquire',
                    'resource': r,
                    'cycle':    cycle,
                    'status':   status
                })

    return timeline