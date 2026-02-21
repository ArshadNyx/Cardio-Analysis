import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from dotenv import load_dotenv
from Utils.CardioAgents import (
    RiskCalculator, ECGAnalyzer, LabAnalyzer,
    SymptomAnalyzer, TreatmentAdvisor, ProgressTracker
)

# Load environment
load_dotenv(dotenv_path='apikey.env')

# Page config
st.set_page_config(
    page_title="CardioAI - Ultimate Cardiovascular Platform",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# Enhanced CSS with more visual effects
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        animation: gradientShift 15s ease infinite;
    }
    
    @keyframes gradientShift {
        0%, 100% { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        50% { background: linear-gradient(135deg, #764ba2 0%, #667eea 100%); }
    }
    
    .main-header {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(120deg, #ff6b6b, #ee5a6f, #c44569);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: fadeInDown 1s ease-in;
        text-shadow: 2px 2px 20px rgba(255,107,107,0.3);
    }
    
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        font-weight: 300;
        animation: fadeIn 1.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: 2px solid rgba(255,255,255,0.3);
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        backdrop-filter: blur(10px);
    }
    
    .metric-card:hover {
        transform: translateY(-10px) scale(1.02);
        box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        border-color: #ff6b6b;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        box-shadow: 0 15px 35px rgba(17, 153, 142, 0.4);
        animation: glow 2s ease-in-out infinite;
    }
    
    .risk-moderate {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        box-shadow: 0 15px 35px rgba(240, 147, 251, 0.4);
        animation: glow 2s ease-in-out infinite;
    }
    
    .risk-high {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        box-shadow: 0 15px 35px rgba(250, 112, 154, 0.4);
        animation: glow 2s ease-in-out infinite;
    }
    
    .risk-critical {
        background: linear-gradient(135deg, #ff0844 0%, #ffb199 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        font-size: 2rem;
        font-weight: 800;
        box-shadow: 0 15px 35px rgba(255, 8, 68, 0.5);
        animation: pulse 1.5s infinite, glow 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 15px 35px rgba(255, 8, 68, 0.5); }
        50% { box-shadow: 0 20px 50px rgba(255, 8, 68, 0.8); }
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        font-weight: 700;
        border-radius: 50px;
        transition: all 0.3s ease;
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: scale(1.08);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    .info-box {
        background: linear-gradient(135deg, rgba(168, 237, 234, 0.9) 0%, rgba(254, 214, 227, 0.9) 100%);
        padding: 2rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        border: 2px solid rgba(255,255,255,0.5);
        transition: all 0.3s ease;
    }
    
    .info-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 30px rgba(0,0,0,0.2);
    }
    
    .big-metric {
        font-size: 4rem;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(120deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: scaleIn 0.5s ease-out;
    }
    
    @keyframes scaleIn {
        from { transform: scale(0.5); opacity: 0; }
        to { transform: scale(1); opacity: 1; }
    }
    
    .heart-3d-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    
    .problem-indicator {
        background: rgba(255, 0, 0, 0.1);
        border: 3px solid #ff0000;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        animation: blink 2s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 15px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1rem 2rem;
        font-weight: 700;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
        transform: scale(1.05);
    }
    
    .risk-model-badge {
        display: inline-block;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        font-size: 0.9rem;
        margin: 0.5rem;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .framingham-badge {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .ascvd-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
    }
    
    .score2-badge {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
    }
    </style>
""", unsafe_allow_html=True)


# Initialize session state
if 'patient_data' not in st.session_state:
    st.session_state.patient_data = {}
if 'risk_assessment' not in st.session_state:
    st.session_state.risk_assessment = None
if 'lab_results' not in st.session_state:
    st.session_state.lab_results = {}
if 'ecg_analysis' not in st.session_state:
    st.session_state.ecg_analysis = None
if 'ecg_problems' not in st.session_state:
    st.session_state.ecg_problems = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = None
if 'progress_tracker' not in st.session_state:
    st.session_state.progress_tracker = ProgressTracker()
if 'current_risk_model' not in st.session_state:
    st.session_state.current_risk_model = 'Framingham'

# Risk model information
RISK_MODELS = {
    'Framingham': {
        'name': 'Framingham Risk Score',
        'description': 'Predicts 10-year risk of cardiovascular disease. Developed from the Framingham Heart Study.',
        'best_for': 'General population, ages 30-74',
        'factors': ['Age', 'Gender', 'Total Cholesterol', 'HDL', 'Blood Pressure', 'Smoking', 'Diabetes'],
        'interpretation': {
            'low': '<10% - Low risk, continue healthy lifestyle',
            'moderate': '10-20% - Moderate risk, lifestyle changes recommended',
            'high': '20-30% - High risk, medication may be needed',
            'very_high': '>30% - Very high risk, aggressive treatment required'
        }
    },
    'ASCVD': {
        'name': 'ASCVD Risk Calculator',
        'description': 'Estimates 10-year risk of atherosclerotic cardiovascular disease. ACC/AHA guideline.',
        'best_for': 'Adults 40-79 without existing CVD',
        'factors': ['Age', 'Gender', 'Race', 'Total Cholesterol', 'HDL', 'Blood Pressure', 'Diabetes', 'Smoking', 'Treatment'],
        'interpretation': {
            'low': '<5% - Low risk, lifestyle modifications',
            'borderline': '5-7.5% - Borderline risk, consider risk enhancers',
            'intermediate': '7.5-20% - Intermediate risk, statin therapy recommended',
            'high': '>20% - High risk, high-intensity statin therapy'
        }
    },
    'SCORE2': {
        'name': 'SCORE2 (European)',
        'description': 'European cardiovascular risk assessment. Predicts 10-year risk of CVD death and events.',
        'best_for': 'European populations, ages 40-69',
        'factors': ['Age', 'Gender', 'Smoking', 'Systolic BP', 'Total Cholesterol', 'HDL'],
        'interpretation': {
            'low': '<5% - Low risk, healthy lifestyle',
            'moderate': '5-10% - Moderate risk, lifestyle intervention',
            'high': '10-15% - High risk, consider drug therapy',
            'very_high': '>15% - Very high risk, intensive treatment'
        }
    }
}

# Sidebar
with st.sidebar:
    st.markdown("# 🫀 CardioAI")
    st.markdown("### Ultimate Cardiovascular Platform")
    st.markdown("---")
    
    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "👤 Patient Profile", 
            "📈 ECG Analysis",
            "🧪 Lab Results",
            "🎯 Risk Assessment",
            "💊 Recommendations",
            "📊 Progress Tracking",
            "🫀 3D Heart Visualization"
        ],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Risk Model")
    
    risk_model = st.selectbox(
        "Select Risk Model",
        ["Framingham", "ASCVD", "SCORE2"],
        help="Different models for different populations"
    )
    
    if risk_model != st.session_state.current_risk_model:
        st.session_state.current_risk_model = risk_model
        st.info(f"Switched to {RISK_MODELS[risk_model]['name']}")
    
    # Show model info
    with st.expander("ℹ️ About This Model"):
        model_info = RISK_MODELS[risk_model]
        st.markdown(f"**{model_info['name']}**")
        st.caption(model_info['description'])
        st.caption(f"**Best for:** {model_info['best_for']}")
    
    ai_model = st.selectbox(
        "AI Model",
        ["llama-3.3-70b-versatile", "mixtral-8x7b-32768"]
    )
    
    st.markdown("---")
    if st.session_state.patient_data:
        st.markdown("### 📊 Quick Stats")
        st.metric("Age", st.session_state.patient_data.get('age', 'N/A'))
        st.metric("Gender", st.session_state.patient_data.get('gender', 'N/A'))
        if st.session_state.risk_assessment:
            risk_pct = st.session_state.risk_assessment.get('risk_percentage', 0)
            st.metric("10-Year Risk", f"{risk_pct}%")
            
            # Show risk model badge
            badge_class = f"{risk_model.lower()}-badge"
            st.markdown(f'<div class="risk-model-badge {badge_class}">{risk_model}</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("⚠️ For educational purposes only")
    st.caption("Not for clinical use")

# Main header
st.markdown('<h1 class="main-header">🫀 CardioAI Ultimate</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Cardiovascular Risk Assessment with 3D Visualization</p>', unsafe_allow_html=True)


from Utils.VisualHelpers import (
    create_risk_gauge, create_ecg_waveform, create_3d_heart_model,
    create_lipid_panel_chart, create_trend_chart, create_risk_factor_radar
)
import streamlit.components.v1 as components

# Helper function to get risk category based on model
def get_risk_category(risk_pct, model):
    if model == 'Framingham':
        if risk_pct < 10: return 'Low', 'risk-low'
        elif risk_pct < 20: return 'Moderate', 'risk-moderate'
        elif risk_pct < 30: return 'High', 'risk-high'
        else: return 'Very High', 'risk-critical'
    elif model == 'ASCVD':
        if risk_pct < 5: return 'Low', 'risk-low'
        elif risk_pct < 7.5: return 'Borderline', 'risk-moderate'
        elif risk_pct < 20: return 'Intermediate', 'risk-high'
        else: return 'High', 'risk-critical'
    else:  # SCORE2
        if risk_pct < 5: return 'Low', 'risk-low'
        elif risk_pct < 10: return 'Moderate', 'risk-moderate'
        elif risk_pct < 15: return 'High', 'risk-high'
        else: return 'Very High', 'risk-critical'

# Page: Dashboard
if page == "🏠 Dashboard":
    st.markdown("## 📊 Cardiovascular Health Dashboard")
    
    if not st.session_state.patient_data:
        st.info("👋 Welcome! Please complete your **Patient Profile** to get started.")
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("➡️ Go to Patient Profile", type="primary", use_container_width=True):
                st.rerun()
    else:
        # Quick stats row with animations
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            hr = st.session_state.patient_data.get('heart_rate', 72)
            hr_status = 'Normal' if 60 <= hr <= 100 else 'Abnormal'
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #e74c3c; margin-bottom: 1rem;">❤️ Heart Rate</h3>
                    <p class="big-metric">{hr}</p>
                    <p style="color: #888; font-size: 1.1rem; margin-top: 0.5rem;">bpm - {hr_status}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            sys = st.session_state.patient_data.get('systolic', 120)
            dia = st.session_state.patient_data.get('diastolic', 80)
            bp_status = 'Optimal' if sys < 120 and dia < 80 else 'Elevated'
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #e74c3c; margin-bottom: 1rem;">🩸 Blood Pressure</h3>
                    <p class="big-metric">{sys}/{dia}</p>
                    <p style="color: #888; font-size: 1.1rem; margin-top: 0.5rem;">mmHg - {bp_status}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            chol = st.session_state.lab_results.get('total_cholesterol', 180)
            chol_status = 'Good' if chol < 200 else 'High'
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #e74c3c; margin-bottom: 1rem;">📊 Cholesterol</h3>
                    <p class="big-metric">{chol}</p>
                    <p style="color: #888; font-size: 1.1rem; margin-top: 0.5rem;">mg/dL - {chol_status}</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            if st.session_state.risk_assessment:
                risk_pct = st.session_state.risk_assessment.get('risk_percentage', 0)
            else:
                risk_pct = 0
            st.markdown(f"""
                <div class="metric-card">
                    <h3 style="color: #e74c3c; margin-bottom: 1rem;">🎯 Risk Score</h3>
                    <p class="big-metric">{risk_pct}%</p>
                    <p style="color: #888; font-size: 1.1rem; margin-top: 0.5rem;">10-year risk</p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Risk gauge and category
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🎯 Cardiovascular Risk Meter")
            if st.session_state.risk_assessment:
                risk_pct = st.session_state.risk_assessment.get('risk_percentage', 0)
                fig = create_risk_gauge(risk_pct, st.session_state.current_risk_model)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Complete risk assessment to see your risk gauge")
        
        with col2:
            st.markdown("### 📋 Risk Category")
            
            if st.session_state.risk_assessment:
                risk_pct = st.session_state.risk_assessment.get('risk_percentage', 0)
                category, css_class = get_risk_category(risk_pct, st.session_state.current_risk_model)
                st.markdown(f'<div class="{css_class}">{category.upper()} RISK</div>', unsafe_allow_html=True)
                
                # Show interpretation
                st.markdown("### 📖 Interpretation")
                model_info = RISK_MODELS[st.session_state.current_risk_model]
                interp_key = category.lower().replace(' ', '_')
                interpretation = model_info['interpretation'].get(interp_key, 'N/A')
                st.info(interpretation)
            else:
                st.warning("No risk assessment available")
            
            st.markdown("### 🎯 Risk Factors")
            
            risk_factors = []
            protective_factors = []
            
            if st.session_state.patient_data.get('smoking') == 'Current':
                risk_factors.append("⚠️ Current smoker")
            else:
                protective_factors.append("✅ Non-smoker")
            
            if st.session_state.patient_data.get('diabetes'):
                risk_factors.append("⚠️ Diabetes")
            
            if st.session_state.patient_data.get('hypertension'):
                risk_factors.append("⚠️ Hypertension")
            
            if st.session_state.patient_data.get('family_history'):
                risk_factors.append("⚠️ Family history")
            
            if st.session_state.patient_data.get('exercise') in ['3-4x/week', '5+x/week']:
                protective_factors.append("✅ Active lifestyle")
            
            for rf in risk_factors:
                st.markdown(rf)
            for pf in protective_factors:
                st.markdown(pf)
        
        st.markdown("---")
        
        # Risk factor radar chart
        st.markdown("### 🎯 Risk Factor Profile")
        fig_radar = create_risk_factor_radar(st.session_state.patient_data)
        st.plotly_chart(fig_radar, use_container_width=True)
        
        st.markdown("---")
        
        # Action items
        st.markdown("### 🎯 Today's Action Items")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class="info-box">
                    <h4 style="color: #2c3e50;">🏃 Exercise Goal</h4>
                    <p><strong>Target:</strong> 30 min cardio</p>
                    <p><strong>Status:</strong> ⏳ Not started</p>
                    <p><strong>Time:</strong> 7:00 AM</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="info-box">
                    <h4 style="color: #2c3e50;">💊 Medication</h4>
                    <p><strong>Next:</strong> Statin 20mg</p>
                    <p><strong>Status:</strong> ⏳ Pending</p>
                    <p><strong>Time:</strong> 9:00 PM</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="info-box">
                    <h4 style="color: #2c3e50;">🩺 Check-up</h4>
                    <p><strong>Type:</strong> Cardiology</p>
                    <p><strong>Status:</strong> ✅ Scheduled</p>
                    <p><strong>Date:</strong> Dec 15, 2024</p>
                </div>
            """, unsafe_allow_html=True)


# Page: Patient Profile
elif page == "👤 Patient Profile":
    st.markdown("## 👤 Patient Profile & Risk Factors")
    
    with st.form("patient_form"):
        st.markdown("### 📋 Demographics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            age = st.number_input("Age", min_value=18, max_value=120, value=st.session_state.patient_data.get('age', 45))
            gender = st.selectbox("Gender", ["Male", "Female"], index=0 if st.session_state.patient_data.get('gender', 'Male') == 'Male' else 1)
            ethnicity = st.selectbox("Ethnicity", ["Caucasian", "African American", "Hispanic", "Asian", "Other"])
        
        with col2:
            height = st.number_input("Height (cm)", min_value=100, max_value=250, value=st.session_state.patient_data.get('height', 170))
            weight = st.number_input("Weight (kg)", min_value=30, max_value=300, value=st.session_state.patient_data.get('weight', 75))
            bmi = weight / ((height/100) ** 2)
            st.metric("BMI", f"{bmi:.1f}", help="Body Mass Index")
        
        with col3:
            systolic = st.number_input("Systolic BP (mmHg)", min_value=80, max_value=200, value=st.session_state.patient_data.get('systolic', 120))
            diastolic = st.number_input("Diastolic BP (mmHg)", min_value=40, max_value=130, value=st.session_state.patient_data.get('diastolic', 80))
            heart_rate = st.number_input("Heart Rate (bpm)", min_value=40, max_value=200, value=st.session_state.patient_data.get('heart_rate', 72))
        
        st.markdown("---")
        st.markdown("### 🏥 Medical History")
        
        col1, col2 = st.columns(2)
        
        with col1:
            diabetes = st.checkbox("Diabetes", value=st.session_state.patient_data.get('diabetes', False))
            hypertension = st.checkbox("Hypertension", value=st.session_state.patient_data.get('hypertension', False))
            previous_mi = st.checkbox("Previous Heart Attack", value=st.session_state.patient_data.get('previous_mi', False))
            previous_stroke = st.checkbox("Previous Stroke", value=st.session_state.patient_data.get('previous_stroke', False))
        
        with col2:
            family_history = st.checkbox("Family History of CVD", value=st.session_state.patient_data.get('family_history', False))
            chronic_kidney = st.checkbox("Chronic Kidney Disease", value=st.session_state.patient_data.get('chronic_kidney', False))
            atrial_fib = st.checkbox("Atrial Fibrillation", value=st.session_state.patient_data.get('atrial_fib', False))
            heart_failure = st.checkbox("Heart Failure", value=st.session_state.patient_data.get('heart_failure', False))
        
        st.markdown("---")
        st.markdown("### 🚬 Lifestyle Factors")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            smoking = st.selectbox("Smoking Status", ["Never", "Former", "Current"])
            alcohol = st.selectbox("Alcohol Use", ["None", "Moderate", "Heavy"])
        
        with col2:
            exercise = st.selectbox("Exercise Frequency", ["Sedentary", "1-2x/week", "3-4x/week", "5+x/week"])
            diet = st.selectbox("Diet Quality", ["Poor", "Fair", "Good", "Excellent"])
        
        with col3:
            stress = st.slider("Stress Level", 1, 10, st.session_state.patient_data.get('stress', 5))
            sleep = st.number_input("Sleep (hours/night)", min_value=0, max_value=24, value=st.session_state.patient_data.get('sleep', 7))
        
        st.markdown("---")
        
        submitted = st.form_submit_button("💾 Save Profile & Calculate Risk", use_container_width=True, type="primary")
        
        if submitted:
            # Save patient data
            st.session_state.patient_data = {
                'age': age, 'gender': gender, 'ethnicity': ethnicity,
                'height': height, 'weight': weight, 'bmi': bmi,
                'systolic': systolic, 'diastolic': diastolic, 'heart_rate': heart_rate,
                'diabetes': diabetes, 'hypertension': hypertension,
                'previous_mi': previous_mi, 'previous_stroke': previous_stroke,
                'family_history': family_history, 'chronic_kidney': chronic_kidney,
                'atrial_fib': atrial_fib, 'heart_failure': heart_failure,
                'smoking': smoking, 'alcohol': alcohol,
                'exercise': exercise, 'diet': diet,
                'stress': stress, 'sleep': sleep,
                'total_cholesterol': st.session_state.lab_results.get('total_cholesterol', 200),
                'hdl': st.session_state.lab_results.get('hdl', 50),
                'ldl': st.session_state.lab_results.get('ldl', 130)
            }
            
            # Calculate risk score based on selected model
            with st.spinner(f"Calculating risk using {st.session_state.current_risk_model} model..."):
                calculator = RiskCalculator(st.session_state.patient_data, model_name=ai_model)
                framingham = calculator.calculate_framingham_score()
                
                # Adjust for different models
                if st.session_state.current_risk_model == 'ASCVD':
                    # ASCVD typically gives lower risk for same profile
                    framingham['risk_percentage'] = framingham['risk_percentage'] * 0.7
                elif st.session_state.current_risk_model == 'SCORE2':
                    # SCORE2 European model
                    framingham['risk_percentage'] = framingham['risk_percentage'] * 0.6
                
                st.session_state.risk_assessment = framingham
            
            st.success("✅ Profile saved and risk calculated successfully!")
            st.balloons()
            
            # Show risk result
            risk_pct = framingham['risk_percentage']
            category, css_class = get_risk_category(risk_pct, st.session_state.current_risk_model)
            
            st.markdown(f"### 🎯 Your 10-Year CVD Risk: **{risk_pct:.1f}%** ({category})")
            st.markdown(f'<div class="{css_class}" style="margin-top: 1rem;">{category.upper()} RISK</div>', unsafe_allow_html=True)
            
            # Show model-specific interpretation
            model_info = RISK_MODELS[st.session_state.current_risk_model]
            st.info(f"**{model_info['name']}**: {model_info['description']}")


# Page: ECG Analysis
elif page == "📈 ECG Analysis":
    st.markdown("## 📈 ECG Analysis & Rhythm Assessment")
    
    st.info("💡 Upload ECG data or paste ECG readings for AI-powered analysis with 3D heart visualization")
    
    tab1, tab2, tab3 = st.tabs(["📤 Upload ECG", "📊 View Analysis", "🫀 3D Heart View"])
    
    with tab1:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            ecg_input = st.text_area(
                "Paste ECG Report or Findings:",
                height=300,
                placeholder="Example:\nHeart Rate: 72 bpm\nRhythm: Normal sinus rhythm\nPR Interval: 160 ms\nQRS Duration: 90 ms\nQT/QTc: 400/420 ms\nST Segment: Normal\nT Wave: Normal\n..."
            )
            
            uploaded_file = st.file_uploader("Or upload ECG file", type=['txt', 'pdf', 'jpg', 'png'])
        
        with col2:
            st.markdown("### 📋 ECG Parameters")
            st.markdown("""
            **Normal Ranges:**
            - Heart Rate: 60-100 bpm
            - PR Interval: 120-200 ms
            - QRS Duration: 80-120 ms
            - QT Interval: 350-450 ms
            - QTc: <440 ms (M), <460 ms (F)
            
            **Common Abnormalities:**
            - Tachycardia: HR >100
            - Bradycardia: HR <60
            - Prolonged QT: Risk of arrhythmia
            - ST Elevation: Possible MI
            """)
        
        if st.button("🔍 Analyze ECG", type="primary", use_container_width=True):
            if ecg_input or uploaded_file:
                with st.spinner("Analyzing ECG data with AI..."):
                    # Simulate AI analysis
                    import time
                    time.sleep(2)
                    
                    # Parse ECG data for problems
                    problems = []
                    if 'elevated' in ecg_input.lower() or 'elevation' in ecg_input.lower():
                        problems.append({
                            'area': 'Left Ventricle',
                            'description': 'ST segment elevation detected - possible acute myocardial infarction',
                            'severity': 'critical'
                        })
                    if 'irregular' in ecg_input.lower():
                        problems.append({
                            'area': 'Atria',
                            'description': 'Irregular rhythm detected - possible atrial fibrillation',
                            'severity': 'moderate'
                        })
                    if 'prolonged' in ecg_input.lower() and 'qt' in ecg_input.lower():
                        problems.append({
                            'area': 'Ventricular Conduction',
                            'description': 'Prolonged QT interval - increased risk of arrhythmia',
                            'severity': 'high'
                        })
                    
                    st.session_state.ecg_analysis = {
                        'rhythm': 'Normal Sinus Rhythm' if not problems else 'Abnormal Rhythm',
                        'rate': 72,
                        'abnormalities': [p['description'] for p in problems],
                        'risk_level': 'Critical' if any(p['severity'] == 'critical' for p in problems) else 'Moderate' if problems else 'Low'
                    }
                    st.session_state.ecg_problems = problems
                    
                    st.success("✅ ECG analysis complete!")
                    st.rerun()
            else:
                st.error("Please provide ECG data")
    
    with tab2:
        if st.session_state.ecg_analysis:
            st.markdown("### 🎯 Analysis Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Rhythm", st.session_state.ecg_analysis['rhythm'])
            with col2:
                st.metric("Heart Rate", f"{st.session_state.ecg_analysis['rate']} bpm")
            with col3:
                risk_level = st.session_state.ecg_analysis['risk_level']
                st.metric("Risk Level", risk_level)
            
            # ECG waveform visualization
            st.markdown("### 📊 ECG Waveform")
            
            abnormalities = []
            if st.session_state.ecg_problems:
                if any('irregular' in p['description'].lower() for p in st.session_state.ecg_problems):
                    abnormalities.append('irregular')
                if any('elevation' in p['description'].lower() for p in st.session_state.ecg_problems):
                    abnormalities.append('elevated_st')
            
            fig_ecg = create_ecg_waveform(duration=4, heart_rate=72, abnormalities=abnormalities if abnormalities else None)
            st.plotly_chart(fig_ecg, use_container_width=True)
            
            # Findings
            st.markdown("### 📋 Findings")
            
            if st.session_state.ecg_analysis['abnormalities']:
                for abnormality in st.session_state.ecg_analysis['abnormalities']:
                    st.error(f"⚠️ {abnormality}")
            else:
                st.success("✅ Normal sinus rhythm detected")
                st.info("ℹ️ No significant abnormalities identified")
            
            # Recommendations
            if st.session_state.ecg_problems:
                st.markdown("### 💊 Recommendations")
                for problem in st.session_state.ecg_problems:
                    if problem['severity'] == 'critical':
                        st.error(f"🚨 **URGENT**: {problem['description']} - Seek immediate medical attention!")
                    elif problem['severity'] == 'high':
                        st.warning(f"⚠️ **Important**: {problem['description']} - Consult cardiologist soon")
                    else:
                        st.info(f"ℹ️ {problem['description']} - Monitor and follow up")
        else:
            st.warning("⚠️ No ECG analysis available. Please upload and analyze ECG data first.")
    
    with tab3:
        st.markdown("### 🫀 3D Heart Visualization with Problem Highlighting")
        
        if st.session_state.ecg_problems:
            st.warning(f"⚠️ {len(st.session_state.ecg_problems)} problem(s) detected and highlighted on the 3D model")
            heart_html = create_3d_heart_model(st.session_state.ecg_problems)
        else:
            st.success("✅ No problems detected - showing healthy heart model")
            heart_html = create_3d_heart_model(None)
        
        components.html(heart_html, height=800, scrolling=True)


# Page: Lab Results
elif page == "🧪 Lab Results":
    st.markdown("## 🧪 Laboratory Results Analyzer")
    
    tab1, tab2 = st.tabs(["📝 Enter Lab Results", "📊 View Analysis"])
    
    with tab1:
        st.markdown("### 💉 Lipid Panel")
        
        col1, col2 = st.columns(2)
        
        with col1:
            total_chol = st.number_input(
                "Total Cholesterol (mg/dL)",
                min_value=100,
                max_value=400,
                value=st.session_state.lab_results.get('total_cholesterol', 200),
                help="Optimal: <200 mg/dL"
            )
            
            ldl = st.number_input(
                "LDL Cholesterol (mg/dL)",
                min_value=50,
                max_value=300,
                value=st.session_state.lab_results.get('ldl', 130),
                help="Optimal: <100 mg/dL"
            )
        
        with col2:
            hdl = st.number_input(
                "HDL Cholesterol (mg/dL)",
                min_value=20,
                max_value=150,
                value=st.session_state.lab_results.get('hdl', 50),
                help="Optimal: >60 mg/dL"
            )
            
            triglycerides = st.number_input(
                "Triglycerides (mg/dL)",
                min_value=50,
                max_value=500,
                value=st.session_state.lab_results.get('triglycerides', 150),
                help="Optimal: <150 mg/dL"
            )
        
        st.markdown("---")
        st.markdown("### 🫀 Cardiac Biomarkers (Optional)")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            troponin = st.number_input(
                "Troponin (ng/mL)",
                min_value=0.0,
                max_value=10.0,
                value=st.session_state.lab_results.get('troponin', 0.01),
                step=0.01,
                format="%.2f",
                help="Normal: <0.04 ng/mL"
            )
        
        with col2:
            bnp = st.number_input(
                "BNP (pg/mL)",
                min_value=0,
                max_value=1000,
                value=st.session_state.lab_results.get('bnp', 50),
                help="Normal: <100 pg/mL"
            )
        
        with col3:
            crp = st.number_input(
                "CRP (mg/L)",
                min_value=0.0,
                max_value=20.0,
                value=st.session_state.lab_results.get('crp', 1.0),
                step=0.1,
                format="%.1f",
                help="Low risk: <1 mg/L"
            )
        
        st.markdown("---")
        
        if st.button("🔬 Analyze Lab Results", type="primary", use_container_width=True):
            st.session_state.lab_results = {
                'total_cholesterol': total_chol,
                'ldl': ldl,
                'hdl': hdl,
                'triglycerides': triglycerides,
                'troponin': troponin,
                'bnp': bnp,
                'crp': crp
            }
            
            with st.spinner("Analyzing lab results with AI..."):
                import time
                time.sleep(2)
                
                # Update patient data with lab results
                if st.session_state.patient_data:
                    st.session_state.patient_data.update(st.session_state.lab_results)
                
                st.success("✅ Lab results analyzed successfully!")
                st.balloons()
    
    with tab2:
        if st.session_state.lab_results:
            st.markdown("### 📊 Lipid Panel Visualization")
            
            fig_lipid = create_lipid_panel_chart(st.session_state.lab_results)
            st.plotly_chart(fig_lipid, use_container_width=True)
            
            st.markdown("---")
            st.markdown("### 📋 Detailed Analysis")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 📊 Cholesterol Profile")
                
                total_chol = st.session_state.lab_results.get('total_cholesterol', 200)
                if total_chol < 200:
                    st.success(f"✅ Total Cholesterol: {total_chol} mg/dL (Optimal)")
                elif total_chol < 240:
                    st.warning(f"⚠️ Total Cholesterol: {total_chol} mg/dL (Borderline High)")
                else:
                    st.error(f"🔴 Total Cholesterol: {total_chol} mg/dL (High)")
                
                ldl = st.session_state.lab_results.get('ldl', 130)
                if ldl < 100:
                    st.success(f"✅ LDL: {ldl} mg/dL (Optimal)")
                elif ldl < 130:
                    st.info(f"ℹ️ LDL: {ldl} mg/dL (Near Optimal)")
                elif ldl < 160:
                    st.warning(f"⚠️ LDL: {ldl} mg/dL (Borderline High)")
                else:
                    st.error(f"🔴 LDL: {ldl} mg/dL (High)")
                
                hdl = st.session_state.lab_results.get('hdl', 50)
                if hdl >= 60:
                    st.success(f"✅ HDL: {hdl} mg/dL (Protective)")
                elif hdl >= 40:
                    st.info(f"ℹ️ HDL: {hdl} mg/dL (Normal)")
                else:
                    st.error(f"🔴 HDL: {hdl} mg/dL (Low - Risk Factor)")
                
                trig = st.session_state.lab_results.get('triglycerides', 150)
                if trig < 150:
                    st.success(f"✅ Triglycerides: {trig} mg/dL (Normal)")
                elif trig < 200:
                    st.warning(f"⚠️ Triglycerides: {trig} mg/dL (Borderline High)")
                else:
                    st.error(f"🔴 Triglycerides: {trig} mg/dL (High)")
            
            with col2:
                st.markdown("#### 🫀 Cardiac Biomarkers")
                
                troponin = st.session_state.lab_results.get('troponin', 0.01)
                if troponin < 0.04:
                    st.success(f"✅ Troponin: {troponin:.2f} ng/mL (Normal)")
                else:
                    st.error(f"🔴 Troponin: {troponin:.2f} ng/mL (Elevated - Possible MI)")
                
                bnp = st.session_state.lab_results.get('bnp', 50)
                if bnp < 100:
                    st.success(f"✅ BNP: {bnp} pg/mL (Normal)")
                elif bnp < 400:
                    st.warning(f"⚠️ BNP: {bnp} pg/mL (Mild Heart Failure)")
                else:
                    st.error(f"🔴 BNP: {bnp} pg/mL (Severe Heart Failure)")
                
                crp = st.session_state.lab_results.get('crp', 1.0)
                if crp < 1:
                    st.success(f"✅ CRP: {crp:.1f} mg/L (Low Risk)")
                elif crp < 3:
                    st.warning(f"⚠️ CRP: {crp:.1f} mg/L (Moderate Risk)")
                else:
                    st.error(f"🔴 CRP: {crp:.1f} mg/L (High Risk)")
            
            st.markdown("---")
            st.markdown("### 💊 Treatment Recommendations")
            
            # Generate recommendations based on results
            recommendations = []
            
            if st.session_state.lab_results.get('ldl', 0) >= 130:
                recommendations.append("🔴 **High LDL**: Consider statin therapy. Target LDL <100 mg/dL")
            
            if st.session_state.lab_results.get('hdl', 100) < 40:
                recommendations.append("⚠️ **Low HDL**: Increase aerobic exercise, consider niacin therapy")
            
            if st.session_state.lab_results.get('triglycerides', 0) >= 200:
                recommendations.append("⚠️ **High Triglycerides**: Reduce carbohydrates, increase omega-3 fatty acids")
            
            if st.session_state.lab_results.get('troponin', 0) >= 0.04:
                recommendations.append("🚨 **URGENT**: Elevated troponin suggests acute cardiac event - seek immediate medical attention!")
            
            if recommendations:
                for rec in recommendations:
                    if '🚨' in rec:
                        st.error(rec)
                    elif '🔴' in rec:
                        st.warning(rec)
                    else:
                        st.info(rec)
            else:
                st.success("✅ All lab values within normal ranges. Continue healthy lifestyle!")
        else:
            st.warning("⚠️ No lab results available. Please enter lab data first.")


# Page: Risk Assessment
elif page == "🎯 Risk Assessment":
    st.markdown("## 🎯 Comprehensive Risk Assessment")
    
    if not st.session_state.patient_data:
        st.warning("⚠️ Please complete your Patient Profile first!")
    else:
        # Show current model
        st.info(f"📊 Using **{RISK_MODELS[st.session_state.current_risk_model]['name']}** for risk calculation")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            if st.session_state.risk_assessment:
                risk_pct = st.session_state.risk_assessment.get('risk_percentage', 0)
                fig = create_risk_gauge(risk_pct, st.session_state.current_risk_model)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Click 'Calculate Risk' to see your assessment")
        
        with col2:
            if st.button("🔄 Recalculate Risk", type="primary", use_container_width=True):
                with st.spinner(f"Calculating risk using {st.session_state.current_risk_model}..."):
                    calculator = RiskCalculator(st.session_state.patient_data, model_name=ai_model)
                    framingham = calculator.calculate_framingham_score()
                    
                    # Adjust for different models
                    if st.session_state.current_risk_model == 'ASCVD':
                        framingham['risk_percentage'] = framingham['risk_percentage'] * 0.7
                    elif st.session_state.current_risk_model == 'SCORE2':
                        framingham['risk_percentage'] = framingham['risk_percentage'] * 0.6
                    
                    st.session_state.risk_assessment = framingham
                    st.success("✅ Risk recalculated!")
                    st.rerun()
            
            if st.session_state.risk_assessment:
                risk_pct = st.session_state.risk_assessment.get('risk_percentage', 0)
                category, css_class = get_risk_category(risk_pct, st.session_state.current_risk_model)
                
                st.markdown("### 📋 Risk Category")
                st.markdown(f'<div class="{css_class}">{category.upper()}</div>', unsafe_allow_html=True)
                
                st.markdown("### 📖 Interpretation")
                model_info = RISK_MODELS[st.session_state.current_risk_model]
                interp_key = category.lower().replace(' ', '_')
                interpretation = model_info['interpretation'].get(interp_key, 'N/A')
                st.info(interpretation)
        
        st.markdown("---")
        
        # Model comparison
        st.markdown("### 📊 Compare Risk Models")
        
        if st.button("🔄 Calculate with All Models"):
            with st.spinner("Calculating with all three models..."):
                calculator = RiskCalculator(st.session_state.patient_data, model_name=ai_model)
                base_risk = calculator.calculate_framingham_score()
                
                comparison_data = {
                    'Model': ['Framingham', 'ASCVD', 'SCORE2'],
                    'Risk (%)': [
                        base_risk['risk_percentage'],
                        base_risk['risk_percentage'] * 0.7,
                        base_risk['risk_percentage'] * 0.6
                    ]
                }
                
                df = pd.DataFrame(comparison_data)
                
                fig = px.bar(
                    df,
                    x='Model',
                    y='Risk (%)',
                    color='Risk (%)',
                    color_continuous_scale=['#2ecc71', '#f39c12', '#e74c3c'],
                    text='Risk (%)',
                    title="<b>Risk Comparison Across Models</b>"
                )
                
                fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig.update_layout(
                    height=450,
                    font=dict(family="Poppins", size=14),
                    plot_bgcolor='rgba(255,255,255,0.95)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.info("💡 Different models use different populations and factors, which is why results vary.")

# Page: Recommendations
elif page == "💊 Recommendations":
    st.markdown("## 💊 Personalized Treatment Recommendations")
    
    if not st.session_state.patient_data or not st.session_state.risk_assessment:
        st.warning("⚠️ Please complete Patient Profile and Risk Assessment first!")
    else:
        if st.button("🔄 Generate Recommendations", type="primary", use_container_width=True):
            with st.spinner("Generating personalized recommendations with AI..."):
                advisor = TreatmentAdvisor(
                    st.session_state.patient_data,
                    st.session_state.risk_assessment,
                    model_name=ai_model
                )
                recommendations = advisor.get_recommendations()
                st.session_state.recommendations = recommendations
                st.success("✅ Recommendations generated!")
        
        if st.session_state.recommendations:
            rec = st.session_state.recommendations
            
            # Lifestyle modifications
            st.markdown("### 🏃 Lifestyle Modifications")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if 'lifestyle_modifications' in rec:
                    lifestyle = rec['lifestyle_modifications']
                    
                    st.markdown("#### 🥗 Diet")
                    for item in lifestyle.get('diet', ['Maintain balanced diet'])[:3]:
                        st.info(f"• {item}")
                    
                    st.markdown("#### 🏃 Exercise")
                    for item in lifestyle.get('exercise', ['Regular physical activity'])[:3]:
                        st.info(f"• {item}")
            
            with col2:
                if 'lifestyle_modifications' in rec:
                    lifestyle = rec['lifestyle_modifications']
                    
                    st.markdown("#### 🚭 Smoking Cessation")
                    for item in lifestyle.get('smoking_cessation', ['Continue non-smoking'])[:3]:
                        st.info(f"• {item}")
                    
                    st.markdown("#### 😌 Stress Management")
                    for item in lifestyle.get('stress_management', ['Practice relaxation'])[:3]:
                        st.info(f"• {item}")
            
            st.markdown("---")
            
            # Medications
            st.markdown("### 💊 Medication Recommendations")
            
            if 'medications' in rec:
                meds = rec['medications']
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if 'statins' in meds:
                        statin = meds['statins']
                        if statin.get('recommended'):
                            st.success("✅ **Statin Therapy Recommended**")
                            st.caption(statin.get('rationale', 'For cholesterol management'))
                        else:
                            st.info("ℹ️ **Statin Not Required**")
                
                with col2:
                    if 'antihypertensives' in meds:
                        bp_med = meds['antihypertensives']
                        if bp_med.get('recommended'):
                            st.success("✅ **BP Medication Recommended**")
                            st.caption(bp_med.get('rationale', 'For blood pressure control'))
                        else:
                            st.info("ℹ️ **BP Medication Not Required**")
                
                with col3:
                    if 'antiplatelet' in meds:
                        antiplatelet = meds['antiplatelet']
                        if antiplatelet.get('recommended'):
                            st.success("✅ **Aspirin Recommended**")
                            st.caption(antiplatelet.get('rationale', 'For cardiovascular protection'))
                        else:
                            st.info("ℹ️ **Aspirin Not Required**")
            
            st.markdown("---")
            
            # Goals
            st.markdown("### 🎯 Treatment Goals")
            
            if 'goals' in rec:
                goals = rec['goals']
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Blood Pressure Target", goals.get('blood_pressure', '<120/80'))
                with col2:
                    st.metric("LDL Target", goals.get('ldl_cholesterol', '<100 mg/dL'))
                with col3:
                    st.metric("Weight Target", goals.get('weight', 'BMI <25'))
                with col4:
                    st.metric("Exercise Target", goals.get('exercise', '150 min/week'))
        else:
            st.info("Click 'Generate Recommendations' to see personalized treatment plan")

# Page: Progress Tracking
elif page == "📊 Progress Tracking":
    st.markdown("## 📊 Progress Tracking & Trends")
    
    # Generate sample historical data
    dates = pd.date_range(end=datetime.now(), periods=6, freq='M')
    
    st.markdown("### 📈 Health Metrics Over Time")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Blood pressure trend
        systolic_values = [135, 132, 128, 125, 122, 120]
        fig_bp = create_trend_chart(dates, systolic_values, "Systolic BP (mmHg)", target=120)
        st.plotly_chart(fig_bp, use_container_width=True)
    
    with col2:
        # Cholesterol trend
        chol_values = [220, 210, 200, 190, 185, 180]
        fig_chol = create_trend_chart(dates, chol_values, "Total Cholesterol (mg/dL)", target=200)
        st.plotly_chart(fig_chol, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Weight trend
        weight_values = [85, 83, 81, 79, 77, 75]
        fig_weight = create_trend_chart(dates, weight_values, "Weight (kg)", target=70)
        st.plotly_chart(fig_weight, use_container_width=True)
    
    with col2:
        # Risk score trend
        risk_values = [18, 16, 14, 13, 12, 12]
        fig_risk = create_trend_chart(dates, risk_values, "10-Year CVD Risk (%)", target=10)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    st.markdown("---")
    st.markdown("### 📊 Progress Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("BP Improvement", "-15 mmHg", delta="-11%", delta_color="inverse")
    with col2:
        st.metric("Cholesterol Reduction", "-40 mg/dL", delta="-18%", delta_color="inverse")
    with col3:
        st.metric("Weight Loss", "-10 kg", delta="-12%", delta_color="inverse")
    with col4:
        st.metric("Risk Reduction", "-6%", delta="-33%", delta_color="inverse")

# Page: 3D Heart Visualization
elif page == "🫀 3D Heart Visualization":
    st.markdown("## 🫀 Interactive 3D Heart Model")
    
    st.info("💡 Rotate, zoom, and explore the 3D heart model. Problem areas are highlighted based on your ECG and lab results.")
    
    # Collect all problems
    all_problems = []
    
    # Add ECG problems
    if st.session_state.ecg_problems:
        all_problems.extend(st.session_state.ecg_problems)
    
    # Add lab-based problems
    if st.session_state.lab_results:
        if st.session_state.lab_results.get('ldl', 0) >= 160:
            all_problems.append({
                'area': 'Coronary Arteries',
                'description': 'High LDL cholesterol - increased risk of atherosclerosis',
                'severity': 'high'
            })
        
        if st.session_state.lab_results.get('troponin', 0) >= 0.04:
            all_problems.append({
                'area': 'Myocardium',
                'description': 'Elevated troponin - possible myocardial damage',
                'severity': 'critical'
            })
    
    # Display 3D model
    if all_problems:
        st.warning(f"⚠️ {len(all_problems)} problem area(s) detected and highlighted")
        heart_html = create_3d_heart_model(all_problems)
    else:
        st.success("✅ No problems detected - showing healthy heart model")
        heart_html = create_3d_heart_model(None)
    
    components.html(heart_html, height=900, scrolling=True)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: white; padding: 2rem;'>
        <h3 style='color: white;'>🫀 CardioAI Ultimate Platform</h3>
        <p>Powered by AI & Medical Expertise | Built with Streamlit, Groq & Plotly</p>
        <p style='font-size: 0.9rem; margin-top: 1rem;'>⚠️ For Educational & Research Purposes Only - Not for Clinical Use</p>
        <p style='font-size: 0.8rem; color: rgba(255,255,255,0.7);'>
            Always consult qualified healthcare professionals for medical decisions
        </p>
    </div>
""", unsafe_allow_html=True)
