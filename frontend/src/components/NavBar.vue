<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <span class="navbar-brand fw-bold">PlaceMe</span>
            <div class="ms-auto d-flex align-items-center">
                <span class="text-white me-3">{{ role }}</span>
                <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
            </div>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'NavBar',
    computed: {
        role() {
            const role = localStorage.getItem('role')
            if (role === 'admin') return 'Admin'
            if (role === 'student') return 'Student'
            if (role === 'company') return 'Company'
            return ''
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            this.$router.push('/login')
        }
    }
}
</script>