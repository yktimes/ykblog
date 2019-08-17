<template>
  <div class="container">
    <h1>登录</h1>
    <div class="row">
      <div class="col-md-4">
        <form @submit.prevent="onSubmit">
          <div class="form-group" v-bind:class="{'u-has-error-v1': loginForm.usernameError}">
            <label for="username">用户名</label>
            <input type="text" v-model="loginForm.username" class="form-control" id="username" placeholder="">
            <small class="form-control-feedback" v-show="loginForm.usernameError">{{ loginForm.usernameError }}</small>
          </div>
          <div class="form-group" v-bind:class="{'u-has-error-v1': loginForm.passwordError}">
            <label for="password">密码</label>
            <input type="password" v-model="loginForm.password" class="form-control" id="password" placeholder="">
            <small class="form-control-feedback" v-show="loginForm.passwordError">{{ loginForm.passwordError }}</small>
          </div>
          <button type="submit" class="btn btn-primary">登录</button>
        </form>
      </div>
    </div>
    <br>
    <p>新用户? <router-link to="/register">去注册!</router-link></p>

  </div>
</template>

<script>
import store from '../../store'

export default {
  name: 'Login',  //this is the name of the component
  data () {
    return {
      sharedState: store.state,
      loginForm: {
        username: '',
        password: '',
        errors: 0,  // 表单是否在前端验证通过，0 表示没有错误，验证通过
        usernameError: null,
        passwordError: null
      }
    }
  },
  methods: {
    onSubmit (e) {
      this.loginForm.errors = 0  // 重置

      if (!this.loginForm.username) {
        this.loginForm.errors++
        this.loginForm.usernameError = 'Username required.'
      } else {
        this.loginForm.usernameError = null
      }

      if (!this.loginForm.password) {
        this.loginForm.errors++
        this.loginForm.passwordError = 'Password required.'
      } else {
        this.loginForm.passwordError = null
      }

      if (this.loginForm.errors > 0) {
        // 表单验证没通过时，不继续往下执行，即不会通过 axios 调用后端API
        return false
      }

      const path = '/api/tokens/'
      // axios 实现Basic Auth需要在config中设置 auth 这个属性即可
      this.$axios.post(path,{
        'username': this.loginForm.username,
         'password': this.loginForm.password

        },
      ).then((response) => {
          // handle success

          window.localStorage.setItem('yk-token', response.data.token)
          // TODO token
          window.localStorage.setItem('user_id', response.data.id)
          window.localStorage.setItem('user_name',response.data.user_name)

          window.localStorage.setItem('user_avatar',response.data.user_avatar)
          window.localStorage.setItem('permissions',response.data.permissions)
          this.$toasted.success(`Welcome ${this.sharedState.user_name}!`, { icon: 'fingerprint' })

          if (typeof this.$route.query.redirect == 'undefined') {

            this.$router.push('/')
          } else {
            this.$router.push(this.$route.query.redirect)
          }

          store.loginAction()


        })
       .catch((error) => {
          // handle error
          // console.log('failed', error.response);
          if (typeof error.response != 'undefined') {
            if (error.response.status == 400) {
              this.loginForm.usernameError = '用户名或密码错误.'
              this.loginForm.passwordError = '用户名或密码错误.'
            } else {
              console.log(error.response)
            }
          }
        })
    }
  }
}
</script>
