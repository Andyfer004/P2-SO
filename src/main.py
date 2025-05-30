import streamlit as st
import pandas as pd
from loader import load_processes_from_lines, load_resources_from_lines, load_actions_from_lines
from scheduling import run_scheduling
from synchronization import run_sync
from visualizer import plot_gantt, plot_sync
import plotly.graph_objects as go
import time

st.set_page_config(page_title="OS Simulator", layout="wide")
st.title("OS Simulator")

def _blocks_sync(events):
    """
    Convierte la lista de eventos {'pid','cycle','status'}
    en bloques contiguos para Gantt.
    """
    blocks = []
    for pid in sorted({e['pid'] for e in events}):
        seq = sorted([e for e in events if e['pid'] == pid], key=lambda x: x['cycle'])
        cur = None
        for e in seq:
            if cur and cur['status'] == e['status'] and cur['start'] + cur['duration'] == e['cycle']:
                cur['duration'] += 1
            else:
                cur = {
                    'pid': pid,
                    'start': e['cycle'],
                    'duration': 1,
                    'status': e['status']
                }
                blocks.append(cur)
    return blocks

# — Sidebar —
if st.sidebar.button("Limpiar"):
    st.session_state.clear()
    st.experimental_rerun()

mode = st.sidebar.selectbox("Simulación", ["Calendarización", "Sincronización"])

# Siempre pedimos processes.txt
proc_file = st.sidebar.file_uploader("processes.txt", type="txt")
if proc_file:
    st.session_state["proc_lines"] = proc_file.read().decode("utf-8").splitlines()

# Sólo en modo Sincronización pedimos resources + actions + modo
if mode == "Sincronización":
    res_file = st.sidebar.file_uploader("resources.txt", type="txt")
    if res_file:
        st.session_state["res_lines"] = res_file.read().decode("utf-8").splitlines()

    act_file = st.sidebar.file_uploader("actions.txt", type="txt")
    if act_file:
        st.session_state["act_lines"] = act_file.read().decode("utf-8").splitlines()

    mode_key = st.sidebar.selectbox("Modo de sincronización", ["mutex", "semaphore"])

# — Tabs —
tab1, tab2 = st.tabs(["Datos", "Simulación"])

with tab1:
    # Muestra procesos
    if "proc_lines" in st.session_state:
        try:
            procs = load_processes_from_lines(st.session_state["proc_lines"])
            st.dataframe(pd.DataFrame(procs))
        except Exception as e:
            st.error(f"Error en processes.txt: {e}")

    # Muestra recursos/acciones si aplica
    if mode == "Sincronización":
        if "res_lines" in st.session_state:
            try:
                res = load_resources_from_lines(st.session_state["res_lines"])
                df_res = pd.DataFrame(list(res.items()), columns=["Recurso", "Contador"])
                st.dataframe(df_res)
            except Exception as e:
                st.error(f"Error en resources.txt: {e}")

        if "act_lines" in st.session_state:
            try:
                acts = load_actions_from_lines(st.session_state["act_lines"])
                st.dataframe(pd.DataFrame(acts))
            except Exception as e:
                st.error(f"Error en actions.txt: {e}")

with tab2:
    if "proc_lines" not in st.session_state:
        st.info("Sube processes.txt antes de simular.")
    else:
        # — Calendarización —
        if mode == "Calendarización":
            algs = st.multiselect("Algoritmos", ["fifo", "sjf", "srt", "rr", "priority"])
            quantum = (
                st.sidebar.number_input("Quantum (RR)", min_value=1, value=1)
                if "rr" in algs else 1
            )

            if st.button("Ejecutar Calendarización"):
                if not algs:
                    st.warning("Selecciona al menos un algoritmo.")
                else:
                    results = []
                    for alg in algs:
                        procs_loop = load_processes_from_lines(st.session_state["proc_lines"])
                        sched, avg = run_scheduling(procs_loop, alg, quantum)
                        if not sched:
                            st.error(f"No se generó scheduling para {alg}")
                            continue

                        # Animación paso a paso
                        placeholder = st.empty()
                        fig = go.Figure()
                        colors = {}
                        for i, block in enumerate(sched):
                            pid, start, dur = block["pid"], block["start"], block["duration"]
                            if pid not in colors:
                                colors[pid] = f"hsl({(i*40)%360},70%,60%)"
                            fig.add_trace(go.Bar(
                                x=[dur], y=[pid], base=start, orientation="h",
                                marker=dict(color=colors[pid]),
                                text=[start], texttemplate="%{text}",
                                textposition="auto",
                                textfont=dict(color="black", size=12),
                                hovertemplate=f"{pid}: {start}→{start+dur}<extra></extra>"
                            ))
                            fig.update_layout(
                                title=f"Gantt Realtime (Avg Wait Time: {avg:.2f})",
                                xaxis=dict(
                                    title="Tiempo", type="linear",
                                    tickmode="linear", tick0=0, dtick=1,
                                    range=[0, max(b["start"] + b["duration"] for b in sched) + 1]
                                ),
                                yaxis=dict(title="Procesos", autorange="reversed"),
                                barmode="stack", bargap=0.2,
                                showlegend=False, height=300
                            )
                            placeholder.plotly_chart(fig, use_container_width=True, key=f"{alg}_{i}")
                            time.sleep(0.3)

                        results.append({"Algoritmo": alg, "AvgWaitingTime": avg})
                    st.table(pd.DataFrame(results))

        # — Sincronización corregida —
        else:
            if not ("res_lines" in st.session_state and "act_lines" in st.session_state):
                st.info("Sube resources.txt y actions.txt para sincronización.")
            else:
                if st.button("Ejecutar Sincronización"):
                    # 1) Generamos el timeline con run_sync (READ/WRITE → acquire/release)
                    procs_sync = load_processes_from_lines(st.session_state["proc_lines"])
                    resources  = load_resources_from_lines(st.session_state["res_lines"])
                    acts        = load_actions_from_lines(st.session_state["act_lines"])
                    tl          = run_sync(procs_sync, resources, acts, mode_key)

                    # 2) Construyo bloques de duración real
                    sync_blocks = _blocks_sync(tl)

                    # 3) Si no hay bloques, aviso y salgo
                    if not sync_blocks:
                        st.warning("No hay eventos de READ/WRITE para graficar.")
                    else:
                        last_cycle = max(b['start'] + b['duration'] for b in sync_blocks)
                        placeholder = st.empty()
                        colormap    = {"ACCESSED": "green", "WAITING": "red"}

                        # 4) Animación: relleno cada bloque hasta el ciclo actual
                        for ciclo in range(last_cycle + 1):
                            fig = go.Figure()
                            seen = set()
                            for b in sync_blocks:
                                if b['start'] > ciclo:
                                    continue
                                # cuánto mostrar hasta este ciclo:
                                dur = min(b['duration'], ciclo + 1 - b['start'])
                                stt = b['status']
                                first = (stt not in seen)
                                fig.add_trace(go.Bar(
                                    x=[dur], y=[b['pid']], base=b['start'],
                                    orientation="h",
                                    name=stt,
                                    showlegend=first,
                                    marker_color=colormap[stt],
                                    hovertemplate=(
                                        f"{b['pid']}: {b['start']}→{b['start'] + b['duration']}<br>"
                                        f"Estado: {stt}<extra></extra>"
                                    )
                                ))
                                seen.add(stt)

                            fig.update_layout(
                                title=f"Sincronización ({mode_key.title()}) – Ciclo {ciclo}",
                                xaxis=dict(title="Ciclo", tickmode="linear", dtick=1,
                                           range=[-0.5, last_cycle + 1]),
                                yaxis=dict(title="Proceso", autorange="reversed"),
                                barmode="stack", bargap=0.2, height=350,
                                legend_title_text="Estado"
                            )
                            placeholder.plotly_chart(fig, use_container_width=True)
                            time.sleep(0.3)