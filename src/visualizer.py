import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def plot_gantt(blocks, avg):
    df = pd.DataFrame(blocks)
    if df.empty:
        return go.Figure().update_layout(title="No hay datos para Calendarización")

    df['end'] = df['start'] + df['duration']
    df['pid'] = df['pid'].astype(str)

    fig = go.Figure()
    colors = {}

    for i, row in df.iterrows():
        pid      = row['pid']
        start    = row['start']
        duration = row['duration']
        end      = row['end']

        # color consistente por PID
        if pid not in colors:
            colors[pid] = f"hsl({(i*40)%360}, 70%, 60%)"

        fig.add_trace(go.Bar(
            x=[duration],
            y=[pid],
            base=start,
            orientation='h',
            name=pid,
            marker=dict(color=colors[pid]),
            text=[start],                   # mostramos el arranque
            texttemplate='%{text}',         # exactamente ese texto
            textposition='auto',            # dentro o fuera según quepa
            textfont=dict(color='black', size=12),
            hovertemplate=f"{pid}: {start}→{end}<br>Duración: {duration}<extra></extra>"
        ))

    max_end = df['end'].max()

    fig.update_layout(
        title=f"Gantt Realtime (Avg Wait Time: {avg:.2f})",
        xaxis_title='Tiempo',
        yaxis_title='Procesos',
        barmode='stack',
        xaxis=dict(
            type='linear',
            tickmode='linear',
            tick0=0,
            dtick=1,
            range=[0, max_end + 1]
        ),
        yaxis=dict(autorange='reversed'),
        bargap=0.2,
        showlegend=False,
        height=400
    )

    return fig



def plot_sync(tl):
    df = pd.DataFrame(tl)
    # Si no hay datos o faltan columnas, devolvemos una figura vacía
    if df.empty or not {'cycle','pid','status','action'}.issubset(df.columns):
        fig = go.Figure()
        fig.update_layout(title='No hay datos para Sincronización')
        return fig

    # Solo acquire
    df = df[df['action'] == 'acquire']

    # Scatter con tamaño de marcador ajustado
    fig = px.scatter(
        df,
        x='cycle',
        y='pid',
        color='status',
        symbol='status',
        color_discrete_map={'ACCESSED':'green','WAITING':'red'},
        symbol_map={'ACCESSED':'circle','WAITING':'x'},
        labels={'cycle':'Ciclo','pid':'Proceso'},
        title='Sincronización'
    )
    fig.update_traces(marker=dict(size=12))

    # Layout con ejes y leyenda claros
    fig.update_layout(
        legend_title_text='Estado',
        xaxis=dict(title='Ciclo', tickmode='linear', dtick=1),
        yaxis=dict(
            title='Proceso',
            categoryorder='array',
            categoryarray=sorted(df['pid'].unique(), reverse=True)
        ),
        margin=dict(l=50, r=20, t=50, b=50),
        height=350
    )
    return fig