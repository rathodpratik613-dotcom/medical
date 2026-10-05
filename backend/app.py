from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import sqlite3
import datetime
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Database file path
DB_PATH = os.path.join(os.path.dirname(__file__), 'database', 'telemedicine.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with schema and sample data"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            address TEXT,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            specialization TEXT NOT NULL,
            experience_years INTEGER,
            available BOOLEAN DEFAULT 1,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pharmacies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            operating_hours TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pharmacy_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            available BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (pharmacy_id) REFERENCES pharmacies(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            symptoms TEXT NOT NULL,
            diagnosis TEXT,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER NOT NULL,
            medicines TEXT NOT NULL,
            instructions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS followups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            consultation_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            scheduled_date DATE NOT NULL,
            notes TEXT,
            status TEXT DEFAULT 'scheduled',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (consultation_id) REFERENCES consultations(id) ON DELETE CASCADE,
            FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
            FOREIGN KEY (doctor_id) REFERENCES doctors(id) ON DELETE CASCADE
        )
    ''')
    
    # Check if data already exists
    cursor.execute('SELECT COUNT(*) FROM doctors')
    if cursor.fetchone()[0] == 0:
        # Insert sample doctors
        doctors_data = [
            ('Dr. Rajesh Kumar', 'rajesh.kumar@email.com', '+919876543210', 'General Physician', 25, 1, 'doctor123'),
            ('Dr. Maria Garcia', 'maria.garcia@email.com', '+1234567890', 'Cardiologist', 18, 1, 'doctor123'),
            ('Dr. James Wilson', 'james.wilson@email.com', '+1234567891', 'Neurologist', 22, 1, 'doctor123'),
            ('Dr. Sarah Ahmed', 'sarah.ahmed@email.com', '+1234567892', 'Pediatrician', 15, 1, 'doctor123'),
            ('Dr. David Lee', 'david.lee@email.com', '+1234567893', 'Dermatologist', 20, 1, 'doctor123'),
            ('Dr. Emily Chen', 'emily.chen@email.com', '+1234567894', 'Orthopedic Surgeon', 17, 1, 'doctor123'),
            ('Dr. Michael Brown', 'michael.brown@email.com', '+1234567895', 'Gynecologist', 19, 1, 'doctor123'),
            ('Dr. Lisa Patel', 'lisa.patel@email.com', '+1234567896', 'Ophthalmologist', 14, 1, 'doctor123'),
            ('Dr. Robert Taylor', 'robert.taylor@email.com', '+1234567897', 'ENT Specialist', 21, 1, 'doctor123'),
            ('Dr. Jennifer White', 'jennifer.white@email.com', '+1234567898', 'Psychiatrist', 16, 1, 'doctor123'),
            ('Dr. William Johnson', 'william.johnson@email.com', '+1234567899', 'Gastroenterologist', 23, 1, 'doctor123'),
            ('Dr. Amanda Martinez', 'amanda.martinez@email.com', '+1234567900', 'Nephrologist', 12, 1, 'doctor123'),
            ('Dr. Christopher Davis', 'christopher.davis@email.com', '+1234567901', 'Pulmonologist', 20, 1, 'doctor123'),
            ('Dr. Jessica Rodriguez', 'jessica.rodriguez@email.com', '+1234567902', 'Endocrinologist', 18, 1, 'doctor123'),
            ('Dr. Daniel Anderson', 'daniel.anderson@email.com', '+1234567903', 'Rheumatologist', 15, 1, 'doctor123'),
            ('Dr. Michelle Thomas', 'michelle.thomas@email.com', '+1234567904', 'Oncologist', 24, 1, 'doctor123'),
            ('Dr. Matthew Jackson', 'matthew.jackson@email.com', '+1234567905', 'Hematologist', 19, 1, 'doctor123'),
            ('Dr. Laura Harris', 'laura.harris@email.com', '+1234567906', 'Infectious Disease Specialist', 17, 1, 'doctor123'),
            ('Dr. Kevin Clark', 'kevin.clark@email.com', '+1234567907', 'Urologist', 21, 1, 'doctor123'),
            ('Dr. Nicole Lewis', 'nicole.lewis@email.com', '+1234567908', 'Plastic Surgeon', 16, 1, 'doctor123'),
            ('Dr. Brian Walker', 'brian.walker@email.com', '+1234567909', 'Neurosurgeon', 26, 1, 'doctor123'),
            ('Dr. Stephanie Hall', 'stephanie.hall@email.com', '+1234567910', 'Cardiothoracic Surgeon', 22, 1, 'doctor123'),
            ('Dr. Joshua Young', 'joshua.young@email.com', '+1234567911', 'Vascular Surgeon', 18, 1, 'doctor123'),
            ('Dr. Melissa King', 'melissa.king@email.com', '+1234567912', 'Pediatric Surgeon', 14, 1, 'doctor123'),
            ('Dr. Andrew Wright', 'andrew.wright@email.com', '+1234567913', 'Geriatrician', 20, 1, 'doctor123'),
            ('Dr. Rebecca Scott', 'rebecca.scott@email.com', '+1234567914', 'Sports Medicine Specialist', 13, 1, 'doctor123'),
            ('Dr. Eric Green', 'eric.green@email.com', '+1234567915', 'Pain Management Specialist', 19, 1, 'doctor123'),
            ('Dr. Kimberly Adams', 'kimberly.adams@email.com', '+1234567916', 'Sleep Medicine Specialist', 11, 1, 'doctor123'),
            ('Dr. Ryan Baker', 'ryan.baker@email.com', '+1234567917', 'Allergist', 17, 1, 'doctor123'),
            ('Dr. Elizabeth Nelson', 'elizabeth.nelson@email.com', '+1234567918', 'Immunologist', 23, 1, 'doctor123'),
            ('Dr. Justin Hill', 'justin.hill@email.com', '+1234567919', 'Clinical Geneticist', 15, 1, 'doctor123'),
            ('Dr. Samantha Moore', 'samantha.moore@email.com', '+1234567920', 'Perinatologist', 18, 1, 'doctor123'),
            ('Dr. Brandon Taylor', 'brandon.taylor@email.com', '+1234567921', 'Neonatologist', 16, 1, 'doctor123'),
            ('Dr. Katherine Anderson', 'katherine.anderson@email.com', '+1234567922', 'Physical Medicine', 20, 1, 'doctor123'),
            ('Dr. Gregory Thomas', 'gregory.thomas@email.com', '+1234567923', 'Radiologist', 25, 1, 'doctor123'),
            ('Dr. Victoria Jackson', 'victoria.jackson@email.com', '+1234567924', 'Pathologist', 22, 1, 'doctor123'),
            ('Dr. Nathan White', 'nathan.white@email.com', '+1234567925', 'Anesthesiologist', 19, 1, 'doctor123'),
            ('Dr. Christina Harris', 'christina.harris@email.com', '+1234567926', 'Emergency Medicine', 14, 1, 'doctor123'),
            ('Dr. Dylan Martin', 'dylan.martin@email.com', '+1234567927', 'Critical Care Specialist', 21, 1, 'doctor123'),
            ('Dr. Ashley Thompson', 'ashley.thompson@email.com', '+1234567928', 'Addiction Medicine', 12, 1, 'doctor123'),
            ('Dr. Jose Garcia', 'jose.garcia@email.com', '+1234567929', 'Occupational Medicine', 18, 1, 'doctor123'),
            ('Dr. Brianna Martinez', 'brianna.martinez@email.com', '+1234567930', 'Preventive Medicine', 16, 1, 'doctor123'),
            ('Dr. Kyle Robinson', 'kyle.robinson@email.com', '+1234567931', 'Public Health', 23, 1, 'doctor123'),
            ('Dr. Danielle Clark', 'danielle.clark@email.com', '+1234567932', 'Tropical Medicine', 15, 1, 'doctor123'),
            ('Dr. Lucas Rodriguez', 'lucas.rodriguez@email.com', '+1234567933', 'Travel Medicine', 17, 1, 'doctor123'),
            ('Dr. Hannah Lewis', 'hannah.lewis@email.com', '+1234567934', 'Aviation Medicine', 20, 1, 'doctor123'),
            ('Dr. Noah Walker', 'noah.walker@email.com', '+1234567935', 'Undersea Medicine', 14, 1, 'doctor123'),
            ('Dr. Alexis Hall', 'alexis.hall@email.com', '+1234567936', 'Forensic Pathologist', 22, 1, 'doctor123'),
            ('Dr. Isaac Young', 'isaac.young@email.com', '+1234567937', 'Medical Toxicologist', 19, 1, 'doctor123'),
            ('Dr. Julia King', 'julia.king@email.com', '+1234567938', 'Hyperbaric Medicine', 16, 1, 'doctor123'),
            ('Dr. Gabriel Wright', 'gabriel.wright@email.com', '+1234567939', 'Palliative Care', 24, 1, 'doctor123'),
            ('Dr. Morgan Scott', 'morgan.scott@email.com', '+1234567940', 'Rehabilitation Medicine', 18, 1, 'doctor123'),
            ('Dr. Isaiah Green', 'isaiah.green@email.com', '+1234567941', 'Transplant Surgeon', 26, 1, 'doctor123'),
            ('Dr. Sophia Adams', 'sophia.adams@email.com', '+1234567942', 'Hepatologist', 21, 1, 'doctor123'),
            ('Dr. Aaron Baker', 'aaron.baker@email.com', '+1234567943', 'Colorectal Surgeon', 19, 1, 'doctor123'),
            ('Dr. Madison Nelson', 'madison.nelson@email.com', '+1234567944', 'Breast Surgeon', 17, 1, 'doctor123'),
            ('Dr. Cameron Hill', 'cameron.hill@email.com', '+1234567945', 'Thoracic Surgeon', 23, 1, 'doctor123'),
            ('Dr. Aubrey Moore', 'aubrey.moore@email.com', '+1234567946', 'Hand Surgeon', 15, 1, 'doctor123'),
            ('Dr. Tyler Taylor', 'tylor.taylor@email.com', '+1234567947', 'Foot and Ankle Surgeon', 20, 1, 'doctor123'),
            ('Dr. Jordan Anderson', 'jordan.anderson@email.com', '+1234567948', 'Spine Surgeon', 22, 1, 'doctor123'),
            ('Dr. Taylor Thomas', 'taylor.thomas@email.com', '+1234567949', 'Joint Replacement Surgeon', 25, 1, 'doctor123'),
            ('Dr. Riley Jackson', 'riley.jackson@email.com', '+1234567950', 'Trauma Surgeon', 18, 1, 'doctor123'),
            ('Dr. Blake White', 'blake.white@email.com', '+1234567951', 'Burn Specialist', 16, 1, 'doctor123'),
            ('Dr. Avery Harris', 'avery.harris@email.com', '+1234567952', 'Craniofacial Surgeon', 21, 1, 'doctor123'),
            ('Dr. Peyton Martin', 'peyton.martin@email.com', '+1234567953', 'Oral and Maxillofacial Surgeon', 19, 1, 'doctor123'),
            ('Dr. Hayden Thompson', 'hayden.thompson@email.com', '+1234567954', 'Proctologist', 17, 1, 'doctor123'),
            ('Dr. Brooklyn Garcia', 'brooklyn.garcia@email.com', '+1234567955', 'Bariatric Surgeon', 20, 1, 'doctor123'),
            ('Dr. Alexa Martinez', 'alexa.martinez@email.com', '+1234567956', 'Minimally Invasive Surgeon', 15, 1, 'doctor123'),
            ('Dr. Carson Robinson', 'carson.robinson@email.com', '+1234567957', 'Robotic Surgeon', 18, 1, 'doctor123'),
            ('Dr. Preston Clark', 'preston.clark@email.com', '+1234567958', 'Laparoscopic Surgeon', 22, 1, 'doctor123'),
            ('Dr. Kendall Rodriguez', 'kendall.rodriguez@email.com', '+1234567959', 'Endocrine Surgeon', 16, 1, 'doctor123'),
            ('Dr. Audrey Lewis', 'audrey.lewis@email.com', '+1234567960', 'Head and Neck Surgeon', 24, 1, 'doctor123'),
            ('Dr. Sergio Ramirez', 'sergio.ramirez@email.com', '+1234567961', 'Cardiac Electrophysiologist', 21, 1, 'doctor123'),
            ('Dr. Valentina Flores', 'valentina.flores@email.com', '+1234567962', 'Interventional Cardiologist', 19, 1, 'doctor123'),
            ('Dr. Mateo Cruz', 'mateo.cruz@email.com', '+1234567963', 'Heart Failure Specialist', 23, 1, 'doctor123'),
            ('Dr. Isabella Morales', 'isabella.morales@email.com', '+1234567964', 'Structural Heart Disease', 17, 1, 'doctor123'),
            ('Dr. Leonardo Reyes', 'leonardo.reyes@email.com', '+1234567965', 'Preventive Cardiologist', 20, 1, 'doctor123'),
            ('Dr. Camila Ortiz', 'camila.ortiz@email.com', '+1234567966', 'Women Heart Specialist', 15, 1, 'doctor123'),
            ('Dr. Diego Gutierrez', 'diego.gutierrez@email.com', '+1234567967', 'Sports Cardiologist', 18, 1, 'doctor123'),
            ('Dr. Sofia Torres', 'sofia.torres@email.com', '+1234567968', 'Nuclear Cardiologist', 22, 1, 'doctor123'),
            ('Dr. Alejandro Ruiz', 'alejandro.ruiz@email.com', '+1234567969', 'Congenital Heart Disease', 25, 1, 'doctor123'),
            ('Dr. Valeria Vargas', 'valeria.vargas@email.com', '+1234567970', 'Pediatric Cardiologist', 14, 1, 'doctor123'),
            ('Dr. Sebastian Castillo', 'sebastian.castillo@email.com', '+1234567971', 'Epileptologist', 19, 1, 'doctor123'),
            ('Dr. Gabriela Mendez', 'gabriela.mendez@email.com', '+1234567972', 'Stroke Specialist', 21, 1, 'doctor123'),
            ('Dr. Emiliano Herrera', 'emiliano.herrera@email.com', '+1234567973', 'Movement Disorder Specialist', 17, 1, 'doctor123'),
            ('Dr. Renata Luna', 'renata.luna@email.com', '+1234567974', 'Multiple Sclerosis Specialist', 23, 1, 'doctor123'),
            ('Dr. Andrés Rios', 'andres.rios@email.com', '+1234567975', 'Memory Disorder Specialist', 20, 1, 'doctor123'),
            ('Dr. Carolina Soto', 'carolina.soto@email.com', '+1234567976', 'Neuromuscular Specialist', 16, 1, 'doctor123'),
            ('Dr. Ricardo Mendoza', 'ricardo.mendoza@email.com', '+1234567977', 'Headache Specialist', 18, 1, 'doctor123'),
            ('Dr. Fernanda Castro', 'fernanda.castro@email.com', '+1234567978', 'Brain Injury Specialist', 22, 1, 'doctor123'),
            ('Dr. Omar Aguilar', 'omar.aguilar@email.com', '+1234567979', 'Sleep Neurologist', 15, 1, 'doctor123'),
            ('Dr. Mariana Ortiz', 'mariana.ortiz@email.com', '+1234567980', 'Autism Specialist', 19, 1, 'doctor123'),
            ('Dr. Julián Delgado', 'julian.delgado@email.com', '+1234567981', 'ADHD Specialist', 17, 1, 'doctor123'),
            ('Dr. Victoria León', 'victoria.leon@email.com', '+1234567982', 'Developmental Pediatrician', 21, 1, 'doctor123'),
            ('Dr. Alejandro Vega', 'alejandro.vega@email.com', '+1234567983', 'Pediatric Pulmonologist', 14, 1, 'doctor123'),
            ('Dr. Daniela Paredes', 'daniela.paredes@email.com', '+1234567984', 'Pediatric Gastroenterologist', 20, 1, 'doctor123'),
            ('Dr. Maximiliano Espinoza', 'maximiliano.espinoza@email.com', '+1234567985', 'Pediatric Nephrologist', 23, 1, 'doctor123'),
            ('Dr. Camila Benítez', 'camila.benitez@email.com', '+1234567986', 'Pediatric Endocrinologist', 16, 1, 'doctor123'),
            ('Dr. Sebastián Medina', 'sebastian.medina@email.com', '+1234567987', 'Pediatric Hematologist', 18, 1, 'doctor123'),
            ('Dr. Valentina Clemente', 'valentina.clemente@email.com', '+1234567988', 'Pediatric Oncologist', 25, 1, 'doctor123'),
            ('Dr. Nicolás Guerrero', 'nicolas.guerrero@email.com', '+1234567989', 'Pediatric Rheumatologist', 15, 1, 'doctor123'),
        ]
        cursor.executemany('INSERT INTO doctors (name, email, phone, specialization, experience_years, available, password) VALUES (?, ?, ?, ?, ?, ?, ?)', doctors_data)
        
        # Insert pharmacies
        pharmacies_data = [
            ('HealthPlus Pharmacy', '123 Main Street, City Center', '+1234567894', 'healthplus@email.com', '9:00 AM - 9:00 PM'),
            ('MediCare Store', '456 Oak Avenue, West Side', '+1234567895', 'medicare@email.com', '8:00 AM - 10:00 PM'),
            ('QuickMeds', '789 Pine Road, East District', '+1234567896', 'quickmeds@email.com', '24/7'),
            ('PharmaWell', '321 Elm Street, North Side', '+1234567897', 'pharmawell@email.com', '10:00 AM - 8:00 PM'),
            ('City Drugs', '654 Maple Drive, South Side', '+1234567898', 'citydrugs@email.com', '8:00 AM - 9:00 PM'),
        ]
        cursor.executemany('INSERT INTO pharmacies (name, address, phone, email, operating_hours) VALUES (?, ?, ?, ?, ?)', pharmacies_data)
        
        # Insert medicines (sample of 30 including Indian medicines)
        medicines_data = [
            (1, 'Paracetamol 500mg', 'Pain reliever and fever reducer', 5.99, 150, 1),
            (1, 'Ibuprofen 400mg', 'Anti-inflammatory pain reliever', 7.99, 120, 1),
            (1, 'Aspirin 100mg', 'Blood thinner and pain reliever', 4.99, 200, 1),
            (1, 'Amoxicillin 500mg', 'Antibiotic for bacterial infections', 12.99, 80, 1),
            (1, 'Azithromycin 500mg', 'Antibiotic for respiratory infections', 15.99, 60, 1),
            (1, 'Omeprazole 20mg', 'Proton pump inhibitor for acid reflux', 8.99, 130, 1),
            (1, 'Metformin 500mg', 'Type 2 diabetes medication', 15.99, 140, 1),
            (1, 'Lisinopril 10mg', 'ACE inhibitor for blood pressure', 7.99, 160, 1),
            (1, 'Amlodipine 5mg', 'Calcium channel blocker for blood pressure', 9.99, 145, 1),
            (1, 'Losartan 50mg', 'ARB for blood pressure', 11.99, 125, 1),
            (2, 'Simvastatin 20mg', 'Statin for cholesterol', 13.99, 110, 1),
            (2, 'Atorvastatin 10mg', 'Statin for cholesterol', 16.99, 95, 1),
            (2, 'Clopidogrel 75mg', 'Antiplatelet for heart protection', 18.99, 120, 1),
            (2, 'Albuterol Inhaler', 'Bronchodilator for asthma', 25.99, 80, 1),
            (2, 'Fluticasone Inhaler', 'Inhaled corticosteroid for asthma', 32.99, 65, 1),
            (3, 'Cetirizine 10mg', 'Antihistamine for allergies', 6.99, 150, 1),
            (3, 'Loratadine 10mg', 'Antihistamine for allergies', 7.99, 140, 1),
            (3, 'Fexofenadine 180mg', 'Antihistamine for allergies', 11.99, 120, 1),
            (3, 'Prednisone 5mg', 'Oral corticosteroid', 8.99, 110, 1),
            (3, 'Levothyroxine 50mcg', 'Thyroid hormone replacement', 12.99, 140, 1),
            (4, 'Gabapentin 300mg', 'Anticonvulsant for nerve pain', 19.99, 95, 1),
            (4, 'Sertraline 50mg', 'SSRI for depression and anxiety', 16.99, 120, 1),
            (4, 'Fluoxetine 20mg', 'SSRI for depression and anxiety', 14.99, 135, 1),
            (4, 'Zolpidem 10mg', 'Sedative for insomnia', 19.99, 95, 1),
            (4, 'Methylphenidate 10mg', 'Stimulant for ADHD', 22.99, 80, 1),
            (5, 'Donepezil 5mg', 'Cholinesterase inhibitor for Alzheimer', 24.99, 60, 1),
            (5, 'Tadalafil 5mg', 'PDE5 inhibitor for erectile dysfunction', 35.99, 75, 1),
            (5, 'Orlistat 120mg', 'Lipase inhibitor for weight loss', 45.99, 80, 1),
            (5, 'Isotretinoin 20mg', 'Retinoid for severe acne', 45.99, 55, 1),
            (5, 'Tretinoin 0.025% Cream', 'Retinoid for acne and anti-aging', 28.99, 85, 1),
            # Indian Medicines
            (1, 'Dolo 650', 'Paracetamol 650mg - Pain and fever relief (Indian brand)', 2.99, 200, 1),
            (1, 'Crocin 500mg', 'Paracetamol - Pain reliever (Indian brand)', 3.49, 180, 1),
            (1, 'Combiflam', 'Ibuprofen + Paracetamol - Pain relief (Indian brand)', 4.99, 150, 1),
            (1, 'Volini Gel', 'Diclofenac gel - Pain relief (Indian brand)', 6.99, 120, 1),
            (2, 'Augmentin 625', 'Amoxicillin + Clavulanic acid - Antibiotic (Indian brand)', 14.99, 90, 1),
            (2, 'Azee 500', 'Azithromycin 500mg - Antibiotic (Indian brand)', 18.99, 70, 1),
            (2, 'Cifran 500', 'Ciprofloxacin 500mg - Antibiotic (Indian brand)', 15.99, 85, 1),
            (2, 'Omee 20', 'Omeprazole 20mg - Acid reflux (Indian brand)', 7.99, 140, 1),
            (2, 'Pantocid 40', 'Pantoprazole 40mg - Acid reflux (Indian brand)', 10.99, 110, 1),
            (3, 'Glycomet 500', 'Metformin 500mg - Diabetes (Indian brand)', 12.99, 160, 1),
            (3, 'Glycomet GP1', 'Metformin + Glimepiride - Diabetes (Indian brand)', 18.99, 90, 1),
            (3, 'Janumet 50/500', 'Sitagliptin + Metformin - Diabetes (Indian brand)', 24.99, 75, 1),
            (3, 'Telma 40', 'Telmisartan 40mg - Blood pressure (Indian brand)', 13.99, 130, 1),
            (3, 'Amlong 5', 'Amlodipine 5mg - Blood pressure (Indian brand)', 11.99, 145, 1),
            (4, 'Atorva 10', 'Atorvastatin 10mg - Cholesterol (Indian brand)', 17.99, 100, 1),
            (4, 'Roseday 10', 'Rosuvastatin 10mg - Cholesterol (Indian brand)', 22.99, 85, 1),
            (4, 'Ecosprin 75', 'Aspirin 75mg - Heart protection (Indian brand)', 4.49, 180, 1),
            (4, 'Clopitab 75', 'Clopidogrel 75mg - Heart protection (Indian brand)', 16.99, 110, 1),
            (5, 'Foracort 200', 'Budesonide + Formoterol - Asthma (Indian brand)', 28.99, 80, 1),
            (5, 'Seroflo 250', 'Fluticasone + Salmeterol - Asthma (Indian brand)', 32.99, 70, 1),
            (5, 'Allegra 120', 'Fexofenadine 120mg - Allergy (Indian brand)', 12.99, 130, 1),
            (5, 'Cetcip 10', 'Cetirizine 10mg - Allergy (Indian brand)', 7.49, 160, 1),
            (1, 'Thyronorm 50mcg', 'Levothyroxine 50mcg - Thyroid (Indian brand)', 11.99, 150, 1),
            (1, 'Eltroxin 50mcg', 'Levothyroxine 50mcg - Thyroid (Indian brand)', 13.99, 120, 1),
            (2, 'Neuropill 300', 'Gabapentin 300mg - Nerve pain (Indian brand)', 18.99, 100, 1),
            (2, 'Gabanext 300', 'Gabapentin 300mg - Nerve pain (Indian brand)', 19.99, 95, 1),
            (3, 'Zolfresh 10', 'Zolpidem 10mg - Insomnia (Indian brand)', 18.99, 110, 1),
            (3, 'Nitrest 10', 'Zolpidem 10mg - Insomnia (Indian brand)', 17.99, 105, 1),
            (4, 'Serta 50', 'Sertraline 50mg - Depression (Indian brand)', 15.99, 125, 1),
            (4, 'Depsert 50', 'Sertraline 50mg - Depression (Indian brand)', 16.99, 115, 1),
            (5, 'Nise 100', 'Nimesulide 100mg - Pain relief (Indian brand)', 5.99, 140, 1),
            (5, 'Sumo 100', 'Nimesulide 100mg - Pain relief (Indian brand)', 6.49, 135, 1),
            # More Indian Medicines
            (1, 'Calpol 500', 'Paracetamol 500mg - Pain relief (Indian brand)', 2.49, 200, 1),
            (1, 'Crocin Advance', 'Paracetamol 650mg - Pain relief (Indian brand)', 3.99, 180, 1),
            (1, 'Motin 400', 'Ibuprofen 400mg - Pain relief (Indian brand)', 4.49, 160, 1),
            (1, 'Brufen 400', 'Ibuprofen 400mg - Pain relief (Indian brand)', 4.99, 150, 1),
            (1, 'Disprin', 'Aspirin - Pain relief (Indian brand)', 3.49, 190, 1),
            (2, 'Amoxil 500', 'Amoxicillin 500mg - Antibiotic (Indian brand)', 11.99, 85, 1),
            (2, 'Moxikind CV', 'Amoxicillin + Clavulanic acid - Antibiotic (Indian brand)', 15.99, 75, 1),
            (2, 'Taxim 200', 'Cefotaxime 200mg - Antibiotic (Indian brand)', 18.99, 65, 1),
            (2, 'Ceftum 500', 'Cefuroxime 500mg - Antibiotic (Indian brand)', 20.99, 60, 1),
            (2, 'Levoflox 500', 'Levofloxacin 500mg - Antibiotic (Indian brand)', 22.99, 55, 1),
            (3, 'Pan 40', 'Pantoprazole 40mg - Acid reflux (Indian brand)', 9.99, 130, 1),
            (3, 'Pan D', 'Pantoprazole + Domperidone - Acid reflux (Indian brand)', 12.99, 115, 1),
            (3, 'Ranitidine 150', 'H2 blocker - Acid reflux (Indian brand)', 5.99, 150, 1),
            (3, 'Aciloc 150', 'Ranitidine 150mg - Acid reflux (Indian brand)', 6.49, 145, 1),
            (3, 'Gaviscon', 'Antacid - Acid reflux (Indian brand)', 8.99, 120, 1),
            (4, 'Glycomet GP2', 'Metformin + Glimepiride - Diabetes (Indian brand)', 21.99, 85, 1),
            (4, 'Glucophage 500', 'Metformin 500mg - Diabetes (Indian brand)', 14.99, 140, 1),
            (4, 'Januvia 100', 'Sitagliptin 100mg - Diabetes (Indian brand)', 26.99, 70, 1),
            (4, 'Galvus Met', 'Vildagliptin + Metformin - Diabetes (Indian brand)', 24.99, 75, 1),
            (4, 'Trucomet XR', 'Metformin extended release - Diabetes (Indian brand)', 16.99, 100, 1),
            (5, 'Telma H', 'Telmisartan + Hydrochlorothiazide - BP (Indian brand)', 15.99, 120, 1),
            (5, 'Telsartan 40', 'Telmisartan 40mg - BP (Indian brand)', 14.99, 125, 1),
            (5, 'Telma 80', 'Telmisartan 80mg - BP (Indian brand)', 18.99, 110, 1),
            (5, 'Nusar 40', 'Telmisartan 40mg - BP (Indian brand)', 13.99, 130, 1),
            (1, 'Amlokind 5', 'Amlodipine 5mg - BP (Indian brand)', 10.99, 140, 1),
            (1, 'Amlokind AT', 'Amlodipine + Atenolol - BP (Indian brand)', 14.99, 115, 1),
            (1, 'Amlip 5', 'Amlodipine 5mg - BP (Indian brand)', 11.99, 135, 1),
            (2, 'Atorva 5', 'Atorvastatin 5mg - Cholesterol (Indian brand)', 14.99, 110, 1),
            (2, 'Atorva 20', 'Atorvastatin 20mg - Cholesterol (Indian brand)', 19.99, 95, 1),
            (2, 'Lipvas 10', 'Atorvastatin 10mg - Cholesterol (Indian brand)', 16.99, 105, 1),
            (2, 'Crestor 10', 'Rosuvastatin 10mg - Cholesterol (Indian brand)', 24.99, 80, 1),
            (2, 'Storvas 10', 'Atorvastatin 10mg - Cholesterol (Indian brand)', 15.99, 100, 1),
            (3, 'Deplatt 75', 'Clopidogrel 75mg - Heart (Indian brand)', 15.99, 115, 1),
            (3, 'Clopitor 75', 'Clopidogrel 75mg - Heart (Indian brand)', 16.99, 110, 1),
            (3, 'Plavix 75', 'Clopidogrel 75mg - Heart (Indian brand)', 18.99, 95, 1),
            (3, 'Angised', 'Nitroglycerin - Heart (Indian brand)', 12.99, 85, 1),
            (4, 'Asthalin 4', 'Salbutamol 4mg - Asthma (Indian brand)', 9.99, 130, 1),
            (4, 'Asthalin Rotacaps', 'Salbutamol - Asthma (Indian brand)', 11.99, 120, 1),
            (4, 'Budecort 200', 'Budesonide 200mcg - Asthma (Indian brand)', 15.99, 100, 1),
            (4, 'Budenase AQ', 'Budesonide nasal spray - Asthma (Indian brand)', 18.99, 90, 1),
            (5, 'Allegra M', 'Fexofenadine + Montelukast - Allergy (Indian brand)', 14.99, 125, 1),
            (5, 'Montair 10', 'Montelukast 10mg - Allergy (Indian brand)', 13.99, 130, 1),
            (5, 'Montair FX', 'Montelukast + Fexofenadine - Allergy (Indian brand)', 16.99, 115, 1),
            (5, 'Avil 25', 'Pheniramine - Allergy (Indian brand)', 4.99, 150, 1),
            (1, 'Eltroxin 100mcg', 'Levothyroxine 100mcg - Thyroid (Indian brand)', 14.99, 110, 1),
            (1, 'Thyrox 50mcg', 'Levothyroxine 50mcg - Thyroid (Indian brand)', 12.99, 120, 1),
            (1, 'Thyronorm 100mcg', 'Levothyroxine 100mcg - Thyroid (Indian brand)', 13.99, 115, 1),
            (2, 'Gabantin 300', 'Gabapentin 300mg - Nerve pain (Indian brand)', 17.99, 105, 1),
            (2, 'Gabantin 400', 'Gabapentin 400mg - Nerve pain (Indian brand)', 19.99, 95, 1),
            (2, 'Lyrica 75', 'Pregabalin 75mg - Nerve pain (Indian brand)', 24.99, 80, 1),
            (2, 'Maxgalin 75', 'Pregabalin 75mg - Nerve pain (Indian brand)', 22.99, 85, 1),
            (3, 'Stilnoct 10', 'Zolpidem 10mg - Insomnia (Indian brand)', 19.99, 105, 1),
            (3, 'Imovane 7.5', 'Zopiclone 7.5mg - Insomnia (Indian brand)', 18.99, 100, 1),
            (3, 'Zapiz 0.5', 'Clonazepam 0.5mg - Insomnia (Indian brand)', 12.99, 110, 1),
            (4, 'Setraline 50', 'Sertraline 50mg - Depression (Indian brand)', 15.99, 120, 1),
            (4, 'Zosert 50', 'Sertraline 50mg - Depression (Indian brand)', 16.99, 115, 1),
            (4, 'Fludac 20', 'Fluoxetine 20mg - Depression (Indian brand)', 13.99, 130, 1),
            (4, 'Pexep CR 12.5', 'Paroxetine CR - Depression (Indian brand)', 18.99, 95, 1),
            (5, 'Voveran 50', 'Diclofenac 50mg - Pain (Indian brand)', 5.99, 140, 1),
            (5, 'Voveran SR 100', 'Diclofenac SR - Pain (Indian brand)', 7.99, 125, 1),
            (5, 'Dynapar', 'Diclofenac + Paracetamol - Pain (Indian brand)', 8.99, 120, 1),
            (1, 'Hifenac P', 'Aceclofenac + Paracetamol - Pain (Indian brand)', 9.99, 115, 1),
            (1, 'Myospaz', 'Chlorzoxazone + Diclofenac - Pain (Indian brand)', 11.99, 110, 1),
            (2, 'Pan 40', 'Pantoprazole 40mg - Gastric (Indian brand)', 9.99, 130, 1),
            (2, 'Gelusil MPS', 'Antacid - Gastric (Indian brand)', 7.99, 140, 1),
            (2, 'Digene', 'Antacid - Gastric (Indian brand)', 8.49, 135, 1),
            (2, 'Mucaine Gel', 'Antacid - Gastric (Indian brand)', 9.49, 125, 1),
            (3, 'Flagyl 400', 'Metronidazole 400mg - Antibiotic (Indian brand)', 9.99, 120, 1),
            (3, 'Metrogyl 400', 'Metronidazole 400mg - Antibiotic (Indian brand)', 10.99, 115, 1),
            (3, 'Ornidazole 500', 'Ornidazole 500mg - Antibiotic (Indian brand)', 11.99, 110, 1),
            (3, 'Oflox 200', 'Ofloxacin 200mg - Antibiotic (Indian brand)', 12.99, 105, 1),
            (4, 'Udiliv 300', 'Ursodeoxycholic acid - Liver (Indian brand)', 18.99, 90, 1),
            (4, 'Ursocol 300', 'Ursodeoxycholic acid - Liver (Indian brand)', 19.99, 85, 1),
            (4, 'Silymarin 140', 'Liver support - Liver (Indian brand)', 14.99, 100, 1),
            (4, 'Hepamerz', 'Liver support - Liver (Indian brand)', 16.99, 95, 1),
            (5, 'Nasonex', 'Mometasone nasal spray - Allergy (Indian brand)', 22.99, 80, 1),
            (5, 'Flomist', 'Fluticasone nasal spray - Allergy (Indian brand)', 20.99, 85, 1),
            (5, 'Otrivin', 'Xylometazoline nasal drops - Nasal (Indian brand)', 8.99, 130, 1),
            (5, 'Nasivin', 'Oxymetazoline nasal drops - Nasal (Indian brand)', 9.99, 125, 1),
        ]
        cursor.executemany('INSERT INTO medicines (pharmacy_id, name, description, price, stock_quantity, available) VALUES (?, ?, ?, ?, ?, ?)', medicines_data)
        
        # Insert sample patients
        patients_data = [
            ('John Smith', 'john.smith@email.com', '+1234567890', 35, 'male', '123 Oak Street, City Center', 'patient123'),
            ('Jane Doe', 'jane.doe@email.com', '+1234567891', 28, 'female', '456 Maple Avenue, West Side', 'patient123'),
            ('Robert Johnson', 'robert.johnson@email.com', '+1234567892', 42, 'male', '789 Pine Road, East District', 'patient123'),
            ('Emily Brown', 'emily.brown@email.com', '+1234567893', 31, 'female', '321 Elm Street, North Side', 'patient123'),
            ('Michael Davis', 'michael.davis@email.com', '+1234567894', 55, 'male', '654 Birch Drive, South Side', 'patient123'),
        ]
        cursor.executemany('INSERT INTO patients (name, email, phone, age, gender, address, password) VALUES (?, ?, ?, ?, ?, ?, ?)', patients_data)
        
        conn.commit()
        print("Database initialized with sample data!")
    
    conn.close()

# Initialize database on startup
init_db()

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy', 'message': 'Telemedicine API is running'})

# Patient endpoints
@app.route('/api/patients', methods=['POST'])
def create_patient():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO patients (name, email, phone, age, gender, address, password)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (data['name'], data['email'], data['phone'], data['age'], data['gender'], data['address'], data['password']))
        conn.commit()
        return jsonify({'message': 'Patient created successfully', 'id': cursor.lastrowid}), 201
    except sqlite3.IntegrityError as e:
        return jsonify({'error': str(e)}), 500
    finally:
        conn.close()

@app.route('/api/patients/login', methods=['POST'])
def patient_login():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM patients WHERE email = ? AND password = ?', (data['email'], data['password']))
        patient = cursor.fetchone()
        if patient:
            return jsonify({'message': 'Login successful', 'patient': dict(patient)}), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    finally:
        conn.close()

@app.route('/api/patients/<int:patient_id>', methods=['GET'])
def get_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        patient = cursor.fetchone()
        if patient:
            return jsonify(dict(patient)), 200
        return jsonify({'error': 'Patient not found'}), 404
    finally:
        conn.close()

# Doctor endpoints
@app.route('/api/doctors', methods=['GET'])
def get_doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM doctors WHERE available = 1')
        doctors = cursor.fetchall()
        return jsonify([dict(doc) for doc in doctors]), 200
    finally:
        conn.close()

@app.route('/api/doctors/search', methods=['GET'])
def search_doctors():
    search_term = request.args.get('q', '')
    specialization = request.args.get('specialization', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        if search_term and specialization:
            cursor.execute('SELECT * FROM doctors WHERE available = 1 AND (name LIKE ? OR specialization LIKE ?) AND specialization = ?', 
                         (f'%{search_term}%', f'%{search_term}%', specialization))
        elif search_term:
            cursor.execute('SELECT * FROM doctors WHERE available = 1 AND (name LIKE ? OR specialization LIKE ?)', 
                         (f'%{search_term}%', f'%{search_term}%'))
        elif specialization:
            cursor.execute('SELECT * FROM doctors WHERE available = 1 AND specialization = ?', (specialization,))
        else:
            cursor.execute('SELECT * FROM doctors WHERE available = 1')
        doctors = cursor.fetchall()
        return jsonify([dict(doc) for doc in doctors]), 200
    finally:
        conn.close()

@app.route('/api/doctors/specializations', methods=['GET'])
def get_specializations():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT DISTINCT specialization FROM doctors WHERE available = 1 ORDER BY specialization')
        specializations = cursor.fetchall()
        return jsonify([s[0] for s in specializations]), 200
    finally:
        conn.close()

@app.route('/api/doctors/<int:doctor_id>', methods=['GET'])
def get_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM doctors WHERE id = ?', (doctor_id,))
        doctor = cursor.fetchone()
        if doctor:
            return jsonify(dict(doctor)), 200
        return jsonify({'error': 'Doctor not found'}), 404
    finally:
        conn.close()

# Consultation endpoints
@app.route('/api/consultations', methods=['POST'])
def create_consultation():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO consultations (patient_id, doctor_id, symptoms, status, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (data['patient_id'], data['doctor_id'], data['symptoms'], 'pending', datetime.datetime.now()))
        conn.commit()
        return jsonify({'message': 'Consultation created successfully', 'id': cursor.lastrowid}), 201
    finally:
        conn.close()

@app.route('/api/consultations/<int:consultation_id>', methods=['GET'])
def get_consultation(consultation_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM consultations WHERE id = ?', (consultation_id,))
        consultation = cursor.fetchone()
        if consultation:
            return jsonify(dict(consultation)), 200
        return jsonify({'error': 'Consultation not found'}), 404
    finally:
        conn.close()

@app.route('/api/consultations/patient/<int:patient_id>', methods=['GET'])
def get_patient_consultations(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT c.*, d.name as doctor_name, d.specialization
            FROM consultations c
            JOIN doctors d ON c.doctor_id = d.id
            WHERE c.patient_id = ?
            ORDER BY c.created_at DESC
        ''', (patient_id,))
        consultations = cursor.fetchall()
        return jsonify([dict(c) for c in consultations]), 200
    finally:
        conn.close()

@app.route('/api/consultations/<int:consultation_id>/prescription', methods=['POST'])
def add_prescription():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO prescriptions (consultation_id, medicines, instructions, created_at)
            VALUES (?, ?, ?, ?)
        ''', (data['consultation_id'], data['medicines'], data['instructions'], datetime.datetime.now()))
        conn.commit()
        
        cursor.execute('UPDATE consultations SET status = ? WHERE id = ?', ('completed', data['consultation_id']))
        conn.commit()
        
        return jsonify({'message': 'Prescription added successfully'}), 201
    finally:
        conn.close()

# Pharmacy endpoints
@app.route('/api/pharmacies', methods=['GET'])
def get_pharmacies():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM pharmacies')
        pharmacies = cursor.fetchall()
        return jsonify([dict(pharm) for pharm in pharmacies]), 200
    finally:
        conn.close()

@app.route('/api/pharmacies/<int:pharmacy_id>/medicines', methods=['GET'])
def get_pharmacy_medicines(pharmacy_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM medicines WHERE pharmacy_id = ? AND available = 1', (pharmacy_id,))
        medicines = cursor.fetchall()
        return jsonify([dict(med) for med in medicines]), 200
    finally:
        conn.close()

@app.route('/api/medicines/search', methods=['GET'])
def search_medicines():
    search_term = request.args.get('q', '')
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT m.*, p.name as pharmacy_name, p.address as pharmacy_address, p.phone as pharmacy_phone
            FROM medicines m
            JOIN pharmacies p ON m.pharmacy_id = p.id
            WHERE m.name LIKE ? AND m.available = 1
        ''', (f'%{search_term}%',))
        medicines = cursor.fetchall()
        return jsonify([dict(med) for med in medicines]), 200
    finally:
        conn.close()

# Follow-up endpoints
@app.route('/api/followups', methods=['POST'])
def create_followup():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO followups (consultation_id, patient_id, doctor_id, scheduled_date, notes, status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (data['consultation_id'], data['patient_id'], data['doctor_id'], data['scheduled_date'], data.get('notes', ''), 'scheduled'))
        conn.commit()
        return jsonify({'message': 'Follow-up scheduled successfully', 'id': cursor.lastrowid}), 201
    finally:
        conn.close()

@app.route('/api/followups/patient/<int:patient_id>', methods=['GET'])
def get_patient_followups(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            SELECT f.*, d.name as doctor_name
            FROM followups f
            JOIN doctors d ON f.doctor_id = d.id
            WHERE f.patient_id = ?
            ORDER BY f.scheduled_date ASC
        ''', (patient_id,))
        followups = cursor.fetchall()
        return jsonify([dict(f) for f in followups]), 200
    finally:
        conn.close()

@app.route('/api/followups/<int:followup_id>/complete', methods=['PUT'])
def complete_followup(followup_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE followups SET status = ? WHERE id = ?', ('completed', followup_id))
        conn.commit()
        return jsonify({'message': 'Follow-up marked as completed'}), 200
    finally:
        conn.close()

# Serve frontend
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=False, port=port)
