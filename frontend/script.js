// API Base URL
const API_URL = 'http://localhost:5000/api';

// Current user state
let currentUser = null;

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in
    const savedUser = localStorage.getItem('currentUser');
    if (savedUser) {
        currentUser = JSON.parse(savedUser);
        showSection('home');
    } else {
        showSection('login');
    }

    // Setup form listeners
    setupFormListeners();
});

// Setup form event listeners
function setupFormListeners() {
    // Login form
    document.getElementById('loginForm').addEventListener('submit', handleLogin);
    
    // Register form
    document.getElementById('registerForm').addEventListener('submit', handleRegister);
    
    // Consultation form
    document.getElementById('consultationForm').addEventListener('submit', handleConsultation);
    
    // Medicine search on Enter key
    document.getElementById('medicineSearch').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            searchMedicines();
        }
    });
}

// Toggle between login and register
function toggleAuth(type) {
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const toggleBtns = document.querySelectorAll('.toggle-btn');
    
    toggleBtns.forEach(btn => btn.classList.remove('active'));
    
    if (type === 'login') {
        loginForm.classList.remove('hidden');
        registerForm.classList.add('hidden');
        toggleBtns[0].classList.add('active');
    } else {
        loginForm.classList.add('hidden');
        registerForm.classList.remove('hidden');
        toggleBtns[1].classList.add('active');
    }
}

// Handle login
async function handleLogin(e) {
    e.preventDefault();
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const response = await fetch(`${API_URL}/patients/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            currentUser = data.patient;
            localStorage.setItem('currentUser', JSON.stringify(currentUser));
            showSection('home');
            alert('Login successful!');
        } else {
            alert(data.error || 'Login failed');
        }
    } catch (error) {
        console.error('Login error:', error);
        alert('Error connecting to server. Please make sure the backend is running.');
    }
}

// Handle registration
async function handleRegister(e) {
    e.preventDefault();
    
    const patientData = {
        name: document.getElementById('regName').value,
        email: document.getElementById('regEmail').value,
        phone: document.getElementById('regPhone').value,
        age: parseInt(document.getElementById('regAge').value),
        gender: document.getElementById('regGender').value,
        address: document.getElementById('regAddress').value,
        password: document.getElementById('regPassword').value
    };
    
    try {
        const response = await fetch(`${API_URL}/patients`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(patientData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Registration successful! Please login.');
            toggleAuth('login');
            document.getElementById('registerForm').reset();
        } else {
            alert(data.error || 'Registration failed');
        }
    } catch (error) {
        console.error('Registration error:', error);
        alert('Error connecting to server. Please make sure the backend is running.');
    }
}

// Logout
function logout() {
    currentUser = null;
    localStorage.removeItem('currentUser');
    showSection('login');
    alert('Logged out successfully');
}

// Show section
function showSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(section => {
        section.classList.remove('active');
        section.classList.add('hidden');
    });
    
    // Show selected section
    const section = document.getElementById(`${sectionName}Section`);
    if (section) {
        section.classList.remove('hidden');
        section.classList.add('active');
    }
    
    // Show/hide navigation
    const navLinks = document.getElementById('navLinks');
    if (sectionName === 'login') {
        navLinks.style.display = 'none';
    } else {
        navLinks.style.display = 'flex';
    }
    
    // Load section-specific data
    if (sectionName === 'doctors') {
        loadDoctors();
    } else if (sectionName === 'medicines') {
        loadMedicines();
    } else if (sectionName === 'consultations') {
        loadConsultations();
    } else if (sectionName === 'followups') {
        loadFollowups();
    }
}

// Load doctors
async function loadDoctors() {
    try {
        const response = await fetch(`${API_URL}/doctors`);
        const doctors = await response.json();
        
        const doctorsList = document.getElementById('doctorsList');
        doctorsList.innerHTML = '';
        
        if (doctors.length === 0) {
            doctorsList.innerHTML = '<p>No doctors available at the moment.</p>';
            return;
        }
        
        doctors.forEach(doctor => {
            const card = document.createElement('div');
            card.className = 'doctor-card';
            card.innerHTML = `
                <h3>${doctor.name}</h3>
                <p class="specialization">${doctor.specialization}</p>
                <p>Experience: ${doctor.experience_years} years</p>
                <p>Phone: ${doctor.phone}</p>
                <button onclick="openConsultationModal(${doctor.id}, '${doctor.name}')" class="btn btn-primary" style="margin-top: 1rem;">Request Consultation</button>
            `;
            doctorsList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading doctors:', error);
        document.getElementById('doctorsList').innerHTML = '<p>Error loading doctors. Please try again later.</p>';
    }
}

// Open consultation modal
function openConsultationModal(doctorId, doctorName) {
    if (!currentUser) {
        alert('Please login to request a consultation');
        showSection('login');
        return;
    }
    
    document.getElementById('selectedDoctorId').value = doctorId;
    document.getElementById('consultationModal').classList.remove('hidden');
}

// Close modal
function closeModal(modalId) {
    document.getElementById(modalId).classList.add('hidden');
}

// Handle consultation
async function handleConsultation(e) {
    e.preventDefault();
    
    const consultationData = {
        patient_id: currentUser.id,
        doctor_id: parseInt(document.getElementById('selectedDoctorId').value),
        symptoms: document.getElementById('symptoms').value
    };
    
    try {
        const response = await fetch(`${API_URL}/consultations`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(consultationData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            alert('Consultation request submitted successfully!');
            closeModal('consultationModal');
            document.getElementById('consultationForm').reset();
            showSection('consultations');
        } else {
            alert(data.error || 'Failed to submit consultation request');
        }
    } catch (error) {
        console.error('Consultation error:', error);
        alert('Error connecting to server. Please try again.');
    }
}

// Load medicines
async function loadMedicines() {
    try {
        const response = await fetch(`${API_URL}/pharmacies`);
        const pharmacies = await response.json();
        
        // Load medicines from first pharmacy
        if (pharmacies.length > 0) {
            const medResponse = await fetch(`${API_URL}/pharmacies/${pharmacies[0].id}/medicines`);
            const medicines = await medResponse.json();
            displayMedicines(medicines);
        }
    } catch (error) {
        console.error('Error loading medicines:', error);
        document.getElementById('medicinesList').innerHTML = '<p>Error loading medicines. Please try again later.</p>';
    }
}

// Search medicines
async function searchMedicines() {
    const searchTerm = document.getElementById('medicineSearch').value;
    
    if (!searchTerm.trim()) {
        loadMedicines();
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/medicines/search?q=${encodeURIComponent(searchTerm)}`);
        const medicines = await response.json();
        displayMedicines(medicines);
    } catch (error) {
        console.error('Error searching medicines:', error);
        document.getElementById('medicinesList').innerHTML = '<p>Error searching medicines. Please try again.</p>';
    }
}

// Display medicines
function displayMedicines(medicines) {
    const medicinesList = document.getElementById('medicinesList');
    medicinesList.innerHTML = '';
    
    if (medicines.length === 0) {
        medicinesList.innerHTML = '<p>No medicines found.</p>';
        return;
    }
    
    medicines.forEach(medicine => {
        const card = document.createElement('div');
        card.className = 'medicine-card';
        card.innerHTML = `
            <h3>${medicine.name}</h3>
            <p>${medicine.description || 'No description available'}</p>
            <p class="price">$${medicine.price}</p>
            <p class="pharmacy">Available at: ${medicine.pharmacy_name}</p>
            <p class="pharmacy">📍 ${medicine.pharmacy_address}</p>
            <p class="pharmacy">📞 ${medicine.pharmacy_phone}</p>
            <p class="pharmacy">Stock: ${medicine.stock_quantity} units</p>
        `;
        medicinesList.appendChild(card);
    });
}

// Load consultations
async function loadConsultations() {
    if (!currentUser) {
        showSection('login');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/consultations/patient/${currentUser.id}`);
        const consultations = await response.json();
        
        const consultationsList = document.getElementById('consultationsList');
        consultationsList.innerHTML = '';
        
        if (consultations.length === 0) {
            consultationsList.innerHTML = '<p>No consultations yet. <a href="#" onclick="showSection(\'doctors\')" style="color: #667eea;">Find a doctor</a></p>';
            return;
        }
        
        consultations.forEach(consultation => {
            const card = document.createElement('div');
            card.className = 'consultation-card';
            card.innerHTML = `
                <h3>Consultation #${consultation.id}</h3>
                <p><strong>Doctor:</strong> ${consultation.doctor_name} (${consultation.specialization})</p>
                <p><strong>Date:</strong> ${new Date(consultation.created_at).toLocaleString()}</p>
                <p><strong>Symptoms:</strong> ${consultation.symptoms}</p>
                <p><strong>Status:</strong> <span class="status ${consultation.status}">${consultation.status.replace('_', ' ')}</span></p>
                ${consultation.diagnosis ? `<p><strong>Diagnosis:</strong> ${consultation.diagnosis}</p>` : ''}
            `;
            consultationsList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading consultations:', error);
        document.getElementById('consultationsList').innerHTML = '<p>Error loading consultations. Please try again.</p>';
    }
}

// Load follow-ups
async function loadFollowups() {
    if (!currentUser) {
        showSection('login');
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/followups/patient/${currentUser.id}`);
        const followups = await response.json();
        
        const followupsList = document.getElementById('followupsList');
        followupsList.innerHTML = '';
        
        if (followups.length === 0) {
            followupsList.innerHTML = '<p>No follow-ups scheduled yet.</p>';
            return;
        }
        
        followups.forEach(followup => {
            const card = document.createElement('div');
            card.className = 'followup-card';
            card.innerHTML = `
                <h3>Follow-up #${followup.id}</h3>
                <p><strong>Doctor:</strong> ${followup.doctor_name}</p>
                <p><strong>Scheduled Date:</strong> ${new Date(followup.scheduled_date).toLocaleDateString()}</p>
                <p><strong>Status:</strong> <span class="status ${followup.status}">${followup.status}</span></p>
                ${followup.notes ? `<p><strong>Notes:</strong> ${followup.notes}</p>` : ''}
                ${followup.status === 'scheduled' ? `<button onclick="completeFollowup(${followup.id})" class="btn btn-success" style="margin-top: 0.5rem;">Mark as Completed</button>` : ''}
            `;
            followupsList.appendChild(card);
        });
    } catch (error) {
        console.error('Error loading follow-ups:', error);
        document.getElementById('followupsList').innerHTML = '<p>Error loading follow-ups. Please try again.</p>';
    }
}

// Complete follow-up
async function completeFollowup(followupId) {
    if (!confirm('Mark this follow-up as completed?')) {
        return;
    }
    
    try {
        const response = await fetch(`${API_URL}/followups/${followupId}/complete`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            alert('Follow-up marked as completed');
            loadFollowups();
        } else {
            alert('Failed to update follow-up status');
        }
    } catch (error) {
        console.error('Error completing follow-up:', error);
        alert('Error updating follow-up. Please try again.');
    }
}
