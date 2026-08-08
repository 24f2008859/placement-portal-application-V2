<template>
  <div style="background-color: #f8fafc; min-height: 100vh;">
    <NavBar />

    <div class="container-fluid px-4 py-4">
      <div v-if="successMessage" class="alert alert-success alert-dismissible fade show">
        {{ successMessage }}
        <button type="button" class="btn-close" @click="successMessage = ''"></button>
      </div>
      <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
        {{ errorMessage }}
        <button type="button" class="btn-close" @click="errorMessage = ''"></button>
      </div>
      <!-- Profile Header -->
      <div class="card border-0 shadow-sm mb-4">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-start">
            <div>
              <h3 class="fw-bold mb-1">{{ profile.full_name }}
                <span class="badge bg-primary ms-2" style="font-size: 0.6rem;">STUDENT</span>
              </h3>
              <p class="text-muted small mb-1">
                Education: <strong>{{ profile.education }}</strong> • 
                Skills: <strong>{{ profile.skills }}</strong> • 
                Branch: <strong>{{ profile.branch }}</strong>
              </p>
            </div>
            <div class="d-flex gap-2">
              <button class="btn btn-outline-secondary btn-sm" @click="activeTab = 'profile'">
                ✏️ Edit Profile & Resume
              </button>
              <button class="btn btn-success btn-sm" @click="exportApplications">
                ⬇️ Export History to CSV
              </button>
            </div>
          </div>
          <p class="text-success small mt-2" v-if="exportMessage">{{ exportMessage }}</p>
          <a v-if="exportFilename"
              :href="`http://127.0.0.1:5000/student/export/download/${exportFilename}`"
              class="btn btn-success btn-sm ms-2"
              target="_blank">
              ⬇️ Download CSV
            </a>
        </div>
      </div>

      <!-- Tabs -->
      <ul class="nav nav-tabs mb-4">
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'jobs' }" @click="activeTab = 'jobs'">
            🏢 Approved Placement Drives
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'applications' }" @click="activeTab = 'applications'">
            📋 My Applications ({{ applications.length }})
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'profile' }" @click="activeTab = 'profile'">
            👤 Resume & Skills
          </button>
        </li>
        <li class="nav-item">
          <button class="nav-link" :class="{ active: activeTab === 'placements' }" @click="activeTab = 'placements'">
            🎯 Placement History
          </button>
        </li>
      </ul>

      <!-- Jobs Tab -->
      <div v-if="activeTab === 'jobs'">
        <div class="mb-3 d-flex gap-2">
          <input type="text" class="form-control" placeholder="Search job title, company name, location..." v-model="searchQuery">
          <button class="btn btn-primary" @click="searchJobs">Search</button>
        </div>
        <div class="row">
          <div class="col-md-6 mb-3" v-for="job in jobs" :key="job.id">
            <div class="card border-0 shadow-sm h-100">
              <div class="card-body">
                <div class="d-flex justify-content-between align-items-start mb-2">
                  <h5 class="fw-bold mb-0">{{ job.title }}</h5>
                  <span class="badge" :class="isEligible(job) ? 'bg-success' : 'bg-danger'">{{ isEligible(job) ? 'Eligible' : 'Not Eligible' }}</span>
                </div>
                <p class="text-primary small fw-bold mb-2">{{ job.company }}</p>
                <p class="text-muted small mb-2">{{ job.description }}</p>
                <div class="row small text-muted mb-3">
                  <div class="col-6">Package: <strong class="text-dark">{{ job.salary }} LPA</strong></div>
                  <div class="col-6">Location: <strong class="text-dark">{{ job.location }}</strong></div>
                  <div class="col-12 mt-1">Skills: <strong class="text-dark">{{ job.skills_required }}</strong></div>
                  <div class="col-6 mt-1" v-if="job.eligible_branch">Branch: <strong class="text-dark">{{ job.eligible_branch }}</strong></div>
                  <div class="col-6 mt-1" v-if="job.minimum_cgpa">Min CGPA: <strong class="text-dark">{{ job.minimum_cgpa }}</strong></div>
                </div>
                <button class="btn btn-primary w-100" @click="applyJob(job.id)">Apply for Drive</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Applications Tab -->
      <div v-if="activeTab === 'applications'">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>Job Title</th>
                  <th>Company</th>
                  <th>Location</th>
                  <th>Salary</th>
                  <th>Status</th>
                  <th>Applied At</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="app in applications" :key="app.id">
                  <td>{{ app.job_title }}</td>
                  <td>{{ app.company }}</td>
                  <td>{{ app.location }}</td>
                  <td>{{ app.salary }}</td>
                  <td>
                    <span class="badge" :class="{
                      'bg-success': app.status === 'selected',
                      'bg-primary': app.status === 'interview',
                      'bg-warning': app.status === 'shortlisted',
                      'bg-danger': app.status === 'rejected',
                      'bg-secondary': app.status === 'applied'
                    }">{{ app.status.toUpperCase() }}</span>
                  </td>
                  <td>{{ app.applied_at }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <!-- Profile Tab -->
      <div v-if="activeTab === 'profile'">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h5 class="fw-bold mb-4">Edit Profile & Resume</h5>
            <div class="row">
              <div class="col-md-6 mb-3">
                <label class="form-label">Full Name</label>
                <input type="text" class="form-control" v-model="profile.full_name">
              </div>
              <div class="col-md-6 mb-3">
                <label class="form-label">Education</label>
                <input type="text" class="form-control" v-model="profile.education">
              </div>
              <div class="col-md-4 mb-3">
                <label class="form-label">Branch</label>
                <select class="form-select" v-model="profile.branch">
                  <option value="">Select Branch</option>
                  <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
                </select>
              </div>
              <div class="col-md-4 mb-3">
                <label class="form-label">Skills</label>
                <input type="text" class="form-control" v-model="profile.skills">
              </div>
              <div class="col-md-4 mb-3">
                <label class="form-label">CGPA</label>
                <input type="number" step="0.01" class="form-control" v-model="profile.cgpa">
              </div>
              
              <div class="col-md-4 mb-3">
                <label for="form-label">Graduation Year</label>
                <input type="number" class="form-control" v-model="profile.graduation_year">
              </div>
              <div class="col-md-12 mb-3">
                <label class="form-label">Resume (PDF, DOC, DOCX)</label>
                <input type="file" class="form-control" @change="handleFileUpload" accept=".pdf,.doc,.docx">
              </div>
              <div class="col-md-12 mb-3" v-if="profile.resume">
                <p class="text-muted small">Current Resume: <strong>{{ profile.resume }}</strong></p>
              </div>
              <div class="col-md-12">
                <button class="btn btn-primary me-2" @click="updateProfile">Update Profile</button>
                <button class="btn btn-secondary" @click="uploadResume">Upload Resume</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Placements Tab -->
      <div v-if="activeTab === 'placements'">
        <div class="card border-0 shadow-sm">
          <div class="card-body">
            <h5 class="fw-bold mb-3">Placement History</h5>
            <table class="table table-hover">
              <thead class="table-light">
                <tr>
                  <th>Company</th>
                  <th>Job Title</th>
                  <th>Salary</th>
                  <th>Joining Date</th>
                  <th>Created At</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="placement in placements" :key="placement.id">
                  <td>{{ placement.company }}</td>
                  <td>{{ placement.job_title }}</td>
                  <td>{{ placement.salary }}</td>
                  <td>{{ placement.joining_date }}</td>
                  <td>{{ placement.created_at }}</td>
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
    name: 'StudentDashboard',
    components: {
        NavBar
    },
    data() {
        return{
            profile: {
                full_name: '',
                education: '',
                skills: '',
                cgpa: '',
                branch: '',
                graduation_year: '',
                resume: ''
            },
            jobs: [],
            applications: [],
            searchQuery: '',
            resumeFile: null,
            placements: [],
            exportMessage: '',
            exportFilename: '',
            exportTaskId: '',
            activeTab: 'jobs',
            branches: [],
            successMessage: '',
            errorMessage: ''
        }
    },
    mounted() {
        this.fetchProfile()
        this.fetchJobs()
        this.fetchApplications()
        this.fetchPlacements()
        this.fetchBranches()
    },
    methods: {
        async fetchProfile() {
            const token = localStorage.getItem('token')
            const response = await fetch('http://127.0.0.1:5000/student/profile', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.profile = data
        }, 
        async updateProfile() {
            const token = localStorage.getItem('token')
            const response = await fetch('http://127.0.0.1:5000/student/profile', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(this.profile)
            })
            const data = await response.json()
            if (response.ok) {
              this.successMessage = data.message
              this.errorMessage = ''
            } else {
                this.errorMessage = data.message
                this.successMessage = ''
            }
        },
        async fetchJobs() {
            const token = localStorage.getItem('token')
            const response = await fetch('http://127.0.0.1:5000/student/jobs', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.jobs = data
        },
        async searchJobs() {
            const token = localStorage.getItem('token')
            const response = await fetch(
                `http://127.0.0.1:5000/student/jobs?search=${encodeURIComponent(this.searchQuery)}`,
                {
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                }
            )
            const data = await response.json()
            this.jobs = data
        },
        async applyJob(jobId) {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/student/jobs/${jobId}/apply`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            if (response.ok) {
              this.successMessage = data.message
              this.errorMessage = ''
              this.fetchJobs()
              this.fetchApplications()
            } else {
              this.errorMessage = data.message
              this.successMessage = ''
            }
            
        },
        async fetchApplications() {
            const token = localStorage.getItem('token')
            const response = await fetch('http://127.0.0.1:5000/student/applications', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.applications = data 
        },
        handleFileUpload(event) {
            this.resumeFile = event.target.files[0]
        },
        async uploadResume() {
            if (!this.resumeFile) {
                alert('Please select a file first')
                return
            }
            const token = localStorage.getItem('token')
            const formData = new FormData()
            formData.append('resume', this.resumeFile)

            const response = await fetch('http://127.0.0.1:5000/student/resume', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                },
                body: formData
            })
            const data = await response.json()
            if (response.ok) {
              this.successMessage = data.message
              this.errorMessage = ''
              this.fetchProfile()
            } else {
              this.errorMessage = data.message
              this.successMessage = ''
            }
            
        },
        async fetchPlacements() {
            const token = localStorage.getItem('token')
            const response = await fetch('http://127.0.0.1:5000/student/placements', {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.placements = data
        },
        async exportApplications() {
            const token = localStorage.getItem('token')
            const response = await fetch('http://127.0.0.1:5000/student/export', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.exportMessage = data.message 
            this.exportTaskId = data.task_id

            setTimeout(() => this.checkExportStatus(), 3000)
        },
        async checkExportStatus() {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/student/export/${this.exportTaskId}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            if (data.status === 'complete') {
                this.exportMessage = `Export complete!`
                this.exportFilename = data.filename
            } else if (data.status === 'pending') {
                this.exportMessage = 'Still processing...'
                setTimeout(() => this.checkExportStatus(), 3000)
            }
        },
        async fetchBranches() {
          const response = await fetch('http://127.0.0.1:5000/public/branches')
          this.branches = await response.json()
        },
        isEligible(job) {
          if (job.minimum_cgpa && (!this.profile.cgpa || this.profile.cgpa < job.minimum_cgpa)) {
            return false
          }
          if (job.eligible_branch && this.profile.branch && this.profile.branch.toLowerCase() !== job.eligible_branch.toLowerCase()) {
            return false
          }
          if (job.eligible_year && this.profile.graduation_year && this.profile.graduation_year != job.eligible_year) {
            return false 
          }
          return true 
        }
    }
}
</script>