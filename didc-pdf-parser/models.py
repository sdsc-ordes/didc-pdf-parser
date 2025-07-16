from pydantic import BaseModel, Field
from typing import List, Optional


class SectionData(BaseModel):
    analyte: str
    result: str
    unit: str
    reference: str
    comments: Optional[str] = None
    out_of_range: Optional[bool] = False

class Section(BaseModel):
    section_name: str
    data: List[SectionData]

class SimpleReport(BaseModel):
    report_id: str
    project: str
    patient_id: str
    gender: Optional[str] = None
    birth_year: Optional[str] = None
    daily_id: Optional[str]
    date: Optional[str] 
    time: Optional[str]
    sections: List[Section]

#####################################################################
# Explicit IKC Report Schema
#####################################################################

class Analyte(BaseModel):
    caption: str
    result: str
    unit: str
    reference: str
    comments: Optional[str] = None
    out_of_range: Optional[bool] = False

class ElectrolyteAndWaterBalance(BaseModel):
    caption: str = "Elektrolyt- und Wasserhaushalt"
    sodium: Analyte = Field(..., description="Sodium")
    potassium: Analyte = Field(..., description="Potassium")
    total_calcium: Analyte = Field(..., description="Total Calcium")
    albumin_corrected_calcium: Analyte = Field(..., description="Albumin-Corrected Calcium")
    phosphate: Analyte = Field(..., description="Phosphate")

class Kidney(BaseModel):
    caption: str = "Niere"
    urea: Analyte = Field(..., description="Urea")
    creatinine: Analyte = Field(..., description="Creatinine")
    egfr_crea_ckd_epi_2009: Analyte = Field(..., description="eGFR (CKD-EPI 2009)")
    uric_acid: Analyte = Field(..., description="Uric Acid")

class AminoAcidBilirubinAndHemeMetabolism(BaseModel):
    caption: str = "Aminosäure-,Bili.-und Hämstoffwechsel"
    bilirubin_total: Analyte = Field(..., description="Bilirubin, total")

class Proteins(BaseModel):
    caption: str = "Proteine"
    protein: Analyte = Field(..., description="Protein")
    albumin: Analyte = Field(..., description="Albumin")

class Enzymes(BaseModel):
    caption: str = "Enzyme"
    ast_got: Analyte = Field(..., description="AST (GOT) Aspartate Aminotransferase")
    ggt: Analyte = Field(..., description="GGT (Gamma-Glutamyltransferase)")
    alkaline_phosphatase: Analyte = Field(..., description="Alkaline Phosphatase")

class Inflammation(BaseModel):
    caption: str = "Entzündung"
    crp: Analyte = Field(..., description="CRP (C-Reactive Protein)")

class HeartAndMuscle(BaseModel):
    caption: str = "Herz und Muskel"
    ck_total: Analyte = Field(..., description="CK, total")
    troponin_t_hs: Analyte = Field(..., description="Troponin T, High Sensitive")
    nt_pro_bnp: Analyte = Field(..., description="NT-proBNP (Roche)")

class DiabetesAndEnergyMetabolism(BaseModel):
    caption: str = "Diabetes und Energiestoffwechsel"
    glucose_hep_plasma: Analyte = Field(..., description="Glucose, Hepatic Plasma")
    hba1c_ngsp: Analyte = Field(..., description="HbA1c (NGSP)")
    hba1c_ifcc: Analyte = Field(..., description="HbA1c (IFCC)")

class LipidAndArteriosclerosis(BaseModel):
    caption: str = "Lipidstoffwechsel und Arteriosklerose"
    total_cholesterol: Analyte = Field(..., description="Total Cholesterol")
    hdl_cholesterol: Analyte = Field(..., description="HDL-Cholesterol")
    non_hdl_cholesterol: Analyte = Field(..., description="non-HDL Cholesterol")
    ldl_cholesterol_sampson: Analyte = Field(..., description="LDL-Cholesterol (Sampson)")
    triglycerides: Analyte = Field(..., description="Triglycerides")
    lipoprotein_a: Analyte = Field(..., description="Lipoprotein (a) (Roche)")
    apolipoprotein_a1: Analyte = Field(..., description="Apolipoprotein A1")
    apolipoprotein_b: Analyte = Field(..., description="Apolipoprotein B")

class IronMetabolism(BaseModel):
    caption: str = "Eisenstoffwechsel"
    iron: Analyte = Field(..., description="Iron")
    ferritin_eclia: Analyte = Field(..., description="Ferritin (ECLIA)")
    ferritin_risk_eclia: Analyte = Field(..., description="Ferritin (Risk) (ECLIA)")
    transferrin: Analyte = Field(..., description="Transferrin")

class Vitamins(BaseModel):
    caption: str = "Vitamine"
    folic_acid: Analyte = Field(..., description="Folic Acid")
    vitamin_b12: Analyte = Field(..., description="Vitamin B12")
    hydroxyvitamin_d: Analyte = Field(..., description="25-Hydroxy-Vitamin D (Roche)")

class ThyroidFunction(BaseModel):
    caption: str = "Schilddrüsenfunktion"
    tsh_basal_ft4: Analyte = Field(..., description="TSH, basal FT4 (free)")
    ft3_free: Analyte = Field(..., description="FT3 (free)")
    ft4_free: Analyte = Field(..., description="FT4 (free)")

class SexualHormones(BaseModel):
    caption: str = "Sexualhormone"

    # Common for all
    testosterone: Analyte = Field(..., description="Testosterone")
    estradiol: Analyte = Field(..., description="Estradiol")

    # Female-specific hormones (optional)
    lh: Optional[Analyte] = Field(None, description="LH")
    fsh: Optional[Analyte] = Field(None, description="FSH")
    progesterone: Optional[Analyte] = Field(None, description="Progesterone")

class IKCLabResult(BaseModel):
    electrolyte_and_water_balance: ElectrolyteAndWaterBalance = Field(..., description="Elektrolyt- und Wasserhaushalt")
    kidney: Kidney = Field(..., description="Niere")
    amino_acid_bilirubin_and_heme_metabolism: AminoAcidBilirubinAndHemeMetabolism = Field(..., description="Aminosäure-,Bili.-und Hämstoffwechsel")
    proteins: Proteins = Field(..., description="Proteine")
    enzymes: Enzymes = Field(..., description="Enzyme")
    inflammation: Inflammation = Field(..., description="Entzündung")
    heart_and_muscle: HeartAndMuscle = Field(..., description="Herz und Muskel")
    diabetes_and_energy_metabolism: DiabetesAndEnergyMetabolism = Field(..., description="Diabetes und Energiestoffwechsel Glucose,Hep.Plasma")
    lipid_and_arteriosclerosis: LipidAndArteriosclerosis = Field(..., description="Lipidstoffwechsel und Arteriosklerose")
    iron_metabolism: IronMetabolism = Field(..., description="Eisenstoffwechsel")
    vitamins: Vitamins = Field(..., description="Vitamine")
    thyroid_function: ThyroidFunction = Field(..., description="Schilddrüse")
    sexual_hormones: SexualHormones = Field(..., description="Sexualhormone")

class ExplicitIKCReport(BaseModel):
    report_id: str
    project: str
    patient_id: str
    gender: Optional[str] = None
    birth_year: Optional[str] = None
    daily_id: Optional[str]
    date: Optional[str] 
    time: Optional[str]
    lab_result: IKCLabResult

#####################################################################
# Explicit AKH Report Schema
#####################################################################

class BloodStatus(BaseModel):
    caption: str = "Blutstatus"
    hemoglobin: Analyte = Field(..., description="Hämoglobin")
    hematocrit: Analyte = Field(..., description="Hämatokrit")
    erythrocytes: Analyte = Field(..., description="Erythrozyten")
    mcv: Analyte = Field(..., description="MCV")
    mch: Analyte = Field(..., description="MCH")
    mchc: Analyte = Field(..., description="MCHC")
    rdw: Analyte = Field(..., description="RDW")
    platelets: Analyte = Field(..., description="Thrombozyten")
    leukocytes: Analyte = Field(..., description="Leukozyten")

class BloodCountAbsolute(BaseModel):
    caption: str = "Blutbild automatisch absolut"
    neutrophils: Analyte = Field(..., description="Neutrophile")
    monocytes: Analyte = Field(..., description="Monozyten")
    eosinophils: Analyte = Field(..., description="Eosinophile")
    basophils: Analyte = Field(..., description="Basophile")
    lymphocytes: Analyte = Field(..., description="Lymphozyten")
    immature_granulocytes: Analyte = Field(..., description="Immature Granulocytes")
    nrbc_abs: Analyte = Field(..., description="NRBC abs.")

class BloodCountRelative(BaseModel):
    caption: str = "Blutbild automatisch relativ"
    neutrophils: Analyte = Field(..., description="Neutrophile")
    monocytes: Analyte = Field(..., description="Monozyten")
    eosinophils: Analyte = Field(..., description="Eosinophile")
    basophils: Analyte = Field(..., description="Basophile")
    lymphocytes: Analyte = Field(..., description="Lymphozyten")
    immature_granulocytes: Analyte = Field(..., description="Immature Granulocytes")
    nrbc: Analyte = Field(..., description="NRBC")

class HematologicalExaminations(BaseModel):
    caption: str = "Hämatologische Untersuchungen"
    blood_status: BloodStatus = Field(..., description="Blutstatus")
    blood_count_absolute: BloodCountAbsolute = Field(..., description="Blutbild automatisch absolut")
    blood_count_relative: BloodCountRelative = Field(..., description="Blutbild automatisch relativ")

class CoagulationFactors(BaseModel):
    caption: str = "Gerinnungsfaktoren"
    fibrinogen: Analyte = Field(..., description="Fibrinogen (fkt.)")

class HemostasisExaminations(BaseModel):
    caption: str = "Hämostase Untersuchungen"
    coagulation_factors: CoagulationFactors = Field(..., description="Gerinnungsfaktoren")

class AKHLabResult(BaseModel):
    hematological_examinations: HematologicalExaminations = Field(..., description="Hämatologische Untersuchungen")
    hemostasis_examinations: HemostasisExaminations = Field(..., description="Hämostase Untersuchungen")
    
class ExplicitAKHReport(BaseModel):
    report_id: str
    project: str
    patient_id: str
    gender: Optional[str] = None
    birth_year: Optional[str] = None
    daily_id: Optional[str]
    date: Optional[str] 
    time: Optional[str]
    lab_result: AKHLabResult