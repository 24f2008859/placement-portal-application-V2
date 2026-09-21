<template>
    <div>
        <!-- Navbar -->
        <nav class="navbar navbar-dark bg-primary">
            <div class="container">
                <router-link to="/" class="navbar-brand fw-bold">PlaceMe</router-link>
            </div>
        </nav>

        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6 text-center">
                    <h2 class="fw-bold mb-4">Join PlaceMe</h2>
                    <p class="text-muted mb-5">Choose how you want to register</p>
                    <div class="row">
                        <div class="col-md-6 mb-3">
                            <div class="card border-0 shadow-sm p-4 h-100">
                                <div class="fs-1 mb-3">🎓</div>
                                <h5 class="fw-bold">Student</h5>
                                <p class="text-muted small">Register as a student to apply for placement drives</p>
                                <router-link to="/register/student" class="btn btn-primary mt-2">Register as Student</router-link>
                            </div>
                        </div>
                        <div class="col-md-6 mb-3">
                            <div class="card border-0 shadow-sm p-4 h-100">
                                <div class="fs-1 mb-3">🏢</div>
                                <h5 class="fw-bold">Company</h5>
                                <p class="text-muted small">Register your company to post placement opportunities</p>
                                <router-link to="/register/company" class="btn btn-primary mt-2">Register as Company</router-link>
                            </div>
                        </div>
                    </div>
                    <p class="mt-4">Already have an account? <router-link to="/login">Login here</router-link></p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'RegisterPage'
}
</script>