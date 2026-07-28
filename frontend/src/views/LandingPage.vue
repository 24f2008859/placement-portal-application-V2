<template>
    <div>
        <!-- Navbar -->
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
            <div class="container">
                <a class="navbar-brand fw-bold">PlaceMe</a>
                <div class="ms-auto">
                    <router-link to="/login" class="btn btn-light me-2">Login</router-link>
                    <router-link to="/register" class="btn btn-outline-light">Register</router-link>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <div class="bg-primary text-white py-5">
            <div class="container text-center py-4">
                <h1 class="display-4 fw-bold">Welcome to PlaceMe</h1>
                <p class="lead mt-3">Connecting Students with Top Companies for Better Career Opportunities</p>
                <div class="mt-4">
                    <router-link to="/login" class="btn btn-light btn-lg me-3">Get Started</router-link>
                    <router-link to="/register" class="btn btn-outline-light btn-lg">Register Now</router-link>
                </div>
            </div>
        </div>

        <!-- Stats Section -->
        <div class="container my-5">
            <div class="row text-center">
                <div class="col-md-4">
                    <div class="card border-0 shadow-sm p-4">
                        <h2 class="text-primary fw-bold">{{ stats.total_students }}+</h2>
                        <p class="text-muted">Students Registered</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 shadow-sm p-4">
                        <h2 class="text-primary fw-bold">{{ stats.total_companies }}+</h2>
                        <p class="text-muted">Companies Onboard</p>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card border-0 shadow-sm p-4">
                        <h2 class="text-primary fw-bold">{{ stats.total_jobs }}+</h2>
                        <p class="text-muted">Placement Drives</p>
                    </div>
                </div>
            </div>
        </div>

        <!-- How it Works -->
        <div class="bg-light py-5">
            <div class="container">
                <h2 class="text-center fw-bold mb-5">How It Works</h2>
                <div class="row text-center">
                    <div class="col-md-4 mb-4">
                        <div class="card border-0 shadow-sm p-4 h-100">
                            <div class="fs-1 mb-3">🎓</div>
                            <h5 class="fw-bold">Students</h5>
                            <p class="text-muted">Register, build your profile, upload resume and apply for placement drives from top companies</p>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4">
                        <div class="card border-0 shadow-sm p-4 h-100">
                            <div class="fs-1 mb-3">🏢</div>
                            <h5 class="fw-bold">Companies</h5>
                            <p class="text-muted">Register your company, get approved by admin, post placement drives and find the best talent.</p>
                        </div>
                    </div>
                    <div class="col-md-4 mb-4">
                        <div class="card border-0 shadow-sm p-4 h-100">
                            <div class="fs-1 mb-3">⚙️</div>
                            <h5 class="fw-bold">Admin</h5>
                            <p class="text-muted">Manage the entire placement process, approve companies and drives, track statistics.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Footer -->
        <footer class="bg-primary text-white text-center py-3">
            <p class="mb-0">© 2026 PlaceMe — All Rights Reserved</p>
        </footer>
    </div>
</template>


<script>
export default {
    name: 'LandingPage',
    data() {
        return {
            stats: {
                total_students: 0,
                total_companies: 0,
                total_jobs: 0
            }
        }
    },
    mounted() {
        this.fetchStats()
    },
    methods: {
        async fetchStats() {
            const response = await fetch('http://127.0.0.1:5000/public/stats')
            const data = await response.json()
            this.stats = data 
        }
    }
}
</script>