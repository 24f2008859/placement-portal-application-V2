<template>
    <div class="container mt-4">
        <h2>Student Dashboard</h2>
        <button class="btn btn-danger float-end" @click="logout">Logout</button>
    </div>
</template>

<script>
export default {
    name: 'StudentDashboard',
    methods: {
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            this.$router.path('/login')
        }
    }
}
</script>