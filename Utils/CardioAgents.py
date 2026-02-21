from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import json
import numpy as np

class CardioAgent:
    """Base class for cardiovascular assessment agents"""
    
    def __init__(self, model_name="llama-3.3-70b-versatile", temperature=0):
        self.model = ChatGroq(temperature=temperature, model=model_name)
        self.response = None
        
    def parse_json_response(self, response_text):
        """Safely parse JSON from LLM response"""
        try:
            return json.loads(response_text)
        except:
            return {"raw_response": response_text, "error": "Failed to parse JSON"}


class RiskCalculator(CardioAgent):
    """Calculate cardiovascular risk scores"""
    
    def __init__(self, patient_data, model_name="llama-3.3-70b-versatile"):
        super().__init__(model_name)
        self.patient_data = patient_data
        
    def calculate_framingham_score(self):
        """Calculate Framingham Risk Score"""
        # Simplified calculation (real implementation would be more complex)
        age = self.patient_data.get('age', 50)
        gender = self.patient_data.get('gender', 'Male')
        systolic = self.patient_data.get('systolic', 120)
        cholesterol = self.patient_data.get('total_cholesterol', 200)
        hdl = self.patient_data.get('hdl', 50)
        smoking = self.patient_data.get('smoking', 'Never') == 'Current'
        diabetes = self.patient_data.get('diabetes', False)
        
        # Simplified point system
        points = 0
        
        # Age points
        if gender == 'Male':
            if age >= 70: points += 11
            elif age >= 60: points += 8
            elif age >= 50: points += 5
            elif age >= 40: points += 2
        else:
            if age >= 70: points += 12
            elif age >= 60: points += 9
            elif age >= 50: points += 6
            elif age >= 40: points += 3
        
        # Cholesterol points
        if cholesterol >= 280: points += 3
        elif cholesterol >= 240: points += 2
        elif cholesterol >= 200: points += 1
        
        # HDL points
        if hdl < 35: points += 2
        elif hdl < 45: points += 1
        elif hdl >= 60: points -= 1
        
        # Blood pressure points
        if systolic >= 160: points += 3
        elif systolic >= 140: points += 2
        elif systolic >= 130: points += 1
        
        # Risk factors
        if smoking: points += 2
        if diabetes: points += 2
        
        # Convert points to risk percentage (simplified)
        risk_percentage = min(points * 2, 50)
        
        return {
            'score': points,
            'risk_percentage': risk_percentage,
            'risk_category': self._categorize_risk(risk_percentage)
        }
    
    def _categorize_risk(self, risk_percentage):
        """Categorize risk level"""
        if risk_percentage < 10:
            return 'Low'
        elif risk_percentage < 20:
            return 'Moderate'
        elif risk_percentage < 30:
            return 'High'
        else:
            return 'Very High'
    
    def get_ai_risk_assessment(self):
        """Get AI-powered risk assessment"""
        prompt = PromptTemplate.from_template("""
            You are a cardiovascular risk assessment specialist. Analyze the patient data and provide a comprehensive risk assessment.
            
            Patient Data:
            {patient_data}
            
            Provide your assessment in this JSON format:
            {{
                "overall_risk": "low/moderate/high/very_high",
                "10_year_risk_percentage": 0-100,
                "key_risk_factors": ["factor1", "factor2"],
                "protective_factors": ["factor1", "factor2"],
                "immediate_concerns": ["concern1", "concern2"],
                "recommendations": ["recommendation1", "recommendation2"],
                "confidence_score": 0.0-1.0
            }}
        """)
        
        formatted_prompt = prompt.format(patient_data=json.dumps(self.patient_data, indent=2))
        response = self.model.invoke(formatted_prompt)
        return self.parse_json_response(response.content)


class ECGAnalyzer(CardioAgent):
    """Analyze ECG data for abnormalities"""
    
    def __init__(self, ecg_data, model_name="llama-3.3-70b-versatile"):
        super().__init__(model_name)
        self.ecg_data = ecg_data
        
    def analyze(self):
        """Analyze ECG data"""
        prompt = PromptTemplate.from_template("""
            You are an expert cardiologist specializing in ECG interpretation. Analyze the ECG data provided.
            
            ECG Data:
            {ecg_data}
            
            Provide your analysis in this JSON format:
            {{
                "rhythm": "description of rhythm",
                "heart_rate": number,
                "intervals": {{
                    "pr_interval": "normal/abnormal",
                    "qrs_duration": "normal/abnormal",
                    "qt_interval": "normal/abnormal"
                }},
                "abnormalities": ["abnormality1", "abnormality2"],
                "severity": "normal/mild/moderate/severe",
                "clinical_significance": "description",
                "urgent_findings": ["finding1", "finding2"],
                "recommendations": ["recommendation1", "recommendation2"],
                "confidence_score": 0.0-1.0
            }}
        """)
        
        formatted_prompt = prompt.format(ecg_data=self.ecg_data)
        response = self.model.invoke(formatted_prompt)
        return self.parse_json_response(response.content)


class LabAnalyzer(CardioAgent):
    """Analyze cardiovascular-related lab results"""
    
    def __init__(self, lab_data, model_name="llama-3.3-70b-versatile"):
        super().__init__(model_name)
        self.lab_data = lab_data
        
    def analyze_lipid_panel(self):
        """Analyze lipid panel results"""
        prompt = PromptTemplate.from_template("""
            You are a clinical pathologist specializing in cardiovascular biomarkers. Analyze the lipid panel.
            
            Lab Results:
            {lab_data}
            
            Provide your analysis in this JSON format:
            {{
                "total_cholesterol": {{
                    "value": number,
                    "status": "optimal/borderline/high",
                    "target": "target value"
                }},
                "ldl_cholesterol": {{
                    "value": number,
                    "status": "optimal/near_optimal/borderline/high/very_high",
                    "target": "target value"
                }},
                "hdl_cholesterol": {{
                    "value": number,
                    "status": "low/normal/high",
                    "target": "target value"
                }},
                "triglycerides": {{
                    "value": number,
                    "status": "normal/borderline/high/very_high",
                    "target": "target value"
                }},
                "risk_assessment": "low/moderate/high",
                "recommendations": ["recommendation1", "recommendation2"],
                "treatment_needed": true/false,
                "confidence_score": 0.0-1.0
            }}
        """)
        
        formatted_prompt = prompt.format(lab_data=json.dumps(self.lab_data, indent=2))
        response = self.model.invoke(formatted_prompt)
        return self.parse_json_response(response.content)
    
    def analyze_cardiac_biomarkers(self):
        """Analyze cardiac biomarkers (troponin, BNP, etc.)"""
        prompt = PromptTemplate.from_template("""
            You are a cardiologist analyzing cardiac biomarkers. Evaluate the results for acute cardiac events.
            
            Biomarker Results:
            {lab_data}
            
            Provide your analysis in this JSON format:
            {{
                "troponin": {{
                    "value": number,
                    "status": "normal/elevated/highly_elevated",
                    "interpretation": "description"
                }},
                "bnp_or_nt_probnp": {{
                    "value": number,
                    "status": "normal/elevated",
                    "interpretation": "description"
                }},
                "crp": {{
                    "value": number,
                    "status": "normal/elevated",
                    "interpretation": "description"
                }},
                "acute_event_risk": "low/moderate/high/critical",
                "urgent_action_needed": true/false,
                "recommendations": ["recommendation1", "recommendation2"],
                "confidence_score": 0.0-1.0
            }}
        """)
        
        formatted_prompt = prompt.format(lab_data=json.dumps(self.lab_data, indent=2))
        response = self.model.invoke(formatted_prompt)
        return self.parse_json_response(response.content)


class SymptomAnalyzer(CardioAgent):
    """Analyze cardiovascular symptoms"""
    
    def __init__(self, symptoms, model_name="llama-3.3-70b-versatile"):
        super().__init__(model_name)
        self.symptoms = symptoms
        
    def analyze_chest_pain(self):
        """Analyze chest pain characteristics"""
        prompt = PromptTemplate.from_template("""
            You are an emergency cardiologist evaluating chest pain. Assess the likelihood of acute coronary syndrome.
            
            Symptom Description:
            {symptoms}
            
            Provide your assessment in this JSON format:
            {{
                "pain_characteristics": {{
                    "location": "description",
                    "quality": "description",
                    "radiation": "description",
                    "duration": "description",
                    "triggers": ["trigger1", "trigger2"]
                }},
                "acs_probability": "low/intermediate/high",
                "differential_diagnoses": ["diagnosis1", "diagnosis2"],
                "urgency_level": "routine/urgent/emergency",
                "immediate_actions": ["action1", "action2"],
                "recommended_tests": ["test1", "test2"],
                "confidence_score": 0.0-1.0
            }}
        """)
        
        formatted_prompt = prompt.format(symptoms=self.symptoms)
        response = self.model.invoke(formatted_prompt)
        return self.parse_json_response(response.content)


class TreatmentAdvisor(CardioAgent):
    """Provide treatment recommendations"""
    
    def __init__(self, patient_data, risk_assessment, model_name="llama-3.3-70b-versatile"):
        super().__init__(model_name)
        self.patient_data = patient_data
        self.risk_assessment = risk_assessment
        
    def get_recommendations(self):
        """Get comprehensive treatment recommendations"""
        prompt = PromptTemplate.from_template("""
            You are a preventive cardiologist creating a comprehensive cardiovascular risk reduction plan.
            
            Patient Data:
            {patient_data}
            
            Risk Assessment:
            {risk_assessment}
            
            Provide recommendations in this JSON format:
            {{
                "lifestyle_modifications": {{
                    "diet": ["recommendation1", "recommendation2"],
                    "exercise": ["recommendation1", "recommendation2"],
                    "smoking_cessation": ["recommendation1", "recommendation2"],
                    "stress_management": ["recommendation1", "recommendation2"],
                    "sleep": ["recommendation1", "recommendation2"]
                }},
                "medications": {{
                    "statins": {{
                        "recommended": true/false,
                        "rationale": "explanation"
                    }},
                    "antihypertensives": {{
                        "recommended": true/false,
                        "rationale": "explanation"
                    }},
                    "antiplatelet": {{
                        "recommended": true/false,
                        "rationale": "explanation"
                    }}
                }},
                "monitoring": {{
                    "frequency": "description",
                    "tests": ["test1", "test2"],
                    "follow_up": "timeline"
                }},
                "goals": {{
                    "blood_pressure": "target",
                    "ldl_cholesterol": "target",
                    "weight": "target",
                    "exercise": "target"
                }},
                "priority_actions": ["action1", "action2"],
                "confidence_score": 0.0-1.0
            }}
        """)
        
        formatted_prompt = prompt.format(
            patient_data=json.dumps(self.patient_data, indent=2),
            risk_assessment=json.dumps(self.risk_assessment, indent=2)
        )
        response = self.model.invoke(formatted_prompt)
        return self.parse_json_response(response.content)


class ProgressTracker:
    """Track patient progress over time"""
    
    def __init__(self):
        self.history = []
    
    def add_measurement(self, date, measurements):
        """Add new measurements"""
        self.history.append({
            'date': date,
            'measurements': measurements
        })
    
    def get_trends(self):
        """Calculate trends"""
        if len(self.history) < 2:
            return {"error": "Insufficient data for trend analysis"}
        
        trends = {}
        metrics = ['systolic', 'diastolic', 'total_cholesterol', 'ldl', 'hdl', 'weight']
        
        for metric in metrics:
            values = [h['measurements'].get(metric) for h in self.history if metric in h['measurements']]
            if len(values) >= 2:
                trend = 'improving' if values[-1] < values[0] else 'worsening' if values[-1] > values[0] else 'stable'
                change = values[-1] - values[0]
                trends[metric] = {
                    'trend': trend,
                    'change': change,
                    'current': values[-1],
                    'baseline': values[0]
                }
        
        return trends
    
    def generate_progress_report(self):
        """Generate comprehensive progress report"""
        trends = self.get_trends()
        
        report = {
            'total_measurements': len(self.history),
            'date_range': {
                'start': self.history[0]['date'] if self.history else None,
                'end': self.history[-1]['date'] if self.history else None
            },
            'trends': trends,
            'overall_progress': self._assess_overall_progress(trends)
        }
        
        return report
    
    def _assess_overall_progress(self, trends):
        """Assess overall progress"""
        if not trends:
            return "insufficient_data"
        
        improving_count = sum(1 for t in trends.values() if t['trend'] == 'improving')
        worsening_count = sum(1 for t in trends.values() if t['trend'] == 'worsening')
        
        if improving_count > worsening_count:
            return "improving"
        elif worsening_count > improving_count:
            return "worsening"
        else:
            return "stable"
