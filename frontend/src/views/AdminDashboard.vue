<template>
  <div style="background-color: #f8fafc; min-height: 100vh;">
    <NavBar />
    <div class="container-fluid px-4 py-4">
      <!-- Header -->
      <div class="d-flex justify-content-between align-items-start mb-4">
        <div>
          <h3 class="fw-bold mb-1">Institute Placement Cell Portal</h3>
          <p class="text-muted small mb-0">Superuser Administrative Console • Company Approvals & Placement Drives Management</p>
        </div>
        <div class="d-flex gap-2">
          <button class="btn btn-outline-secondary btn-sm" @click="triggerReminders">🔔 Trigger Daily Reminders</button>
          <button class="btn btn-primary btn-sm" @click="generateReport">📄 Generate Monthly Report</button>
        </div>
      </div>

      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <p class="text-muted small mb-1">Total Students</p>
                <h3 class="fw-bold mb-1">{{ stats.total_students }}</h3>
                <p class="text-muted small mb-0">{{ stats.placed_students }} placed ({{ stats.placement_rate }}%)</p>
              </div>
              <span class="fs-4">👥</span>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <p class="text-muted small mb-1">Total Companies</p>
                <h3 class="fw-bold mb-1">{{ stats.total_companies }}</h3>
                <p class="text-warning small mb-0">{{ pendingCompanies.length }} pending approval</p>
              </div>
              <span class="fs-4">🏢</span>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <div class="d-flex justify-content-between align-items-start">
               <div>
                <p class="text-muted small mb-1">Placement Drives</p>
                <h3 class="fw-bold mb-1">{{ stats.pending_jobs }}</h3>
                <p class="text-warning small mb-0">drives pending review</p>
              </div>
              <span class="fs-4">💼</span>
            </div>
          </div>
        </div>
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <div class="d-flex justify-content-between align-items-start">
              <div>
                <p class="text-muted small mb-1">Total Applications</p>
                <h3 class="fw-bold mb-1">{{ stats.total_applications }}</h3>
                <p class="text-muted small mb-0">Across all companies</p>
              </div>
              <span class="fs-4">📊</span>
            </div>
          </div>
        </div>
      </div>

      <!--  Tabs -->
      <div class="card border-0 shadow-sm">
        <div class="card-header bg-white border-bottom">
          <ul class="nav nav-tabs card-header-tabs">
            <li class="nav-item">
              <button class="nav-link" :class="{ active: activeTab === 'overview' }" @click="activeTab = 'overview'">
                Overview & Queue
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="{ active: activeTab === 'companies' }" @click="activeTab = 'companies'">
                Companies
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="{ active: activeTab === 'jobs' }" @click="activeTab = 'jobs'">
                Placement Drives
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="{ active: activeTab === 'students' }" @click="activeTab = 'students'">
                Student Directory
              </button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="{ active: activeTab === 'applications' }" @click="activeTab = 'applications'">
                All Applications
              </button>
            </li>
          </ul>
        </div>

        <div class="card-body">
          <!-- Overview Tab -->
          <div v-if="activeTab === 'overview'">
            <h5 class="fw-bold mb-3">⚠️ Pending Approvals Queue</h5>
            <div class="alert alert-warning d-flex justify-content-between align-items-center" v-if="pendingCompanies.length > 0">
              <div>
                <strong>Company Registrations Pending Approval</strong>
                <p class="mb-0 small">{{ pendingCompanies.length }} companies awaiting verification.</p>
              </div>
              <button class="btn btn-warning btn-sm" @click="activeTab = 'companies'">Review Companies</button>
            </div>
            <div class="alert alert-info d-flex justify-content-between align-items-center">
              <div>
                <strong>Placement Drives Pending Approval</strong>
                <p class="mb-0 small">{{ stats.total_jobs }} drives waiting for admin go-ahead.</p>
              </div>
              <button class="btn btn-info btn-sm text-white" @click="activeTab = 'jobs'">Review Drives</button>
            </div>
          </div>
          <!-- Companies Tab -->
          <div v-if="activeTab === 'companies'">
            <h5 class="fw-bold mb-3">Pending Companies</h5>
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>Name</th>
                  <th>Industry</th>
                  <th>Location</th>
                  <th>Email</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="company in pendingCompanies" :key="company.id">
                  <td>{{ company.name }}</td>
                  <td>{{ company.industry }}</td>
                  <td>{{ company.location }}</td>
                  <td>{{ company.email }}</td>
                  <td>
                    <button class="btn btn-success btn-sm me-2" @click="approveCompany(company.id)">Approve</button>
                    <button class="btn btn-danger btn-sm" @click="removeCompany(company.id)">Remove</button>
                  </td>
                </tr>
              </tbody>
            </table>
            <hr class="my-4">
            <h5 class="fw-bold mb-3">Search Companies</h5>
            <div class="row mb-3">
              <div class="col-md-5">
                <input type="text" class="form-control" placeholder="Search by name" v-model="companySearch.name">
              </div>
              <div class="col-md-5">
                <input type="text" class="form-control" placeholder="Search by industry" v-model="companySearch.industry">
              </div>
              <div class="col-md-2">
                <button class="btn btn-primary w-100" @click="searchCompanies">Search</button>
              </div>
            </div>
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>Name</th>
                  <th>Industry</th>
                  <th>Location</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="company in searchedCompanies" :key="company.id">
                  <td>{{ company.name }}</td>
                  <td>{{ company.industry }}</td>
                  <td>{{ company.location }}</td>
                  <td>
                    <span class="badge" :class="company.is_approved ? 'bg-success' : 'bg-warning'">
                      {{ company.is_approved ? 'Approved' : 'Pending' }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-warning btn-sm" v-if="company.is_active" @click="deactivateCompany(company.id)">Deactivate</button>
                    <button class="btn btn-danger btn-sm" @click="removeCompany(company.id)">Remove</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Jobs Tab -->
          <div v-if="activeTab === 'jobs'">
            <h5 class="fw-bold mb-3">All Placement Drives</h5>
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>Title</th>
                  <th>Company</th>
                  <th>Location</th>
                  <th>Salary</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="job in allJobs" :key="job.id">
                  <td>{{ job.title }}</td>
                  <td>{{ job.company }}</td>
                  <td>{{ job.location }}</td>
                  <td>{{ job.salary }}</td>
                  <td>
                    <span class="badge" :class="job.status === 'approved' ? 'bg-success' : job.status === 'pending' ? 'bg-warning' : 'bg-secondary'">
                      {{ job.status.toUpperCase() }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-success btn-sm me-2" v-if="job.status==='pending'" @click="approveJob(job.id)">Approve</button>
                    <button class="btn btn-danger btn-sm" @click="removeJob(job.id)">Remove</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Students Tab -->
          <div v-if="activeTab === 'students'">
            <h5 class="fw-bold mb-3">Student Directory</h5>
            <div class="row mb-3">
              <div class="col-md-4">
                <input type="text" class="form-control" placeholder="Search by name" v-model="studentSearch.name">
              </div>
              <div class="col-md-3">
                <input type="text" class="form-control" placeholder="Search by ID" v-model="studentSearch.id">
              </div>
              <div class="col-md-2">
                <button class="btn btn-primary w-100" @click="searchStudents">Search</button>
              </div>
            </div>
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Education</th>
                  <th>Skills</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="student in searchedStudents" :key="student.id">
                  <td>{{ student.id }}</td>
                  <td>{{ student.full_name }}</td>
                  <td>{{ student.education }}</td>
                  <td>{{ student.skills }}</td>
                  <td>
                    <span class="badge" :class="student.is_active ? 'bg-success' : 'bg-danger'">
                      {{ student.is_active ? 'Active' : 'Deactivated' }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-info btn-sm me-2 text-white" @click="viewStudentHistory(student.id)">View</button>
                    <button class="btn btn-warning btn-sm" v-if="student.is_active" @click="deactivateStudent(student.id)">Deactivate</button>
                  </td>
                </tr>
              </tbody>
            </table>          

            <!-- Student History -->
            <div class="card border-0 bg-light mt-4" v-if="selectedStudent">
              <div class="card-body">
                <h5 class="fw-bold">{{ selectedStudent.full_name }} — Application History</h5>
                <p class="text-muted small">{{ selectedStudent.email }}</p>
                <table class="table table-sm">
                  <thead>
                    <tr>
                      <th>Job</th>
                      <th>Company</th>
                      <th>Status</th>
                      <th>Applied At</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="app in selectedStudentApplications" :key="app.id">
                      <td>{{ app.job_title }}</td>
                      <td>{{ app.company }}</td>
                      <td>
                        <span class="badge bg-primary">{{ app.status }}</span>
                      </td>
                      <td>{{ app.applied_at }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

          <!-- Applications Tab -->
          <div v-if="activeTab === 'applications'">
            <h5 class="fw-bold mb-3">All Applications</h5>
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>Student</th>
                  <th>Job</th>
                  <th>Company</th>
                  <th>Status</th>
                  <th>Applied At</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="application in allApplications" :key="application.id">
                  <td>{{ application.student }}</td>
                  <td>{{ application.job }}</td>
                  <td>{{ application.company }}</td>
                  <td>
                    <span class="badge bg-primary">{{ application.status }}</span>
                  </td>
                  <td>{{ application.applied_at }}</td>
                </tr>
              </tbody>
            </table>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';

export default {
    name: 'AdminDashboard',
    components: {
        NavBar
    },
    data() {
        return {
            stats: {
                total_students: 0,
                total_companies: 0,
                total_jobs: 0,
                total_applications: 0
            },
            pendingCompanies: [],
            companySearch: {
                name: '',
                industry: ''
            },
            searchedCompanies: [],
            studentSearch: {
            name: '',
            id: ''
            },
            searchedStudents: [],
            allJobs:[],
            allApplications: [],
            selectedStudent: null,
            selectedStudentApplications: [],
            activeTab: 'overview'
        }
        
    },
    mounted() {
        this.fetchStats()
        this.fetchPendingCompanies()
        this.fetchAllJobs()
        this.fetchAllApplications()
    },
    methods: {
        async fetchStats() {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/dashboard/stats`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.stats = data 
        },
        async fetchPendingCompanies() {
            const token = localStorage.getItem('token')
            const response = await fetch('http://127.0.0.1:5000/admin/companies/pending', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.pendingCompanies = data 
        },
        async approveCompany(companyId) {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/companies/${companyId}/approve`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            alert(data.message)
            this.fetchPendingCompanies()
            this.fetchStats()
        },
        async removeCompany(companyId) {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/companies/${companyId}/remove`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }    
            })
            const data = await response.json()
            alert(data.message)
            this.fetchPendingCompanies()
            this.fetchStats()
        },
        async searchCompanies() {
            const token = localStorage.getItem('token')
            const response = await fetch(
                `http://127.0.0.1:5000/admin/companies/search?name=${this.companySearch.name}&industry=${this.companySearch.industry}`,
                {
                    headers: {
                    'Authorization': `Bearer ${token}`
                    }        
                }
            )
           const data =await response.json()
           this.searchedCompanies = data
        },
        async deactivateCompany(companyId) {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/companies/${companyId}/deactivate`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            alert(data.message)
            this.searchCompanies()
        },
        async searchStudents() {
            const token = localStorage.getItem('token')
            const response = await fetch(
                `http://127.0.0.1:5000/admin/students/search?name=${this.studentSearch.name}&id=${this.studentSearch.id}`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            )
            const data = await response.json()
            this.searchedStudents = data
        },
        async deactivateStudent(studentId) {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/students/${studentId}/deactivate`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            alert(data.message)
            this.searchStudents()
        },
        async fetchAllJobs() {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/jobs`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.allJobs = data
        },
        async approveJob(jobId) {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/jobs/${jobId}/approve`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            alert(data.message)
            this.fetchAllJobs()
            this.fetchStats()
        },
        async removeJob(jobId) {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/jobs/${jobId}/remove`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            alert(data.message)
            this.fetchAllJobs()
            this.fetchStats()
        },
        async fetchAllApplications() {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/admin/applications`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.allApplications = data
        },
        async viewStudentHistory(studentId) {
            const token = localStorage.getItem('token')

            const profileResponse = await fetch(`http://127.0.0.1:5000/admin/students/${studentId}`, {
                headers: {'Authorization': `Bearer ${token}`}
            })
            this.selectedStudent = await profileResponse.json()

            const appsResponse = await fetch(`http://127.0.0.1:5000/admin/students/${studentId}/applications`, {
                headers: {'Authorization': `Bearer ${token}`}
            })
            this.selectedStudentApplications = await appsResponse.json()
        },
        async triggerReminders() {
          const token = localStorage.getItem('token')
          const response = await fetch('http://127.0.0.1:5000/admin/trigger-reminders', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`}
          })
          const data = await response.json()
          alert(data.message)
        },
        async generateReport() {
          const token = localStorage.getItem('token')
          const response = await fetch('http://127.0.0.1:5000/admin/generate-report', {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`}
          })
          const data = await response.json()
          alert(data.message)
        }
    }
}
</script>