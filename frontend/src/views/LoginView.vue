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
        <div class="col-md-5">
          <div class="card border-0 shadow-sm">
            <div class="card-body p-4">
              <h3 class="fw-bold mb-4 text-center">Login to PlaceMe</h3>
              
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input 
                  type="email" 
                  class="form-control" 
                  v-model="email"
                  placeholder="Enter your email"
                >
              </div>
              <div class="mb-3">
                <label class="form-label">Password</label>
                <input 
                  type="password" 
                  class="form-control" 
                  v-model="password"
                  placeholder="Enter your password"
                >
              </div>
              <button 
                class="btn btn-primary w-100"
                @click="login"
              >
                Login
              </button>
              <p class="text-danger mt-2">{{ errorMessage }}</p>
              <p class="text-center mt-3">Don't have an account? <router-link to="/register">Register here</router-link></p>
            </div>
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
          localStorage.setItem('email', data.email)

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