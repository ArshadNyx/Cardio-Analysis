import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

def create_risk_gauge(risk_value, risk_model='Framingham'):
    """Create animated risk gauge based on model"""
    
    # Different thresholds for different models
    thresholds = {
        'Framingham': [10, 20, 30, 50],
        'ASCVD': [5, 7.5, 20, 50],
        'SCORE2': [5, 10, 15, 50]
    }
    
    colors = {
        'Framingham': ['#2ecc71', '#f39c12', '#e67e22', '#e74c3c'],
        'ASCVD': ['#3498db', '#9b59b6', '#e67e22', '#e74c3c'],
        'SCORE2': ['#1abc9c', '#f39c12', '#e67e22', '#c0392b']
    }
    
    thresh = thresholds.get(risk_model, thresholds['Framingham'])
    color_scheme = colors.get(risk_model, colors['Framingham'])
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = risk_value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {
            'text': f"<b>10-Year CVD Risk (%)</b><br><span style='font-size:0.8em;color:gray'>{risk_model} Model</span>",
            'font': {'size': 28, 'color': '#2c3e50'}
        },
        delta = {
            'reference': thresh[0],
            'increasing': {'color': "#e74c3c"},
            'decreasing': {'color': "#2ecc71"}
        },
        number = {'font': {'size': 60, 'color': '#2c3e50'}, 'suffix': '%'},
        gauge = {
            'axis': {
                'range': [None, thresh[3]],
                'tickwidth': 3,
                'tickcolor': "#2c3e50",
                'tickfont': {'size': 16}
            },
            'bar': {'color': "#e74c3c", 'thickness': 0.8},
            'bgcolor': "white",
            'borderwidth': 4,
            'bordercolor': "#ecf0f1",
            'steps': [
                {'range': [0, thresh[0]], 'color': color_scheme[0]},
                {'range': [thresh[0], thresh[1]], 'color': color_scheme[1]},
                {'range': [thresh[1], thresh[2]], 'color': color_scheme[2]},
                {'range': [thresh[2], thresh[3]], 'color': color_scheme[3]}
            ],
            'threshold': {
                'line': {'color': "#c0392b", 'width': 8},
                'thickness': 0.9,
                'value': risk_value
            }
        }
    ))
    
    fig.update_layout(
        height=500,
        font={'color': "#2c3e50", 'family': "Poppins"},
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    return fig

def create_ecg_waveform(duration=4, heart_rate=72, abnormalities=None):
    """Create realistic ECG waveform with optional abnormalities"""
    
    samples = 1000
    t = np.linspace(0, duration, samples)
    
    # Normal ECG components
    ecg = np.zeros(samples)
    beats = int(heart_rate * duration / 60)
    
    for beat in range(beats):
        beat_time = beat * 60 / heart_rate
        beat_idx = int(beat_time * samples / duration)
        
        # P wave
        p_wave = 0.15 * np.exp(-((t - beat_time - 0.1)**2) / 0.001)
        # QRS complex
        qrs = 1.0 * np.exp(-((t - beat_time - 0.2)**2) / 0.0005)
        # T wave
        t_wave = 0.3 * np.exp(-((t - beat_time - 0.4)**2) / 0.002)
        
        ecg += p_wave + qrs + t_wave
    
    # Add abnormalities if specified
    if abnormalities:
        if 'irregular' in abnormalities:
            ecg += 0.1 * np.random.randn(samples)
        if 'elevated_st' in abnormalities:
            ecg += 0.2
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=t,
        y=ecg,
        mode='lines',
        name='ECG',
        line=dict(color='#e74c3c', width=3),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.1)'
    ))
    
    # Add grid
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(231, 76, 60, 0.2)',
        dtick=0.2
    )
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor='rgba(231, 76, 60, 0.2)',
        dtick=0.2
    )
    
    fig.update_layout(
        title="<b>ECG Trace (Lead II)</b>",
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude (mV)",
        height=400,
        showlegend=False,
        font=dict(family="Poppins", size=14),
        plot_bgcolor='rgba(255,255,255,0.95)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=20, t=60, b=50)
    )
    
    return fig

def create_3d_heart_model(problems=None):
    """Create 3D heart visualization with problem highlighting"""
    
    # Sketchfab embed with problem overlay
    heart_html = """
    <div class="heart-3d-container">
        <div style="position: relative;">
            <iframe 
                title="Human Heart Cross Section model" 
                frameborder="0" 
                allowfullscreen 
                mozallowfullscreen="true" 
                webkitallowfullscreen="true" 
                allow="autoplay; fullscreen; xr-spatial-tracking" 
                xr-spatial-tracking 
                execution-while-out-of-viewport 
                execution-while-not-rendered 
                web-share 
                width="100%" 
                height="600" 
                src="https://sketchfab.com/models/dfa78cdfa98744cc8643e37acc25e4ea/embed?autostart=1&ui_theme=dark">
            </iframe>
    """
    
    if problems:
        heart_html += '<div style="margin-top: 1rem;">'
        heart_html += '<h3 style="color: #e74c3c;">⚠️ Detected Problems:</h3>'
        for problem in problems:
            heart_html += f'<div class="problem-indicator">🔴 <strong>{problem["area"]}</strong>: {problem["description"]}</div>'
        heart_html += '</div>'
    
    heart_html += """
        </div>
        <p style="font-size: 13px; font-weight: normal; margin: 10px 0; color: #7f8c8d; text-align: center;">
            <a href="https://sketchfab.com/3d-models/human-heart-cross-section-model-dfa78cdfa98744cc8643e37acc25e4ea" 
               target="_blank" style="font-weight: bold; color: #e74c3c;">
                Human Heart Cross Section model
            </a> by 
            <a href="https://sketchfab.com/arloopa" target="_blank" style="font-weight: bold; color: #e74c3c;">
                arloopa
            </a> on 
            <a href="https://sketchfab.com" target="_blank" style="font-weight: bold; color: #e74c3c;">
                Sketchfab
            </a>
        </p>
    </div>
    """
    
    return heart_html

def create_lipid_panel_chart(lab_data):
    """Create beautiful lipid panel visualization"""
    
    # Target ranges
    targets = {
        'Total Cholesterol': {'value': lab_data.get('total_cholesterol', 200), 'optimal': 200, 'max': 300},
        'LDL': {'value': lab_data.get('ldl', 100), 'optimal': 100, 'max': 200},
        'HDL': {'value': lab_data.get('hdl', 60), 'optimal': 60, 'max': 100},
        'Triglycerides': {'value': lab_data.get('triglycerides', 150), 'optimal': 150, 'max': 300}
    }
    
    fig = go.Figure()
    
    for i, (test, data) in enumerate(targets.items()):
        # Actual value bar
        color = '#2ecc71' if data['value'] <= data['optimal'] else '#e74c3c'
        
        fig.add_trace(go.Bar(
            name=test,
            x=[test],
            y=[data['value']],
            marker_color=color,
            text=[f"{data['value']} mg/dL"],
            textposition='outside',
            textfont=dict(size=14, color=color, family="Poppins", weight='bold'),
            hovertemplate=f"<b>{test}</b><br>Value: {data['value']} mg/dL<br>Target: <{data['optimal']} mg/dL<extra></extra>"
        ))
        
        # Target line
        fig.add_shape(
            type="line",
            x0=i-0.4, x1=i+0.4,
            y0=data['optimal'], y1=data['optimal'],
            line=dict(color="#3498db", width=3, dash="dash")
        )
    
    fig.update_layout(
        title="<b>Lipid Panel Results</b>",
        yaxis_title="mg/dL",
        height=450,
        showlegend=False,
        font=dict(family="Poppins", size=14),
        plot_bgcolor='rgba(255,255,255,0.95)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=20, t=80, b=50),
        hovermode='x unified'
    )
    
    return fig

def create_trend_chart(dates, values, metric_name, target=None):
    """Create animated trend chart"""
    
    fig = go.Figure()
    
    # Main trend line
    fig.add_trace(go.Scatter(
        x=dates,
        y=values,
        mode='lines+markers',
        name=metric_name,
        line=dict(color='#667eea', width=4),
        marker=dict(size=12, color='#764ba2', line=dict(color='white', width=2)),
        fill='tozeroy',
        fillcolor='rgba(102, 126, 234, 0.2)',
        hovertemplate=f"<b>{metric_name}</b><br>Date: %{{x}}<br>Value: %{{y}}<extra></extra>"
    ))
    
    # Target line if provided
    if target:
        fig.add_hline(
            y=target,
            line_dash="dash",
            line_color="#2ecc71",
            line_width=3,
            annotation_text=f"Target: {target}",
            annotation_position="right"
        )
    
    fig.update_layout(
        title=f"<b>{metric_name} Trend</b>",
        xaxis_title="Date",
        yaxis_title=metric_name,
        height=400,
        font=dict(family="Poppins", size=14),
        plot_bgcolor='rgba(255,255,255,0.95)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=50, r=20, t=60, b=50),
        hovermode='x unified'
    )
    
    return fig

def create_risk_factor_radar(patient_data):
    """Create radar chart for risk factors"""
    
    categories = ['Age', 'BP', 'Cholesterol', 'Lifestyle', 'Family History']
    
    # Calculate scores (0-100)
    age_score = min((patient_data.get('age', 45) / 80) * 100, 100)
    bp_score = min((patient_data.get('systolic', 120) / 180) * 100, 100)
    chol_score = min((patient_data.get('total_cholesterol', 200) / 300) * 100, 100)
    
    lifestyle_score = 0
    if patient_data.get('smoking') == 'Current':
        lifestyle_score += 40
    if patient_data.get('exercise') == 'Sedentary':
        lifestyle_score += 30
    if patient_data.get('diet') == 'Poor':
        lifestyle_score += 30
    
    family_score = 100 if patient_data.get('family_history') else 20
    
    values = [age_score, bp_score, chol_score, lifestyle_score, family_score]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(231, 76, 60, 0.3)',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=10, color='#c0392b'),
        name='Risk Factors'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=12),
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, family="Poppins", weight='bold')
            ),
            bgcolor='rgba(255,255,255,0.95)'
        ),
        showlegend=False,
        title="<b>Risk Factor Profile</b>",
        height=450,
        font=dict(family="Poppins", size=14),
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    return fig
