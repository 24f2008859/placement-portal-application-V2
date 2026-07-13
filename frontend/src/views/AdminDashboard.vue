<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2>Admin Dashboard</h2>
      <button class="btn btn-danger" @click="logout">Logout</button>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title">Students</h5>
            <h2>{{ stats.total_students }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title">Companies</h5>
            <h2>{{ stats.total_companies }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title">Jobs</h5>
            <h2>{{ stats.total_jobs }}</h2>
          </div>
        </div>
      </div>
      <div class="col-md-3">
        <div class="card text-center">
          <div class="card-body">
            <h5 class="card-title">Applications</h5>
            <h2>{{ stats.total_applications }}</h2>
          </div>
        </div>
      </div>
    </div>

    <!-- Pending Companies -->
    <div class="card mb-4">
        <div class="card-body">
            <h4>Pending Companies</h4>
            <table class="table">
                <thead>
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
        </div>
    </div>
    
    <!-- Search Companies -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>Search Companies</h4>
                <div class="row mb-3">
                    <div class="col-md-5">
                        <input type="text" class="form-control" placeholder="Search by name" v-model="companySearch.name">
                    </div>
                    <div class="col-md-5">
                        <input type="text" class="form-control" placeholder="Search by industry" v-model = "companySearch.industry">
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-primary w-100" @click="searchCompanies">Search</button>
                    </div>
                </div>
                <table class="table">
                    <thead>
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
                            <td>{{ company.is_approved ? 'Approved' : 'Pending' }}</td>
                            <td>
                            <button class="btn btn-warning btn-sm me-2" @click="deactivateCompany(company.id)">Deactivate</button>
                            <button class="btn btn-danger btn-sm" @click="removeCompany(company.id)">Remove</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    
    <!-- Search Students -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>Search Students</h4>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <input type="text" class="form-control" placeholder="Search by name" v-model="studentSearch.name">
                    </div>
                    <div class="col-md-3">
                        <input type="text" class="form-control" placeholder="Search by ID" v-model="studentSearch.id">
                    </div>
                    <div class="col-md-3">
                        <input type="text" class="form-control" placeholder="Search by phone" v-model="studentSearch.phone">
                    </div>
                    <div class="col-md-2">
                        <button class="btn btn-primary w-100" @click="searchStudents">Search</button>
                    </div>               
                </div>
                <table class="table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Name</th>
                            <th>Phone</th>
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
                            <td>{{ student.phone }}</td>
                            <td>{{ student.education }}</td>
                            <td>{{ student.skills }}</td>
                            <td>{{ student.is_active ? 'Active' : 'Deactivated' }}</td>
                            <td>
                                <button class="btn btn-warning btn-sm me-2" @click="deactivateStudent(student.id)">Deactivate</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
     <!-- All Jobs  -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>All Job Postings</h4>
                <table class="table">
                    <thead>
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
                            <td>{{ job.status }}</td>
                            <td>
                                <button class="btn btn-success btn-sm me-2" @click="approveJob(job.id)">Approve</button>
                                <button class="btn btn-danger btn-sm" @click="removeJob(job.id)">Remove</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    <!-- All Applications -->
        <div class="card mb-4">
            <div class="card-body">
                <h4>All Applications</h4>
                <table class="table">
                    <thead>
                        <tr>
                            <th>Student</th>
                            <th>Job</th>
                            <th>Company</th>
                            <th>Status</th>
                            <th>Applied At</th>
                        </tr>
                    </thead>
                    <tbody v-for="application in allApplications" :key="application.id">
                        <td>{{ application.student }}</td>
                        <td>{{ application.job }}</td>
                        <td>{{ application.company }}</td>
                        <td>{{ application.status }}</td>
                        <td>{{ application.applied_at }}</td>
                    </tbody>
                </table>
            </div>
        </div>
</template>
<script>
export default {
    name: 'AdminDashboard',
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
            id: '',
            phone: ''
            },
            searchedStudents: [],
            allJobs:[],
            allApplications: []
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
                `http://127.0.0.1:5000/admin/students/search?name=${this.studentSearch.name}&id=${this.studentSearch.id}&phone=${this.studentSearch.phone}`,
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
            const response = await fetch(`http://127.0.0.1:5000/admin/jobs/${jobId}approve`, {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            })
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
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        }
    }
}
</script>