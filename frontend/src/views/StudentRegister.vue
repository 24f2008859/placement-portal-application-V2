<template>
    <div>
        <!-- Navbar -->
        <nav class="navbar navbar-dark bg-primary">
            <div class="container">
                <router-link to="/" class="navbar-brand fw-bold">PlaceME</router-link>
            </div>
        </nav>

        <div class="container mt-5">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body p-4">
                            <h3 class="fw-bold mb-4 text-center">Student Registration</h3>

                            <div class="mb-3">
                                <label class="form-label">Full Name *</label>
                                <input type="text" class="form-control" v-model="form.full_name" placeholder="Enter your full name">
                                <div class="text-danger small" v-if="errors.full_name">{{ errors.full_name }}</div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Email *</label>
                                <input type="email" class="form-control" v-model="form.email" placeholder="Enter your email">
                                <div class="text-danger small" v-if="errors.email">{{ errors.email }}</div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Password *</label>
                                <input type="password" class="form-control" v-model="form.password" placeholder="Min 6 characters">
                                <div class="text-danger small" v-if="errors.password">{{ errors.password }}</div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Phone</label>
                                <input type="text" class="form-control" v-model="form.phone" placeholder="Enter your phone number">
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Education</label>
                                <input type="text" class="form-control" v-model="form.education" placeholder="e.g. B.Tech Computer Science">
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Skills</label>
                                <input type="text" class="form-control" v-model="form.skills" placeholder="e.g. Python, Flask, Vue">
                            </div>


                            <div class="text-danger mb-3" v-if="errorMessage">{{ errorMessage }}</div>
                            <div class="text-success mb-3" v-if="successMessage">{{ successMessage }}</div>

                            <button class="btn btn-primary w-100" @click="register">Register</button>
                            <p class="text-center mt-3">Already have an account?<router-link to="/login">Login</router-link></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'StudentRegister',
    data() {
        return {
            form: {
                full_name: '',
                email: '',
                password: '',
                phone: '',
                education: '',
                skills: ''
            },
            errors: {},
            errorMessage: '',
            successMessage: ''
        }
    },
    methods: {
        validate() {
            this.errors = {}

            if (!this.form.full_name) {
                this.errors.full_name = 'Full name is required'
            }
            if (!this.form.email) {
                this.errors.email = 'Email is required'
            } else if (!this.form.email.includes('@')) {
                this.errors.email = 'Enter a valid email'
            }
            if (!this.form.password) {
                this.errors.password = 'Password is required'
            } else if (this.form.password.length < 6) {
                this.errors.password = 'Password must be at least 6 characters'
            }

            return Object.keys(this.errors).length === 0
        },
        async register() {
            if (!this.validate()) return 

            const response = await fetch('http://127.0.0.1:5000/auth/register/student', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(this.form)
            })
            const data = await response.json()

            if (response.ok) {
                this.successMessage = 'Register successful! Please login.'
                setTimeout(() => this.$router.push('/login'), 2000)
            } else {
                this.errorMessage = data.message
            }
        }
    }
}
</script>