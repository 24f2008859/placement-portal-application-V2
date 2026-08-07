<template>
  <div style="background-color: #f8fafc; min-height: 100vh;">
    <NavBar />

    <div class="container-fluid px-4 py-4">
      <div v-if="successMessage" class="alert alert-success alert-dismissible fade show">
        {{ successMessage }}
        <button type="button" class="btn-close" @click="successMessage= ''"></button>
      </div>
      <div v-if="errorMessage" class="alert alert-danger alert-dismissible fade show">
        {{ errorMessage }}
        <button type="button" class="btn-close" @click="errorMessage= ''"></button>
      </div>
      <!-- Header -->
      <div class="d-flex justify-content-between align-items-start mb-4">
        <div>
          <h3 class="fw-bold mb-1">{{ companyName }}
            <span class="badge" :class="companyApproved ? 'bg-success':'bg-warning'">{{ companyApproved ? 'APPROVED': 'PENDING' }}</span>
          </h3>
          <p class="text-muted small mb-0">Company Portal • Placement Drives Management</p>
        </div>
        <button class="btn btn-primary" @click="showJobForm = !showJobForm">
          + Create Placement Drive
        </button>
      </div>

      <!-- Stats Cards -->
      <div class="row mb-4">
        <div class="col-md-6 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <p class="text-muted small mb-1">Total Jobs Posted</p>
            <h3 class="fw-bold mb-0">{{ totalJobs }}</h3>
          </div>
        </div>
        <div class="col-md-6 mb-3">
          <div class="card border-0 shadow-sm p-3">
            <p class="text-muted small mb-1">Total Applications</p>
            <h3 class="fw-bold mb-0">{{ totalApplications }}</h3>
          </div>
        </div>
      </div>

      <!-- Create Job Form -->
      <div class="card border-0 shadow-sm mb-4" v-if="showJobForm">
        <div class="card-body">
          <h5 class="fw-bold mb-3">Create New Placement Drive</h5>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Job Title *</label>
              <input type="text" class="form-control" placeholder="Job Title" v-model="newJob.title">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Location</label>
              <input type="text" class="form-control" placeholder="Location" v-model="newJob.location">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Skills Required</label>
              <input type="text" class="form-control" placeholder="Skills Required" v-model="newJob.skills_required">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Salary</label>
              <input type="number" class="form-control" placeholder="in lpa" v-model="newJob.salary">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Minimum CGPA</label>
              <input type="number" step="0.1" class="form-control" placeholder="e.g. 8.0" v-model="newJob.minimum_cgpa">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible Branch</label>
              <select class="form-select" v-model="newJob.eligible_branch">
                <option value="">All Branches</option>
                <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
              </select>
            </div>
            <div class="col-md-4 mb-3">
              <label class="form-label">Eligible Graduation Year</label>
              <input type="number" class="form-control" v-model="newJob.eligible_year">
            </div>
            <div class="col-md-12 mb-3">
              <label>Application Deadline</label>
              <input type="date" class="form-control" v-model="newJob.application_deadline">
            </div>
            <div class="col-md-12 mb-3">
              <label class="form-label">Job Description</label>
              <textarea class="form-control" placeholder="Job Description" v-model="newJob.description"></textarea>
            </div>
            <div class="col-md-12">
              <button class="btn btn-primary me-2" @click="postJob">Submit Drive</button>
              <button class="btn btn-outline-secondary" @click="showJobForm = false">Cancel</button>
            </div>
          </div>
        </div>
      </div>

      <!-- Edit Job Form -->
      <div class="card border-0 shadow-sm mb-4" v-if="showEditForm">
        <div class="card-body">
          <h5 class="fw-bold mb-3">Edit Placement Drive</h5>
          <div class="row">
            <div class="col-md-6 mb-3">
              <label class="form-label">Job Title *</label>
              <input type="text" class="form-control" v-model="editingJob.title">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Location</label>
              <input type="text" class="form-control" v-model="editingJob.location">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Skills Required</label>
              <input type="text" class="form-control" v-model="editingJob.skills_required">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Salary</label>
              <input type="number" class="form-control" v-model="editingJob.salary">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Minimum CGPA</label>
              <input type="number" step="0.1" class="form-control" v-model="editingJob.minimum_cgpa">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible Branch</label>
              <select class="form-select" v-model="editingJob.eligible_branch">
                <option value="">All Branches</option>
                <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
              </select>
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Eligible Year</label>
              <input type="text" class="form-control" v-model="editingJob.eligible_year">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Application Deadline</label>
              <input type="date" class="form-control" v-model="editingJob.application_deadline">
            </div>
            <div class="col-md-6 mb-3">
              <label class="form-label">Description</label>
              <textarea class="form-control" v-model="editingJob.description"></textarea>
            </div>
            <div class="col-md-12">
              <button class="btn btn-primary me-2" @click="submitEdit">Update Drive</button>
              <button class="btn btn-outline-secondary" @click="showEditForm = false">Cancel</button>
            </div>
          </div>
        </div>
      </div>
      <!-- Main Content -->
      <div class="row">
        <!-- Jobs List -->
        <div class="col-md-4">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <h5 class="fw-bold mb-3">Your Placement Drives <span class="badge bg-primary">{{ jobs.length }}</span></h5>
              <div v-for="job in jobs" :key="job.id"
                class="p-3 mb-2 rounded border cursor-pointer"
                :class="selectedJob && selectedJob.id === job.id ? 'border-primary bg-light' : ''"
                @click="viewApplications(job.id)"
                style="cursor: pointer;">
                <div class="d-flex justify-content-between align-items-start">
                  <h6 class="fw-bold mb-1">{{ job.title }}</h6>
                  <span class="badge" :class="job.status === 'approved' ? 'bg-success' : job.status === 'pending' ? 'bg-warning' : 'bg-secondary'">
                    {{ job.status.toUpperCase() }}
                  </span>
                </div>
                <p class="text-muted small mb-1">Salary: {{ job.salary }} LPA</p>
                <p class="text-muted small mb-0">Applicants: {{ job.total_applications }}</p>
                <div class="d-flex gap-2 mt-2">
                  <button class="btn btn-warning btn-sm" v-if="job.status === 'approved'" @click="closeJob(job.id)">Close Drive</button>
                  <button class="btn btn-outline-primary btn-sm" @click="editJob(job)">Edit</button>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Applications -->
        <div class="col-md-8">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div v-if="!selectedJob">
                <p class="text-muted text-center mt-4">Select a placement drive to view applications</p>
              </div>
              <div v-else>
                <div class="d-flex justify-content-between align-items-center mb-3">
                  <h5 class="fw-bold mb-0">Candidate Applications Pipeline</h5>
                  <span class="text-muted small">Showing {{ selectedJobApplications.length }} applicants</span>
                </div>
                <div v-for="app in selectedJobApplications" :key="app.id" class="card border mb-3">
                  <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                      <div>
                        <h6 class="fw-bold mb-0">{{ app.student_name }}</h6>
                        <p class="text-muted small mb-0">{{ app.student_email }}</p>
                      </div>
                      <span class="badge bg-primary">{{ app.status.toUpperCase() }}</span>
                    </div>
                    <p class="small mb-2"><strong>Skills:</strong> {{ app.skills }}</p>
                    <p class="small mb-3"><strong>Education:</strong> {{ app.education }}</p>
                    <div class="d-flex gap-2 flex-wrap">
                      <span class="text-muted small me-1">Move Status:</span>
                      <button class="btn btn-success btn-sm" @click="updateStatus(app.id, 'shortlisted')">Shortlist</button>
                      <button class="btn btn-primary btn-sm" @click="updateStatus(app.id, 'interview')">Interview</button>
                      <button class="btn btn-warning btn-sm" @click="updateStatus(app.id, 'selected')">Select</button>
                      <button class="btn btn-danger btn-sm" @click="updateStatus(app.id, 'rejected')">Reject</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
export default {
    name: 'CompanyDashboard',
    components: {
        NavBar
    },
    data() {
        return {
            companyName: '',
            companyApproved: false,
            totalJobs: 0,
            totalApplications: 0,
            jobs: [],
            selectedJobApplications: [],
            newJob: {
                title: '',
                description: '',
                skills_required: '',
                salary: '',
                location: '',
                minimum_cgpa: '',
                eligible_branch: '',
                eligible_year: '',
                application_deadline: ''
            },
            branches: [],
            showJobForm: false,
            selectedJob: null,
            successMessage: '',
            errorMessage: '',
            showEditForm: false,
            editingJob: {}
        }
    },
    mounted() {
        this.fetchDashboard()
        this.fetchJobs()
        this.fetchBranches()
    }, 
    methods: {
        async fetchDashboard() {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/company/dashboard`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.companyName = data.company_name
            this.totalJobs = data.total_jobs
            this.totalApplications = data.total_applications
            this.companyApproved = data.is_approved
        },
        async fetchJobs() {
            const token = localStorage.getItem('token')
            const response = await fetch(`http://127.0.0.1:5000/company/jobs`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.jobs = data
        },
        async postJob() {
          const token = localStorage.getItem('token')
          const response = await fetch(`http://127.0.0.1:5000/company/jobs`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify(this.newJob)
          })
          const data = await response.json()
          if (response.ok) {
            this.successMessage = data.message
            this.errorMessage = ''
          
            this.newJob = { 
                title: '', 
                description: '', 
                skills_required: '', 
                salary: '', 
                location: '', 
                minimum_cgpa: '',
                eligible_branch: '',
                eligible_year: '',
                application_deadline: ''
              }
            this.fetchJobs()
            this.fetchDashboard()
            this.showJobForm = false
        } else {
            this.errorMessage = data.message
            this.successMessage = ''
          }
        },
        async viewApplications(jobId) {
          this.selectedJob = this.jobs.find(j => j.id === jobId)
          const token = localStorage.getItem('token')
          const response = await fetch(`http://127.0.0.1:5000/company/jobs/${jobId}/applications`, {
              headers: {
                  'Authorization': `Bearer ${token}`
              }
          })
          const data = await response.json()
          this.selectedJobApplications = data
        },
        async updateStatus(appId, status) {
          const token = localStorage.getItem('token')
          const response = await fetch(`http://127.0.0.1:5000/company/applications/${appId}/status`, {
              method: 'PUT',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify({status: status})
          })
          const data = await response.json()
          if (response.ok) {
            this.successMessage = data.message 
            this.errorMessage = ''
            this.selectedJobApplications = []
          } else {
            this.errorMessage = data.message
            this.successMessage = ''
          }
          this.viewApplications(this.selectedJob.id)
        },
        async closeJob(jobId) {
          const token = localStorage.getItem('token')
          const response = await fetch(`http://127.0.0.1:5000/company/jobs/${jobId}/status`, {
              method: 'PUT',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': `Bearer ${token}`
              },
              body: JSON.stringify({ status: 'closed'})
          })
          const data = await response.json()
          if (response.ok) {
            this.successMessage = data.message 
            this.errorMessage = ''
            this.fetchJobs()
          } else {
            this.errorMessage = data.message 
            this.successMessage = ''
          }
          
        },
        async fetchBranches() {
          const response = await fetch('http://127.0.0.1:5000/public/branches')
          this.branches = await response.json()
        },
        editJob(job) {
          this.editingJob = {...job}
          this.showEditForm = true 
          this.showJobForm = false
        },
        async submitEdit() {
          const token = localStorage.getItem('token')
          const response = await fetch(`http://127.0.0.1:5000/company/jobs/${this.editingJob.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(this.editingJob)
          })
          const data = await response.json()
          if (response.ok) {
            this.successMessage = data.message
            this.errorMessage = ''
            this.showEditForm = false 
            this.fetchJobs()
          } else {
            this.errorMessage = data.message
            this.successMessage = ''
          }
        }
    }
} 
</script>