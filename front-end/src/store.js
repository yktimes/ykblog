
export default {
  debug: true,
  state: {
    is_authenticated: window.localStorage.getItem('madblog-token') ? true : false,
    // 用户登录后，就算刷新页面也能再次计算出 user_id
    user_id: window.localStorage.getItem('user_id') ? window.localStorage.getItem('user_id') : 0,
    // 用户登录后，就算刷新页面也能再次计算出 user_name
    user_name: window.localStorage.getItem('user_name') ? window.localStorage.getItem('user_name') : '',
    // 用户登录后，就算刷新页面也能再次计算出 user_avatar
    // 后端传 URL 必须先用 base64 编码，所以这里还要多进行一次 atob 解码 base64 字符串
    user_avatar: window.localStorage.getItem('user_avatar') ?window.localStorage.getItem('user_avatar') : ''
  },
  loginAction () {
    if (this.debug) { console.log('loginAction triggered') }
    this.state.is_authenticated = true

    this.state.user_id =  window.localStorage.getItem('user_id')
    this.state.user_name = window.localStorage.getItem('user_name')
    this.state.user_avatar = window.localStorage.getItem('user_avatar')
  },
  logoutAction () {
    if (this.debug) console.log('logoutAction triggered')
    window.localStorage.removeItem('madblog-token')
    this.state.is_authenticated = false
    this.state.user_id = 0
    this.state.user_name = ''
    this.state.user_avatar = ''
  }
}
