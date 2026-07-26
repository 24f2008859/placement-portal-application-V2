<template>
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Student Dashboard</h2>
            <button class="btn btn-danger float-end" @click="logout">Logout</button>
        </div>
        
        <!-- Profile Section -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>My Profile</h4>
                <div class="row">
                    <div class="col-md-6 mb-3">
                        <label>Full Name</label>
                        <input type="text" class="form-control" v-model="profile.full_name">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label>Phone</label>
                        <input type="text" class="form-control" v-model="profile.phone">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label>Education</label>
                        <input type="text" class="form-control" v-model="profile.education">
                    </div>
                    <div class="col-md-6 mb-3">
                        <label>Skills</label>
                        <input type="text" class="form-control" v-model="profile.skills">
                    </div>
                    <div class="col-md-12 mb-3">
                        <label>Resume (PDF, DOC, DOCX)</label>
                        <input type="file" class="form-control" @change="handleFileUpload" accept=".pdf,.doc,.docx">
                    </div>
                    <div class="col-md-12 mb-3" v-if="profile.resume">
                        <p>Current Resume: {{ profile.resume }}</p>
                    </div>
                    <div class="col-md-12">
                        <button class="btn btn-primary me-2" @click="updateProfile">Update Profile</button>
                        <button class="btn btn-secondary" @click="uploadResume">Upload Resume</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Job Search -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>Available Jobs</h4>
                <div class="row mb-3">
                    <div class="col-md-10">
                        <input type="text" class="form-control" placeholder="Search by title, skills or location" v-model="searchQuery">
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-primary w-100" @click="searchJobs">Search</button>
                    </div>
                </div>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Company</th>
                            <th>Location</th>
                            <th>Salary</th>
                            <th>Skills Required</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="job in jobs" :key="job.id">
                            <td>{{ job.title }}</td>
                            <td>{{ job.company }}</td>
                            <td>{{ job.location }}</td>
                            <td>{{ job.salary }}</td>
                            <td>{{ job.skills_required }}</td>
                            <td>
                                <button class="btn btn-success btn-sm" @click="applyJob(job.id)">Apply</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- My Applications -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>My Applications</h4>
                <table class="table">
                    <thead>
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
                            <td>{{ app.status }}</td>
                            <td>{{ app.applied_at }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Placement History -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>Placement History</h4>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Company</th>
                            <th>Job Title</th>
                            <th>Salary</th>
                            <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="placement in placements" :key="placement.id">
                            <td>{{ placement.company }}</td>
                            <td>{{ placement.job_title }}</td>
                            <td>{{ placement.salary }}</td>
                            <td>{{ placement.created_at }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <!-- Export Applications -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>Export Applications</h4>
                <button class="btn btn-primary" @click="exportApplications">Export as CSV</button>
                <p class="mt-2" v-if="exportMessage">{{ exportMessage }}</p>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'StudentDashboard',
    data() {
        return{
            profile: {
                full_name: '',
                phone: '',
                education: '',
                skills: ''
            },
            jobs: [],
            applications: [],
            searchQuery: '',
            resumeFile: null,
            placements: [],
            exportMessage: '',
            exportTaskId: ''
        }
    },
    mounted() {
        this.fetchProfile()
        this.fetchJobs()
        this.fetchApplications()
        this.fetchPlacements()
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
            alert(data.message)
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
                `http://127.0.0.1:5000/student/jobs?search=${this.searchQuery}`,
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
            alert(data.message)
            this.fetchApplications()
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
            alert(data.message)
            this.fetchProfile()
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
                this.exportMessage = `Export complete! File: ${data.filename}`
            } else if (data.status === 'pending') {
                this.exportMessage = 'Still processing...'
                setTimeout(() => this.checkExportStatus(), 3000)
            }
        },
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        }
    }
}
</script>