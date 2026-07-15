<template>
    <div class="container mt-4">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2>Company Dashboard - {{ companyName }}</h2>
            <button class="btn btn-damger" @click="logout">Logout</button>
        </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
        <div class="col-md-6">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Total Jobs Posted</h5>
                    <h2>{{ totalJobs }}</h2>
                </div>
            </div>
        </div>
        <div class="col-md-6">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title">Total Applications</h5>
                    <h2>{{ totalApplications }}</h2>
                </div>
            </div>
        </div>
    </div>

    <!-- Post New Job -->
    <div class="card mb-4">
        <div class="card-body">
            <h4>Post New Job</h4>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <input type="text" class="form-control" placeholder="Job title" v-model="newJob.title">
                </div>
                <div class="col-md-6 mb-3">
                    <input type="text" class="form-control" placeholder="Location" v-model="newJob.location">
                </div>
                <div class="col-md-6 mb-3">
                    <input type="text" class="form-control" placeholder="Skills Required" v-model="newJob.skills_required">
                </div>
                <div class="col-md-6 mb-3">
                    <input type="text" class="form-control" placeholder="Salary" v-model="newJob.salary">
                </div>
                <div class="col-md-12 mb-3">
                    <textarea class="form-control" placeholder="Job Description" v-model="newJob.Description"></textarea>
                </div>
                <div class="col-md-12">
                    <button class="btn btn-primary" @click="postJob">Post Job</button>
                </div>
            </div>
        </div>
    </div>

    <!-- Jobs List -->
    <div class="card mb-4">
        <div class="card-body">
            <h4>My Job Postings</h4>
            <table class="table">
                <thead>
                    <tr>
                        <th>Title</th>
                        <th>Location</th>
                        <th>Salary</th>
                        <th>Status</th>
                        <th>Applications</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="job in jobs" :key="job.id">
                        <td>{{ job.title }}</td>
                        <td>{{ job.location }}</td>
                        <td>{{ job.salary }}</td>
                        <td>{{ job.status }}</td>
                        <td>{{ job.total_applications }}</td>
                        <td>
                            <button class="btn btn-info btn-sm me-2" @click="viewApplications(job.id)">View Applicants</button>
                            <button class="btn btn-warning btn-sm" @click="closeJob(job.id)">Close</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <!-- Applications Section -->
    <div class="card mb-4" v-if="selectedJobApplications.length > 0">
        <div class="card-body">
            <h4>Applicants</h4>
            <table class="table">
                <thead>
                    <tr>
                        <th>Name</th>
                        <th>Email</th>
                        <th>Skills</th>
                        <th>Education</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="app in selectedJobApplications" :key="app.id"> 
                        <td>{{ app.student_name }}</td>
                        <td>{{ app.student_email }}</td>
                        <td>{{ app.skills }}</td>
                        <td>{{ app.education }}</td>
                        <td>{{ app.status }}</td>
                        <td>
                            <button class="btn btn-success btn-sm me-1" @click="updateStatus(app.id, 'shortlisted')">Shortlist</button>
                            <button class="btn btn-primary btn-sm me-1" @click="updateStatus(app.id, 'interview')">Interview</button>
                            <button class="btn btn-warning btn-sm me-1" @click="updateStatus(app.id, 'selected')">Select</button>
                            <button class="btn btn-danger btn-sm me-1" @click="updateStatus(app.id, 'rejected')">Reject</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CompanyDashboard',
    data() {
        return {
            companyName: '',
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
            }
        }
    },
    mounted() {
        this.fetchDashboard()
        this.fetchJobs()
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
                    'Content_type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(this.newjob)
            })
            const data = await response.json()
            alert(data.message)
            this.newJob = { title: '', description: '', skills_required: '', salary: '', location: ''}
            this.fetchJobs()
            this.fetchDashboard()
        }, 
        async viewApplications(jobId) {
            const token = localStorage.getItem('token')
            const reponse = await fetch(`http://127.0.0.1:5000/company/jobs/${jobid}/applications`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
            const data = await response.json()
            this.selectedJobApplications = data
        },
        async updateStatus(appId, status) {
            const token = localStorage.getItem('token')
            const reponse = await fetch(`http://127.0.0.1:5000/company/applications/${appId}/status`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({status: status})
            })
            const data = await response.json()
            alert(data.message)
            this.selectedJobApplications = []
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
            alert(data.message)
            this.fetchJobs()
        },
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        }
    }
} 
</script>