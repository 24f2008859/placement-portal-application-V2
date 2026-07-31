<template>
    <nav style="background-color: #0f172a;"  class="navbar navbar-dark px-4 py-2">
        <div class="d-flex align-items-center gap-2">
            <div class="bg-primary rounded p-1">
                <span class="text-white fw-bold">🎓</span>
            </div>
            <span class="text-white fw-bold fs-5">PlaceMe</span>
        </div>
        <div class="d-flex align-items-center gap-3 ms-auto">
            <span class="text-white-50 small">{{ userEmail }}</span>
            <span class="text-white fw-semibold">{{ userName }}</span>
            <button class="btn btn-outline-light btn-sm" @click="logout">Logout</button>
        </div>
    </nav>
</template>

<script>
export default {
    name: 'NavBar',
    computed: {
        role() {
            return localStorage.getItem('role') || ''
        },
        userName() {
            const role = localStorage.getItem('role')
            if (role === 'admin') return 'Admin'
            if (role === 'student') return 'Student'
            if (role === 'company') return 'Company'
            return ''
        },
        userEmail() {
            return localStorage.getItem('email') || ''
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('role')
            localStorage.removeItem('email')
            this.$router.push('/login')
        }
    }
}
</script>