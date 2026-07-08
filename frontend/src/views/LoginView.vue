<template>
    <div class="container mt-5">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-body">
                        <h3 class="card-title text-center">
                            PlaceMe Login
                        </h3>
                        <div class="mb-3">
                            <label>Email</label>
                            <input 
                                type="email"
                                class="form-control"
                                v-model="email"
                            >
                        </div>
                        <div class="mb-3">
                            <label>Password</label>
                            <input 
                                type="password"
                                class="form-control"
                                v-model="password"
                            >
                        </div>
                        <button class="btn btn-primary w-100" @click="login">Login</button>
                        <p class="text-danger mt-2">{{ errorMessage }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
        export default {
            data() {
                return {
                    email: '',
                    password: '',
                    errorMessage: ''
                }
            },
            methods: {
                async login() {
                    try {
                        const response = await fetch('http://127.0.0.1:5000/auth/login', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                email: this.email,
                                password: this.password
                            })
                        })
                        const data = await response.json()

                        if (response.ok) {
                            localStorage.setItem('token', data.access_token)
                            localStorage.setItem('role', data.role)

                            if (data.role === 'admin') {
                                this.$router.push('/admin/dashboard')
                            } else if (data.role === 'student') {
                                this.$router.push('/student/dashboard')
                            } else if (data.role === 'company') {
                                this.$router.push('/company/dashboard')
                            }
                        } else {
                            this.errorMessage = data.message
                        }
                    } catch (error) {
                        this.errorMessage = 'Something went wrong. Please try again.'
                    }
                }
            }
        }
    </script>
