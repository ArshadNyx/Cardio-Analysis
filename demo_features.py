"""
Demo script to showcase the enhanced features
Run this to test the system without the Streamlit UI
"""

from dotenv import load_dotenv
from Utils.EnhancedAgents import (
    Cardiologist, Psychologist, Pulmonologist,
    Neurologist, Endocrinologist, GeneralPractitioner,
    DrugInteractionChecker, LabResultAnalyzer, MultidisciplinaryTeam
)
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load API key
load_dotenv(dotenv_path='apikey.env')

def demo_specialist_analysis():
    """Demo: Multi-specialist analysis"""
    print("\n" + "="*60)
    print("🏥 DEMO: Multi-Specialist Analysis")
    print("="*60)
    
    # Sample medical report
    medical_report = """
    Patient: John Doe, 45 years old
    Chief Complaint: Chest pain and shortness of breath
    
    History: Patient reports intermittent chest pain for 2 weeks,
    associated with anxiety and difficulty breathing. Episodes last
    5-10 minutes. Also reports trouble sleeping and feeling stressed.
    
    Vitals: BP 140/90, HR 88, RR 18, Temp 98.6°F
    
    Physical Exam: Heart sounds normal, lungs clear, no edema
    
    ECG: Normal sinus rhythm
    Blood work: Slightly elevated glucose (110 mg/dL)
    """
    
    # Create specialists
    specialists = {
        "Cardiologist": Cardiologist(medical_report),
        "Psychologist": Psychologist(medical_report),
        "Pulmonologist": Pulmonologist(medical_report),
        "Neurologist": Neurologist(medical_report),
        "Endocrinologist": Endocrinologist(medical_report),
    }
    
    print("\n📋 Analyzing with 5 specialists concurrently...\n")
    
    # Run analysis concurrently
    results = {}
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(agent.run): name for name, agent in specialists.items()}
        
        for future in as_completed(futures):
            name = futures[future]
            print(f"✅ {name} completed")
            results[name] = future.result()
    
    print("\n" + "-"*60)
    print("📊 RESULTS SUMMARY")
    print("-"*60)
    
    for specialist, result in results.items():
        print(f"\n{specialist}:")
        if 'error' not in result:
            print(f"  Severity: {result.get('severity', 'N/A')}")
            print(f"  Confidence: {result.get('confidence_score', 0)*100:.0f}%")
            print(f"  Findings: {len(result.get('findings', []))} items")
        else:
            print(f"  Error: {result['error']}")
    
    return results

def demo_drug_checker():
    """Demo: Drug interaction checker"""
    print("\n" + "="*60)
    print("💊 DEMO: Drug Interaction Checker")
    print("="*60)
    
    medications = [
        "Aspirin 100mg",
        "Warfarin 5mg",
        "Ibuprofen 400mg"
    ]
    
    print(f"\n📋 Checking interactions for:")
    for med in medications:
        print(f"  - {med}")
    
    checker = DrugInteractionChecker(medications)
    result = checker.run()
    
    print("\n" + "-"*60)
    print("⚠️  INTERACTION ANALYSIS")
    print("-"*60)
    
    if 'interactions' in result:
        for interaction in result['interactions']:
            severity = interaction.get('severity', 'unknown')
            drugs = ' + '.join(interaction.get('drugs', []))
            print(f"\n{severity.upper()}: {drugs}")
            print(f"  {interaction.get('description', 'N/A')}")
    else:
        print("\nRaw result:")
        print(json.dumps(result, indent=2))
    
    return result

def demo_lab_analyzer():
    """Demo: Lab result analyzer"""
    print("\n" + "="*60)
    print("🧪 DEMO: Laboratory Result Analyzer")
    print("="*60)
    
    lab_results = """
    Complete Blood Count:
    - Hemoglobin: 11.5 g/dL (Low, normal: 13.5-17.5)
    - White Blood Cell Count: 12,000/μL (High, normal: 4,500-11,000)
    - Platelets: 250,000/μL (Normal)
    
    Metabolic Panel:
    - Glucose (fasting): 125 mg/dL (High, normal: 70-100)
    - Creatinine: 1.2 mg/dL (Normal)
    - ALT: 45 U/L (Slightly elevated, normal: 7-35)
    """
    
    print("\n📋 Analyzing lab results...\n")
    
    analyzer = LabResultAnalyzer(lab_results)
    result = analyzer.run()
    
    print("-"*60)
    print("🔬 ANALYSIS RESULTS")
    print("-"*60)
    
    if 'abnormal_values' in result:
        print(f"\n🔴 Abnormal Values Found: {len(result['abnormal_values'])}")
        for abnormal in result['abnormal_values']:
            print(f"\n  {abnormal.get('test', 'N/A')}")
            print(f"    Value: {abnormal.get('value', 'N/A')}")
            print(f"    Normal: {abnormal.get('normal_range', 'N/A')}")
        
        print(f"\n⚠️  Urgency Level: {result.get('urgency', 'N/A').upper()}")
    else:
        print("\nRaw result:")
        print(json.dumps(result, indent=2))
    
    return result

def demo_final_synthesis(specialist_results):
    """Demo: Multi-disciplinary team synthesis"""
    print("\n" + "="*60)
    print("🎯 DEMO: Final Diagnosis Synthesis")
    print("="*60)
    
    print("\n🔄 Synthesizing all specialist reports...\n")
    
    team = MultidisciplinaryTeam(specialist_results)
    result = team.run()
    
    print("-"*60)
    print("📋 INTEGRATED DIAGNOSIS")
    print("-"*60)
    
    if 'primary_diagnosis' in result:
        print(f"\n🎯 Primary Diagnosis:")
        print(f"  {result.get('primary_diagnosis', 'N/A')}")
        
        print(f"\n🔄 Differential Diagnoses:")
        for dx in result.get('differential_diagnoses', []):
            print(f"  - {dx}")
        
        print(f"\n💊 Treatment Plan:")
        for step in result.get('integrated_treatment_plan', [])[:3]:
            print(f"  - {step}")
        
        print(f"\n⚠️  Overall Severity: {result.get('overall_severity', 'N/A').upper()}")
        print(f"🎯 Confidence: {result.get('confidence_score', 0)*100:.0f}%")
    else:
        print("\nRaw result:")
        print(json.dumps(result, indent=2))
    
    return result

def main():
    """Run all demos"""
    print("\n" + "="*60)
    print("🏥 AI MEDICAL DIAGNOSTICS - FEATURE DEMO")
    print("="*60)
    print("\nThis demo showcases the enhanced features:")
    print("  1. Multi-specialist analysis (6 specialists)")
    print("  2. Drug interaction checker")
    print("  3. Lab result analyzer")
    print("  4. Final diagnosis synthesis")
    print("\n⚠️  Note: This may take 30-60 seconds to complete")
    print("="*60)
    
    try:
        # Run demos
        specialist_results = demo_specialist_analysis()
        demo_drug_checker()
        demo_lab_analyzer()
        demo_final_synthesis(specialist_results)
        
        print("\n" + "="*60)
        print("✅ DEMO COMPLETE!")
        print("="*60)
        print("\n🚀 To use the full Streamlit UI, run:")
        print("   streamlit run streamlit_app.py")
        print("\n📖 For detailed guide, see: STREAMLIT_GUIDE.md")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure:")
        print("  1. GROQ_API_KEY is set in apikey.env")
        print("  2. You have internet connection")
        print("  3. Dependencies are installed: pip install -r requirements.txt")

if __name__ == "__main__":
    main()
