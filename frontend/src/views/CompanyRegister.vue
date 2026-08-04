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
                <div class="col-md-6">
                    <div class="card border-0 shadow-sm">
                        <div class="card-body p-4">
                            <h3 class="fw-bold mb-4 text-center">Company Registration</h3>

                            <div class="mb-3">
                                <label class="form-label">Company Name *</label>
                                <input type="text" class="form-control" v-model="form.name" placeholder="Enter company name">
                                <div class="text-danger small" v-if="errors.name">{{ errors.name }}</div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Email *</label>
                                <input type="email" class="form-control" v-model="form.email" placeholder="Enter company email">
                                <div class="text-danger small" v-if="errors.email">{{ errors.email }}</div>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Password *</label>
                                <input type="password" class="form-control" v-model="form.password" placeholder="Min 6 characters" @keyup.enter="register">
                                <div class="text-danger small" v-if="errors.password">{{ errors.password }}</div>
                            </div>


                            <div class="mb-3">
                                <label class="form-label">Industry</label>
                                <input type="text" class="form-control" v-model="form.industry" placeholder="e.g. IT, Finance, Healthcare">
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Location</label>
                                <input type="text" class="form-control" v-model="form.location" placeholder="e.g. Mumbai, Delhi">
                            </div>


                            <div class="mb-3">
                                <label class="form-label">Website</label>
                                <input type="text" class="form-control" v-model="form.website" placeholder="e.g. https://company.com">
                            </div>

                            <div class="text-danger mb-3" v-if="errorMessage">{{ errorMessage }}</div>
                            <div class="text-success mb-3" v-if="successMessage">{{ successMessage }}</div>

                            <button class="btn btn-primary w-100" @click="register" :disabled="loading">Register</button>
                            <p class="text-center mt-3">Already have an account? <router-link to="/login">Login</router-link></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CompanyRegister',
    data() {
        return {
            form: {
                name: '',
                email: '',
                password: '',
                industry: '',
                location: '',
                website: ''
            },
            errors: {},
            errorMessage: '',
            successMessage: '',
            loading: false
        }
    },
    methods: {
        validate() {
            this.errors = {}

            if (!this.form.name) {
                this.errors.name = 'Company name is required'
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

            this.errorMessage = ''
            this.successMessage = ''
            this.loading = true

            try {
                const response = await fetch('http://127.0.0.1:5000/auth/register/company', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(this.form)
                })

                const data = await response.json()

                if (response.ok) {
                    this.successMessage = 'Registration successful! Awaiting admin approval.'

                    setTimeout(() => {
                        this.$router.push('/login')
                    }, 2000)

                } else {
                    this.errorMessage = data.message || 'Registration failed.'
                }

            } catch(error) {
                this.errorMessage = 'Unable to connect to server.'
            }
            finally {
                this.loading = false
            }
        }
    }
}
</script>