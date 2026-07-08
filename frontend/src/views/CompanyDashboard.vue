<template>
    <div class="container mt-4">
        <h2>Company Dashboard</h2>
        <button class="btn btn-danger float-end" @click="logout">Logout</button>
    </div>
</template>

<script>
export default {
    name: 'CompanyDashboard',
    methods: {
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        }
    }
}
</script>