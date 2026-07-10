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
            pendingCompanies: []
        }
    },
    mounted() {
        this.fetchStats()
        this.fetchPendingCompanies()
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
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        }
    }
}
</script>