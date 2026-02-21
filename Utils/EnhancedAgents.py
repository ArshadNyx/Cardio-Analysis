from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import json

class MedicalAgent:
    """Base class for all medical specialist agents"""
    
    def __init__(self, medical_report=None, role=None, extra_info=None, model_name="llama-3.3-70b-versatile", temperature=0):
        self.medical_report = medical_report
        self.role = role
        self.extra_info = extra_info or {}
        self.model = ChatGroq(temperature=temperature, model=model_name)
        self.prompt_template = self.create_prompt_template()
        self.response = None
        self.confidence_score = 0.0
        
    def create_prompt_template(self):
        """Create role-specific prompt templates"""
        templates = {
            "Cardiologist": """
                Act as an expert cardiologist. Analyze the patient's medical report with focus on cardiovascular health.
                
                Task: Review cardiac workup including ECG, blood tests, Holter monitor, echocardiogram, and any cardiac symptoms.
                
                Focus Areas:
                - Arrhythmias and heart rhythm abnormalities
                - Structural heart issues (valve problems, cardiomyopathy)
                - Coronary artery disease indicators
                - Blood pressure and circulation issues
                - Heart failure signs
                
                Provide your assessment in this JSON format:
                {{
                    "findings": ["list of key cardiac findings"],
                    "possible_conditions": ["list of potential cardiac conditions"],
                    "severity": "low/moderate/high",
                    "recommended_tests": ["list of recommended cardiac tests"],
                    "immediate_concerns": ["list any urgent cardiac issues"],
                    "confidence_score": 0.0-1.0
                }}
                
                Medical Report: {medical_report}
            """,
            
            "Psychologist": """
                Act as an expert clinical psychologist. Analyze the patient's mental health status.
                
                Task: Evaluate psychological and psychiatric aspects of the patient's condition.
                
                Focus Areas:
                - Anxiety disorders and panic attacks
                - Depression and mood disorders
                - Stress-related conditions
                - Sleep disturbances
                - Cognitive function
                - Behavioral patterns
                
                Provide your assessment in this JSON format:
                {{
                    "findings": ["list of key psychological findings"],
                    "possible_conditions": ["list of potential mental health conditions"],
                    "severity": "low/moderate/high",
                    "recommended_interventions": ["therapy types, counseling approaches"],
                    "immediate_concerns": ["list any urgent mental health issues"],
                    "confidence_score": 0.0-1.0
                }}
                
                Patient Report: {medical_report}
            """,
            
            "Pulmonologist": """
                Act as an expert pulmonologist. Analyze the patient's respiratory system health.
                
                Task: Evaluate pulmonary function and respiratory symptoms.
                
                Focus Areas:
                - Breathing difficulties and dyspnea
                - Chronic respiratory conditions (COPD, asthma)
                - Lung infections and inflammation
                - Oxygen saturation levels
                - Pulmonary function test results
                
                Provide your assessment in this JSON format:
                {{
                    "findings": ["list of key respiratory findings"],
                    "possible_conditions": ["list of potential pulmonary conditions"],
                    "severity": "low/moderate/high",
                    "recommended_tests": ["pulmonary function tests, imaging"],
                    "immediate_concerns": ["list any urgent respiratory issues"],
                    "confidence_score": 0.0-1.0
                }}
                
                Patient Report: {medical_report}
            """,
            
            "Neurologist": """
                Act as an expert neurologist. Analyze the patient's neurological health.
                
                Task: Evaluate nervous system function and neurological symptoms.
                
                Focus Areas:
                - Cognitive function and memory
                - Headaches and migraines
                - Seizures or neurological episodes
                - Motor function and coordination
                - Sensory disturbances
                - Neurodegenerative conditions
                
                Provide your assessment in this JSON format:
                {{
                    "findings": ["list of key neurological findings"],
                    "possible_conditions": ["list of potential neurological conditions"],
                    "severity": "low/moderate/high",
                    "recommended_tests": ["MRI, EEG, neurological exams"],
                    "immediate_concerns": ["list any urgent neurological issues"],
                    "confidence_score": 0.0-1.0
                }}
                
                Patient Report: {medical_report}
            """,
            
            "Endocrinologist": """
                Act as an expert endocrinologist. Analyze the patient's hormonal and metabolic health.
                
                Task: Evaluate endocrine system function and metabolic conditions.
                
                Focus Areas:
                - Diabetes and blood sugar regulation
                - Thyroid function
                - Hormonal imbalances
                - Metabolic syndrome
                - Adrenal and pituitary function
                
                Provide your assessment in this JSON format:
                {{
                    "findings": ["list of key endocrine findings"],
                    "possible_conditions": ["list of potential endocrine conditions"],
                    "severity": "low/moderate/high",
                    "recommended_tests": ["hormone panels, glucose tests"],
                    "immediate_concerns": ["list any urgent endocrine issues"],
                    "confidence_score": 0.0-1.0
                }}
                
                Patient Report: {medical_report}
            """,
            
            "GeneralPractitioner": """
                Act as an experienced general practitioner. Provide a holistic overview of the patient's health.
                
                Task: Conduct comprehensive health assessment considering all body systems.
                
                Focus Areas:
                - Overall health status
                - Vital signs and general symptoms
                - Lifestyle factors
                - Preventive care needs
                - Coordination of specialist care
                
                Provide your assessment in this JSON format:
                {{
                    "findings": ["list of key general health findings"],
                    "possible_conditions": ["list of potential health conditions"],
                    "severity": "low/moderate/high",
                    "recommended_actions": ["general health recommendations"],
                    "immediate_concerns": ["list any urgent health issues"],
                    "confidence_score": 0.0-1.0
                }}
                
                Patient Report: {medical_report}
            """
        }
        
        template = templates.get(self.role, "")
        return PromptTemplate.from_template(template)
    
    def run(self):
        """Execute the agent analysis"""
        try:
            prompt = self.prompt_template.format(medical_report=self.medical_report)
            response = self.model.invoke(prompt)
            self.response = response.content
            
            # Try to parse JSON response
            try:
                parsed = json.loads(self.response)
                self.confidence_score = parsed.get('confidence_score', 0.5)
                return parsed
            except:
                # If not JSON, return as text
                return {"raw_response": self.response, "confidence_score": 0.5}
                
        except Exception as e:
            return {"error": str(e), "confidence_score": 0.0}


class DrugInteractionChecker(MedicalAgent):
    """Specialized agent for checking drug interactions"""
    
    def __init__(self, medications, model_name="llama-3.3-70b-versatile"):
        self.medications = medications
        super().__init__(role="DrugInteractionChecker", model_name=model_name)
        
    def create_prompt_template(self):
        return PromptTemplate.from_template("""
            Act as a clinical pharmacologist. Analyze potential drug interactions.
            
            Medications: {medications}
            
            Task: Identify potential drug-drug interactions, contraindications, and safety concerns.
            
            Provide your assessment in this JSON format:
            {{
                "interactions": [
                    {{
                        "drugs": ["drug1", "drug2"],
                        "severity": "minor/moderate/severe",
                        "description": "interaction description",
                        "recommendation": "what to do"
                    }}
                ],
                "warnings": ["list of important warnings"],
                "safe_combinations": ["list of safe drug combinations"],
                "monitoring_required": ["what to monitor"],
                "confidence_score": 0.0-1.0
            }}
        """)
    
    def run(self):
        try:
            prompt = self.prompt_template.format(medications=", ".join(self.medications))
            response = self.model.invoke(prompt)
            self.response = response.content
            
            try:
                return json.loads(self.response)
            except:
                return {"raw_response": self.response, "confidence_score": 0.5}
        except Exception as e:
            return {"error": str(e)}


class LabResultAnalyzer(MedicalAgent):
    """Specialized agent for analyzing laboratory results"""
    
    def __init__(self, lab_results, model_name="llama-3.3-70b-versatile"):
        self.lab_results = lab_results
        super().__init__(role="LabResultAnalyzer", model_name=model_name)
        
    def create_prompt_template(self):
        return PromptTemplate.from_template("""
            Act as a clinical pathologist. Analyze laboratory test results.
            
            Lab Results: {lab_results}
            
            Task: Interpret lab values, identify abnormalities, and suggest clinical significance.
            
            Provide your assessment in this JSON format:
            {{
                "abnormal_values": [
                    {{
                        "test": "test name",
                        "value": "actual value",
                        "normal_range": "normal range",
                        "significance": "clinical significance"
                    }}
                ],
                "patterns": ["identified patterns in results"],
                "possible_conditions": ["conditions suggested by lab results"],
                "follow_up_tests": ["recommended additional tests"],
                "urgency": "routine/urgent/critical",
                "confidence_score": 0.0-1.0
            }}
        """)
    
    def run(self):
        try:
            prompt = self.prompt_template.format(lab_results=self.lab_results)
            response = self.model.invoke(prompt)
            self.response = response.content
            
            try:
                return json.loads(self.response)
            except:
                return {"raw_response": self.response, "confidence_score": 0.5}
        except Exception as e:
            return {"error": str(e)}


class MultidisciplinaryTeam(MedicalAgent):
    """Synthesizes insights from multiple specialists"""
    
    def __init__(self, specialist_reports, model_name="llama-3.3-70b-versatile"):
        self.specialist_reports = specialist_reports
        super().__init__(role="MultidisciplinaryTeam", model_name=model_name)
        
    def create_prompt_template(self):
        return PromptTemplate.from_template("""
            Act as a multidisciplinary medical team coordinator. Synthesize specialist assessments.
            
            Specialist Reports:
            {specialist_reports}
            
            Task: Integrate all specialist findings into a comprehensive diagnosis and treatment plan.
            
            Provide your synthesis in this JSON format:
            {{
                "primary_diagnosis": "most likely diagnosis",
                "differential_diagnoses": ["alternative diagnoses"],
                "consensus_findings": ["findings agreed upon by multiple specialists"],
                "conflicting_opinions": ["areas where specialists disagree"],
                "integrated_treatment_plan": ["comprehensive treatment recommendations"],
                "priority_actions": ["immediate actions needed"],
                "follow_up_plan": ["long-term monitoring and care"],
                "overall_severity": "low/moderate/high/critical",
                "confidence_score": 0.0-1.0
            }}
        """)
    
    def run(self):
        try:
            reports_text = "\n\n".join([
                f"{role}:\n{json.dumps(report, indent=2)}" 
                for role, report in self.specialist_reports.items()
            ])
            
            prompt = self.prompt_template.format(specialist_reports=reports_text)
            response = self.model.invoke(prompt)
            self.response = response.content
            
            try:
                return json.loads(self.response)
            except:
                return {"raw_response": self.response, "confidence_score": 0.5}
        except Exception as e:
            return {"error": str(e)}


# Specialist class definitions
class Cardiologist(MedicalAgent):
    def __init__(self, medical_report, model_name="llama-3.3-70b-versatile"):
        super().__init__(medical_report, "Cardiologist", model_name=model_name)

class Psychologist(MedicalAgent):
    def __init__(self, medical_report, model_name="llama-3.3-70b-versatile"):
        super().__init__(medical_report, "Psychologist", model_name=model_name)

class Pulmonologist(MedicalAgent):
    def __init__(self, medical_report, model_name="llama-3.3-70b-versatile"):
        super().__init__(medical_report, "Pulmonologist", model_name=model_name)

class Neurologist(MedicalAgent):
    def __init__(self, medical_report, model_name="llama-3.3-70b-versatile"):
        super().__init__(medical_report, "Neurologist", model_name=model_name)

class Endocrinologist(MedicalAgent):
    def __init__(self, medical_report, model_name="llama-3.3-70b-versatile"):
        super().__init__(medical_report, "Endocrinologist", model_name=model_name)

class GeneralPractitioner(MedicalAgent):
    def __init__(self, medical_report, model_name="llama-3.3-70b-versatile"):
        super().__init__(medical_report, "GeneralPractitioner", model_name=model_name)
